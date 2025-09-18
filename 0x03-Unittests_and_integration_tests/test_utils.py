#!/usr/bin/env python3
"""
Unit tests for the access_nested_map function in utils.py.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


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
