#!/usr/bin/env python3

from utils import access_nested_map
import unittest

"""Does a unit test for utils from utils.access_nested_map
"""


class TestAccessNestedMap(unittest.TestCase):
    """TestAccessNestedMap class that is an unit test for utils.access_nested_map
    """

    def test_access_nested_map(self):
        """Test that access_nested_map returns the correct value for a given path in a nested dictionary."""

        test_cases = [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
        for nested_map, path, expected in test_cases:
            with self.subTest(nested_map=nested_map, path=path,
                              expected=expected):
                self.assertEqual(access_nested_map(nested_map, path),
                                 expected)

    def test_access_nested_map_exception(self):
        """Tests access_nested_map exception method
        """
        test_cases = [
            ({}, ("a",), KeyError),
            ({"a": 1}, ("a", "b"), KeyError),
        ]
        for nested_map, path, exception in test_cases:
            with self.subTest(nested_map=nested_map, path=path,
                              exception=exception):
                with self.assertRaises(exception):
                    access_nested_map(nested_map, path)
