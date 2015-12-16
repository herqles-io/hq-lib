#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase, TestLoader, TextTestRunner

from hqlib.config import parse_config
from hqlib.config.error import HerqlesConfigError


class TestParseConfig(TestCase):

    def test_missing_file_error_handling(self):
        """ Missing config file should raise HerqlesConfigError """

        with self.assertRaises(HerqlesConfigError) as hce:
            parse_config('bogus_filename')

        self.assertIn('Could not load config file: ', str(hce.exception))

    # def test_valid_api_key(self):
    #     """ Validation of api key presence when returned with Redis data """

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:a4b05a8151b4ddda2739e355aefab48a': DEFAULT_API_CLIENT_DATA.copy(),
    #         },
    #     })

    #     api_request = APIRequest(DEFAULT_PAYLOAD)

    #     api_client = APIClient(api_request, mock_redis)

    #     self.assertTrue(api_client.valid_api_key)

    # def test_invalid_api_key(self):
    #     """ Validation of api key presence fails when no Redis data returned """

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:a4b05a8151b4ddda2739e355aefab48a': DEFAULT_API_CLIENT_DATA.copy(),
    #         },
    #     })

    #     request_data = DEFAULT_PAYLOAD.copy()
    #     request_data['api_key'] = 'unknown_api_key'
    #     api_request = APIRequest(request_data)

    #     with self.assertRaises(APIClientValidationError) as cve:
    #         APIClient(api_request, mock_redis)

    #     self.assertEqual(str(cve.exception), 'You must have a valid API key!')

    # def test_positive_validate_for_request(self):
    #     """ No errors thrown when validating valid api key data """

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:a4b05a8151b4ddda2739e355aefab48a': DEFAULT_API_CLIENT_DATA.copy(),
    #         },
    #     })

    #     api_request = APIRequest(DEFAULT_PAYLOAD)

    #     api_client = APIClient(api_request, mock_redis)

    #     self.assertIsNone(api_client.validate_for_request())

    # def test_invalid_api_key_for_validate_for_request(self):
    #     """ Test invalid api key generates APIClientValidationError """

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:a4b05a8151b4ddda2739e355aefab48a': DEFAULT_API_CLIENT_DATA.copy(),
    #         },
    #     })

    #     request_data = DEFAULT_PAYLOAD.copy()
    #     request_data['api_key'] = 'unknown_api_key'

    #     api_request = APIRequest(request_data)

    #     with self.assertRaises(APIClientValidationError) as cve:
    #         APIClient(api_request, mock_redis)

    #     self.assertEqual(str(cve.exception), 'You must have a valid API key!')

    # def test_inactive_client_for_validate_for_request(self):
    #     """ Test inactive api client generates HTTPError """

    #     api_client_data = DEFAULT_API_CLIENT_DATA.copy()
    #     api_client_data['active'] = 'False'

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:inactive_api': api_client_data,
    #         },
    #     })

    #     request_data = DEFAULT_PAYLOAD.copy()
    #     request_data['api_key'] = 'inactive_api'

    #     api_request = APIRequest(request_data)

    #     with self.assertRaises(APIClientValidationError) as cve:
    #         APIClient(api_request, mock_redis)

    #     self.assertEqual(str(cve.exception), 'You must have an active API key!')

    # def test_not_yet_active_client_for_validate_for_request(self):
    #     """ Test api client with a future contract start generates HTTPError """

    #     api_client_data = DEFAULT_API_CLIENT_DATA.copy()
    #     api_client_data['contract_start'] = \
    #             (datetime.now() + timedelta(days=1)).strftime(DATETIME_FORMAT)

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:future_contract_start': api_client_data,
    #         },
    #     })

    #     request_data = DEFAULT_PAYLOAD.copy()
    #     request_data['api_key'] = 'future_contract_start'

    #     api_request = APIRequest(request_data)

    #     with self.assertRaises(APIClientValidationError) as cve:
    #         APIClient(api_request, mock_redis)

    #     self.assertEqual(str(cve.exception), 'You must have an active API key!')

    # def test_expired_client_for_validate_for_request(self):
    #     """ Test api client with an expired contract generates HTTPError """

    #     api_client_data = DEFAULT_API_CLIENT_DATA.copy()
    #     api_client_data['contract_end'] = \
    #             (datetime.now() - timedelta(days=1)).strftime(DATETIME_FORMAT)

    #     mock_redis = mock_redis_client({
    #         'hgetall': {
    #             'api_keys:expired_contract': api_client_data,
    #         },
    #     })

    #     request_data = DEFAULT_PAYLOAD.copy()
    #     request_data['api_key'] = 'expired_contract'

    #     api_request = APIRequest(request_data)

    #     with self.assertRaises(APIClientValidationError) as cve:
    #         APIClient(api_request, mock_redis)

    #     self.assertEqual(str(cve.exception), 'You must have an active API key!')

    # def test_empty_default_messages_load(self):
    #     """ Verify that an empty value returns no message data """

    #     default_message_text = ''

    #     self.assertEqual(_load_default_messages(default_message_text), {})


    # def test_none_default_messages_load(self):
    #     """ Validate missing data is handled appropriately as well """
    #     default_message_text = None

    #     self.assertEqual(_load_default_messages(default_message_text), {})

    # def test_default_messages_load(self):

    #     default_message_data = {
    #         'default': {
    #             'message': 'This is a test',
    #             'button_label': 'Button',
    #         }
    #     }

    #     default_message_text = json.dumps(default_message_data)

    #     self.assertEqual(
    #         _load_default_messages(default_message_text),
    #         default_message_data)


if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(
        TestLoader().loadTestsFromTestCase(TestParseConfig))
