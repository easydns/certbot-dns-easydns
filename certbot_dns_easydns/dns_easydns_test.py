"""Tests for certbot_dns_easydns.dns_easydns."""

import sys
import unittest
from unittest import mock

import pytest
from requests.exceptions import HTTPError

from certbot.compat import os
from certbot.plugins import dns_test_common
from certbot.plugins import dns_test_common_lexicon
from certbot.plugins.dns_test_common import DOMAIN
from certbot.tests import util as test_util

API_KEY = "foo"
SECRET_KEY = "bar"


class AuthenticatorTest(
    test_util.TempDirTestCase,
    dns_test_common_lexicon.BaseLexiconAuthenticatorTest,
):
    def setUp(self):
        super().setUp()

        from certbot_dns_easydns.dns_easydns import Authenticator

        path = os.path.join(self.tempdir, "file.ini")
        dns_test_common.write(
            {
                "easydns_usertoken": API_KEY,
                "easydns_userkey": SECRET_KEY,
                "easydns_endpoint": "https://sandbox.rest.easydns.net",
            },
            path,
        )

        self.config = mock.MagicMock(
            easydns_credentials=path, easydns_propagation_seconds=0
        )  # don't wait during tests

        self.auth = Authenticator(self.config, "easydns")

        self.mock_client = mock.MagicMock()
        # _get_easydns_client | pylint: disable=protected-access
        self.auth._get_easydns_client = mock.MagicMock(
            return_value=self.mock_client
        )


class EasyDNSLexiconClientTest(
    unittest.TestCase, dns_test_common_lexicon.BaseLexiconClientTest
):
    DOMAIN_NOT_FOUND = HTTPError(
        "404 Client Error: Not Found for url: {0}.".format(DOMAIN)
    )
    LOGIN_ERROR = HTTPError(
        "403 Client Error: Forbidden for url: {0}.".format(DOMAIN)
    )

    def setUp(self):
        from certbot_dns_easydns.dns_easydns import _EasyDNSLexiconClient

        self.client = _EasyDNSLexiconClient(API_KEY, SECRET_KEY, 0)

        self.provider_mock = mock.MagicMock()
        self.client.provider = self.provider_mock


if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))  # pragma: no cover
