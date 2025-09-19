#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function in utils.py.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json
import unittest.mock


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test class for the access_nested_map function.
    This class checks both successful dictionary lookups and expected exceptions.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """
        Test that access_nested_map returns the correct value
        when given a valid nested_map and path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, exception: type) -> None:
        """
        Test that access_nested_map raises a KeyError
        when the path is not present in the nested_map.
        """
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Unit test class for the get_json function in utils.py.
    This class uses mocking to simulate HTTP responses.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, url: str, expected_payload: dict) -> None:
        """
        Test that get_json returns the expected payload
        when given a specific URL.
        """
        with unittest.mock.patch('utils.requests.get') as mock_get:
            mock_get.return_value.json.return_value = expected_payload
            self.assertEqual(get_json(url), expected_payload)
            mock_get.assert_called_once_with(url)
