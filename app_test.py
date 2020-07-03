import pytest
import os
import json

import requests
from pact import Consumer, Provider, EachLike, Like
from pact.matchers import get_generated_values

from app import get_addresses

CONSUMER_NAME = 'consumer-py'
PROVIDER_NAME = 'provider-go'

# PACT_DIR = './pacts'

PACT_BROKER_URL = 'https://qa-ham-pact-broker.herokuapp.com/'


@pytest.fixture(scope='session')
def pact():
    pact = Consumer(CONSUMER_NAME, tags=['master', 'consumer-py'], version='1.0.0') \
        .has_pact_with(Provider(PROVIDER_NAME),
                       # pact_dir=PACT_DIR, //https://github.com/pact-foundation/pact-python/issues/128
                       version='2.0.0',
                       publish_to_broker=True, broker_base_url=PACT_BROKER_URL)
    try:
        pact.start_service()
        yield pact
    finally:
        pact.stop_service()


def test_get_addresses(pact):
    expected = EachLike({
        'ID': Like('py'),
        'ZipCode': Like(''),
        'Street': Like('')
    })
    headers = {
        'Content-Type': 'application/json'
    }
    (pact
     .given('test')
     .upon_receiving('a request for addresses')
     .with_request('get', '/')
     .will_respond_with(200, headers=headers, body=expected))

    with pact:
        result = get_addresses(pact.uri + '/')
        assert result == get_generated_values(expected)

    pact.verify()
