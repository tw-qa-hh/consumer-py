import atexit
import unittest

from pactman import Consumer, Provider, EachLike

from app import get_addresses

pact = Consumer('Consumer').has_pact_with(Provider('Provider'), use_mocking_server=True)
pact.start_service()
atexit.register(pact.stop_service)


class GetAddresses(unittest.TestCase):
    def test_get_addresses(self):
        expected = {'ID': '',  'Zip': '', 'Street': ''}

        (pact
         .given('test')
         .upon_receiving('a request for addresses')
         .with_request('get', '/')
         .will_respond_with(200, body=expected))

        with pact:
            result = get_addresses()

        self.assertEqual(expected, result[0])


if __name__ == '__main__':
    unittest.main()
