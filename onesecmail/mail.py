"""The main module. Contains the OneSecMail class definition."""
from json import JSONDecodeError
from random import choice as random_choice
from uuid import uuid4

import requests

from onesecmail.message import EmailMessage
from onesecmail.utils import get_default_headers


class OneSecMail:
    """Represents a 1secmail mailbox.

    Parameters
    ----------
    user : str
        The mailbox username. This is everything that comes
        before the "@" in the email address.
    domain : str
        The mailbox domain. Restricted to those listed in OneSecMail.DOMAINS.
    **requests_kwargs : dict, optional
            Additional kwargs to be passed to the request.get call in the
            request method.

    Attributes
    ----------
    address : str
    user : str
    domain : str
    request_kwargs : dict
    API_URL : str
        The URL of the 1secmail API.
    DOMAINS : list
        The list of available domains for a 1secmail mailbox.
    """

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
        """The mailbox domain.

        Raises
        ------
        ValueError
            If the domain being set is not listed in self.DOMAINS.
        """
        return self._domain

    @domain.setter
    def domain(self, value):
        if value not in self.DOMAINS:
            raise ValueError(f"{value} is not an allowed domain")
        self._domain = value

    @property
    def address(self):
        """The mailbox email address."""
        return f"{self.user}@{self.domain}"

    @classmethod
    def from_address(cls, address, **requests_kwargs):
        """Generates a mailbox from a given email address.

        Parameters
        ----------
        address : str
            Email address following the [user]@[domain] pattern.
        **requests_kwargs : dict, optional
            Additional kwargs to be passed to the OneSecMail constructor.

        Returns
        -------
        OneSecMail
        """
        user, domain = address.split("@")
        return cls(user, domain, **requests_kwargs)

    @classmethod
    def get_random_mailbox(cls, **requests_kwargs):
        """Generates a mailbox with a random address from 1secmail's API.

        Parameters
        ----------
        **requests_kwargs : dict, optional
            Additional kwargs to be passed to the OneSecMail constructor.

        Returns
        -------
        OneSecMail
        """
        response = requests.get(
            cls.API_URL, params={"action": "genRandomMailbox"}, **requests_kwargs
        )
        user, domain = response.json()[0].split("@")
        return cls(user, domain, **requests_kwargs)

    @classmethod
    def generate_random_mailbox(cls, **requests_kwargs):
        """Generates a mailbox with a random address.

        Parameters
        ----------
        **requests_kwargs : dict, optional
            Additional kwargs to be passed to the OneSecMail constructor.

        Returns
        -------
        OneSecMail

        Notes
        -----
        The domain is randomly chosen from OneSecMail.DOMAINS.
        The user is generated using the uuid.uuid4() function,
        which means it will always be 32 characters long.
        """
        user = uuid4().hex
        domain = random_choice(cls.DOMAINS)
        return cls(user, domain, **requests_kwargs)

    def request(self, action, **params):
        """Makes request to 1secmail API's given action.

        Makes request to 1secmailAPI's given action providing
        the necessary 'login' and 'domain' parameters.

        Parameters
        ----------
        action : str
            The API action to be requested.
        **params : dict, optional
            Extra GET parameters to be added to the request.

        Returns
        -------
        requests.Response
        """
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
        """Gets email message data as a dictionary.

        Parameters
        ----------
        message_id : int

        Returns
        -------
        message_data : dict
            A dictionary containing the message's data (id, from,
            subject, date, body, textBody, htmlBody, to)

        Examples
        --------
        >>> mailbox = OneSecMail.from_address("101c71a3206c42668ca7bda6fe225138@1secmail.com")
        >>> message_data = mailbox.get_message_as_dict(212959953)
        >>> print(message_data)
        {'id': 212959953,
         'from': 'contact@yyyyyyyan.tech',
         'subject': 'Hello!',
         'date': '2021-06-25 23:49:12',
         'attachments': [],
         'body': 'Hi!\\n',
         'textBody': 'Hi!\\n',
         'htmlBody': '',
         'to': '101c71a3206c42668ca7bda6fe225138@1secmail.com'}
        """
        response = self.request("readMessage", id=message_id)
        try:
            message_data = response.json()
        except JSONDecodeError:
            raise ValueError(f"Error reading message #{message_id}: {response.text}")
        message_data["to"] = self.address
        return message_data

    def get_message(self, message_id):
        """Gets email message.

        Parameters
        ----------
        message_id : int

        Returns
        -------
        EmailMessage

        Examples
        --------
        >>> mailbox = OneSecMail.from_address("101c71a3206c42668ca7bda6fe225138@1secmail.com")
        >>> message = mailbox.get_message(212959953)
        >>> print(message)
        <EmailMessage; from='contact@yyyyyyyan.tech', subject='Hello!', date='2021-06-25 23:49:12+02:00'>
        """
        message_data = self.get_message_as_dict(message_id)
        return EmailMessage.from_dict(message_data, mail_handler=self)

    def get_messages(self, validators=()):
        """Gets multiple email messages given validators.

        Gets all available email messages and returns those that
        pass all given validators.

        Parameters
        ----------
        validators : iterable of functions, optional
            The sequence of functions that will be called with an EmailMessage
            object as the parameter.

        Returns
        -------
        list of EmailMessage
            List of EmailMessage objects that passed all validators.
        """
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

    def download_attachment(self, message_id, filename, save_path):
        """Downloads an attachment to a local file.

        Parameters
        ----------
        message_id : int
            The ID of the message from which the attachment will be fetched.
        filename : str
            The filename of the attachment.
        save_path : path-like object
            The file path in which the attachment will be saved.
        """
        attachment_content = self.get_attachment_content(message_id, filename)
        with open(save_path, "wb") as attachment_file:
            size = attachment_file.write(attachment_content)
        return save_path, size
