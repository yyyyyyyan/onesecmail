from json import JSONDecodeError
from random import choice as random_choice
from uuid import uuid4

import requests

from onesecmail.message import EmailMessage
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

    def request(self, action, **params):
        response = requests.get(
            self.API_URL,
            params={
                "action": action,
                "login": self.user,
                "domain": self.domain,
                **params,
            },
            **self.requests_kwargs,
        )
        response.raise_for_status()
        return response

    def get_message_as_dict(self, message_id):
        response = self.request("readMessage", id=message_id)
        try:
            message_data = response.json()
        except JSONDecodeError:
            raise ValueError(f"Error reading message #{message_id}: {response.text}")
        message_data["to"] = self.address
        return message_data

    def get_message(self, message_id):
        message_data = self.get_message_as_dict(message_id)
        return EmailMessage.from_dict(message_data, mail_handler=self)

    def search_messages(self, validators=()):
        response = self.request("getMessages")
        try:
            message_list = response.json()
        except JSONDecodeError:
            raise ValueError(f"Error getting messages: {response.text}")

        messages = []
        for message_data in message_list:
            message_data["to"] = self.address
            message = EmailMessage.from_dict(message_data, mail_handler=self)
            valid = True
            for validator in validators:
                if not validator(message):
                    valid = False
                    break
            if valid:
                message.fetch_content()
                messages.append(message)
        return messages

    def get_attachment_content(self, message_id, filename):
        """Gets the content of an attachment.

        Parameters
        ----------
        message_id : int
            The ID of the message from which the attachment will be fetched.
        filename : str
            The filename of the attachment.

        Returns
        -------
        bytes
            The content of the attachment.
        """
        response = self.request("download", id=message_id, file=filename)
        return response.content
