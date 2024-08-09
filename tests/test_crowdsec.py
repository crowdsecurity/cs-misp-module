# -*- coding: utf-8 -*-
"""CrowdSec unittest."""
import json
import os
import unittest
from unittest.mock import MagicMock, patch

from misp_modules.modules.expansion.crowdsec import (
    get_country_name_from_alpha_2,
    handler,
)


def load_file(filename: str):
    """Utility function to load a json file to a dict."""
    filepath = os.path.join(os.path.dirname(__file__), "resources", filename)
    with open(filepath, encoding="utf-8") as json_file:
        return json.load(json_file)


def remove_uuids(data):
    if isinstance(data, dict):
        return {
            key: remove_uuids(value)
            for key, value in data.items()
            if key not in ["uuid", "object_uuid"]
        }
    elif isinstance(data, list):
        return [remove_uuids(item) for item in data]
    else:
        return data


class TestCrowdsecModule(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.maxDiff = None

    @patch("misp_modules.modules.expansion.crowdsec.requests.get")
    def test_handler_valid_request(self, mock_get):
        mock_response = MagicMock()
        cti_data = load_file("malicious_ip.json")

        mock_response.json.return_value = cti_data
        mock_get.return_value = mock_response

        request_data = json.dumps(
            {
                "config": {"api_key": "test_api_key"},
                "attribute": {"type": "ip-src", "value": "1.2.3.4", "uuid": "1234"},
            }
        )
        response = handler(request_data)
        self.assertIn("results", response)
        expected_response = load_file("malicious_ip_result.json")
        # Remove UUIDs from both the actual response and expected response
        response_no_uuids = remove_uuids(response)
        expected_no_uuids = remove_uuids(expected_response)

        self.assertEqual(response_no_uuids, expected_no_uuids)

    def test_handler_missing_config(self):
        request_data = json.dumps(
            {"attribute": {"type": "ip-src", "value": "1.2.3.4", "uuid": "1234"}}
        )
        response = handler(request_data)
        self.assertEqual(response, {"error": "Missing CrowdSec Config"})

    def test_handler_missing_api_key(self):
        request_data = json.dumps(
            {
                "config": {"key": "value"},
                "attribute": {"type": "ip-src", "value": "1.2.3.4", "uuid": "1234"},
            }
        )
        response = handler(request_data)
        self.assertEqual(response, {"error": "Missing CrowdSec API key"})

    def test_handler_invalid_attribute(self):
        request_data = json.dumps(
            {
                "config": {"api_key": "test_api_key"},
                "attribute": {
                    "type": "invalid-type",
                    "value": "1.2.3.4",
                    "uuid": "1234",
                },
            }
        )
        response = handler(request_data)
        self.assertEqual(
            response,
            {
                "error": "Wrong input type. Please choose on of the following: ip-dst, ip-src"
            },
        )

    def test_get_country_name_from_alpha_2_valid(self):
        country_name = get_country_name_from_alpha_2("US")
        self.assertEqual(country_name, "United States")

    def test_get_country_name_from_alpha_2_invalid(self):
        country_name = get_country_name_from_alpha_2("XX")
        self.assertIsNone(country_name)
