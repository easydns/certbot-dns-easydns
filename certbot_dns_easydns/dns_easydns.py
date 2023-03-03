"""DNS Authenticator for EasyDNS"""
import logging

from typing import Any, Callable, Optional

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon
from lexicon.providers import easydns
from requests import HTTPError

logger = logging.getLogger(__name__)

EASYDNS_REST = "https://rest.easydns.net"


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for EasyDNS

    This Authenticator uses the EasyDNS REST API to fulfill a ``dns-01`` challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using EasyDNS for DNS)."
    ttl = 60

    def __init__(self, *args, **kwargs) -> None:
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(
        cls, add: Callable[..., None], default_propagation_seconds: int = 120
    ) -> None:
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds
        )
        add("credentials", help="EasyDNS credentials INI file.")

    def more_info(
        self,
    ) -> str:  # pylint: disable=missing-docstring,no-self-use
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge using "
            + "the EasyDNS REST API."
        )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "EasyDNS credentials INI file",
            {
                "usertoken": "User token for REST API",
                "userkey": "Secret API key for the named user",
                "endpoint": "Endpoint to use for REST API operations",
            },
        )

    def _perform(
        self, domain: str, validation_name: str, validation: str
    ) -> None:
        self._get_easydns_client().add_txt_record(
            domain, validation_name, validation
        )

    def _cleanup(
        self, domain: str, validation_name: str, validation: str
    ) -> None:
        self._get_easydns_client().del_txt_record(
            domain, validation_name, validation
        )

    def _get_easydns_client(self) -> "_EasyDNSLexiconClient":
        if not self.credentials:
            raise errors.Error("Plugin could not obtain credentials.")
        return _EasyDNSLexiconClient(
            self.credentials.conf("usertoken"),
            self.credentials.conf("userkey"),
            self.credentials.conf("endpoint"),
            self.ttl,
        )


class _EasyDNSLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the EasyDNS REST API.
    """

    def __init__(
        self,
        usertoken: str,
        userkey: str,
        endpoint: str = None,
        ttl: int = None,
    ) -> None:
        logger.debug("creating EasyDNS client")
        super().__init__()
        self.endpoint = endpoint or EASYDNS_REST
        self.ttl = ttl or 60
        self.usertoken = usertoken
        self.userkey = userkey
        config = dns_common_lexicon.build_lexicon_config(
            "easydns",
            {"ttl": self.ttl},
            {
                "auth_username": self.usertoken,
                "auth_token": self.userkey,
                "api_endpoint": self.endpoint,
            },
        )
        self.provider = easydns.Provider(config)

    def _handle_http_error(
        self, e: HTTPError, domain_name: str
    ) -> Optional[errors.PluginError]:
        if domain_name in str(e) and str(e).startswith("404 "):
            return None
        hint = ""
        if str(e).startswith("403 "):
            hint = " (Are your API token and key values correct?)"
        return errors.PluginError(
            f"Error authenticating with EasyDNS REST API: {e}.{hint}"
        )
