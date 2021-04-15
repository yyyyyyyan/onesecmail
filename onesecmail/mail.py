from random import choice as random_choice
from uuid import uuid4

import requests

from onesecmail.utils import get_default_headers


class OneSecMail:
    API_URL = "https://www.1secmail.com/api/v1/"
    DOMAINS = [
        "1secmail.com",
        "1secmail.net",
        "1secmail.org",
        "esiix.com",
        "wwjmp.com",
    ]

    def __init__(self, user, domain, **requests_kwargs):
        self.user = user
        self.domain = domain
        headers = get_default_headers()
        headers.update(requests_kwargs.pop("headers", {}))
        self.requests_kwargs = {"headers": headers, **requests_kwargs}

    def __repr__(self):
        return f"<OneSecMail [{self.address}]>"

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        if value not in self.DOMAINS:
            raise ValueError(f"{value} is not an allowed domain")
        self._domain = value

    @property
    def address(self):
        return f"{self.user}@{self.domain}"

    @classmethod
    def from_address(cls, address, **requests_kwargs):
        user, domain = address.split("@")
        return cls(user, domain, **requests_kwargs)

    @classmethod
    def get_random_mailbox(cls, **requests_kwargs):
        response = requests.get(
            cls.API_URL, params={"action": "genRandomMailbox"}, **requests_kwargs
        )
        user, domain = response.json()[0].split("@")
        return cls(user, domain, **requests_kwargs)

    @classmethod
    def generate_random_mailbox(cls, **requests_kwargs):
        user = uuid4().hex
        domain = random_choice(cls.DOMAINS)
        return cls(user, domain, **requests_kwargs)
