import pytest
import os
import json

import requests
from pact import Consumer, Provider

from app import get_addresses

CONSUMER_NAME = 'consumer-py'
PROVIDER_NAME = 'provider-go'

PACT_DIR = '{}/pacts'.format(os.getcwd())

PACT_BROKER_URL = 'https://qa-ham-pact-broker.herokuapp.com'

PACT_UPLOAD_URL = '{}{}/{}'.format(PACT_BROKER_URL, '/pacts/provider/provider-go/consumer', CONSUMER_NAME)

PACT_FILE = '{}-{}.json'.format(CONSUMER_NAME, PROVIDER_NAME)


@pytest.fixture(scope='session')
def pact(request):
    print('PACT_DIR', PACT_DIR)
    pact = Consumer(CONSUMER_NAME, tag_with_git_branch=True) \
        .has_pact_with(Provider(PROVIDER_NAME), pact_dir=PACT_DIR)
    try:
        pact.start_service()
        yield pact
    finally:
        pact.stop_service()

    if not request.node.testsfailed:
        push_to_broker('1.0.6', 'master')


def test_get_addresses(pact):
    expected = {'ID': 'py', 'Zip': '000', 'Street': ''}

    (pact
     .given('test')
     .upon_receiving('a request for addresses')
     .with_request('get', '/')
     .will_respond_with(200, body=expected))

    with pact:
        result = get_addresses(pact.uri)
        assert expected == json.loads(result)

    pact.verify()


def push_to_broker(version, tag):
    """
    Push to broker
    """
    with open(os.path.join(PACT_DIR, PACT_FILE), 'rb') as pact_file:
        pact_file_json = json.load(pact_file)

    r = requests.put(
        "{}/version/{}".format(PACT_UPLOAD_URL, version),
        json=pact_file_json
    )

    if not r.ok:
        r.raise_for_status()

    r_t = requests.put("{}/pacticipants/{}/versions/{}/tags/{}"
                       .format(PACT_BROKER_URL, CONSUMER_NAME, version, tag),
                       json={})

    if not r_t.ok:
        r_t.raise_for_status()
