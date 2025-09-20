#!/usr/bin/env python3
"""
Unit tests for client.py.
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock
from fixtures import TEST_PAYLOAD

TestCase = unittest.TestCase


class TestGithubOrgClient(TestCase):
    """
    Unit test class for the GithubOrgClient class.
    This class uses mocking to simulate HTTP responses
    and tests various methods of the GithubOrgClient.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(
            self,
            org_name: str,
            expected_payload: dict,
            mock_get_json: unittest.mock.Mock
    ) -> None:
        """
        Test that the org method returns the correct payload
        when get_json is mocked to return a specific value.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch("client.get_json")
    def test_public_repos_url(self,
                              org_name: str,
                              org_payload: dict,
                              mock_get_json: unittest.mock.Mock
                              ) -> None:
        """
        Test that the _public_repos_url property returns the correct URL
        based on the mocked org payload.
        """
        mock_get_json.return_value = org_payload
        client = GithubOrgClient(org_name)
        with patch.object(
                GithubOrgClient,
                'org',
                new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = org_payload
            self.assertEqual(client._public_repos_url,
                             org_payload["repos_url"])
            mock_org.assert_called_once()

    @parameterized.expand([
        (
            {"repos_url": "https://api.github.com/orgs/google/repos"},
            [{"name": "repo1"}, {"name": "repo2"}],
            ["repo1", "repo2"],
            None
        ),
        (
            {"repos_url":
             "https://api.github.com/orgs/google/repos"},
            [{"name": "repo1",
              "license": {"key": "mit"}},
             {"name": "repo2",
              "license": {"key": "apache-2.0"}},
             {"name": "repo3",
              "license": {"key": "mit"}}],
            ["repo1", "repo3"],
            "mit"
        ),
    ])
    @patch("client.get_json")
    def test_public_repos(self,
                          org_payload: dict,
                          repos_payload: list,
                          expected_repos: list,
                          license: str,
                          mock_get_json: unittest.mock.Mock
                          ) -> None:
        """
        Test that the public_repos method returns
        the correct list of repo names based on the
        mocked repos payload and optional license filter.
        """
        mock_get_json.side_effect = [org_payload, repos_payload]
        client = GithubOrgClient("google")
        with patch.object(
                GithubOrgClient,
                '_public_repos_url',
                new_callable=PropertyMock
        ) as mock_repos_url:
            mock_repos_url.return_value = org_payload["repos_url"]
            self.assertEqual(
                client.public_repos(license),
                expected_repos
            )
            mock_repos_url.assert_called_once()
            self.assertEqual(mock_get_json.call_count, 2)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self,
                         repo: dict,
                         license_key: str,
                         expected: bool
                         ) -> None:
        """
        Test that the has_license static method returns the correct boolean
        indicating whether the repo has the specified license.
        """

        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
    for org_payload, repos_payload, expected_repos, apache2_repos in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(TestCase):
    """
    Integration test class for the GithubOrgClient class.
    This class uses mocking to simulate HTTP responses
    and tests the public_repos method of the GithubOrgClient.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test class by patching requests.get
        to return a sequence of predefined payloads.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Define side effect for function to return different mocks per URL
        def get_side_effect(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/google":
                return PropertyMock(json=lambda: cls.org_payload, status_code=200)
            if url == cls.org_payload["repos_url"]:
                return PropertyMock(json=lambda: cls.repos_payload, status_code=200)
            raise ValueError(f"Unexpected URL: {url}")

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down the test class by stopping the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """ Test the public_repos method of GithubOrgClient. """
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos_with_license(self) -> None:
        """ Test the public_repos method with license filter. """
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
        self.assertEqual(self.mock_get.call_count, 2)
