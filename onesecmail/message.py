"""This module contains the `EmailMessage` class definition."""
from datetime import datetime


class EmailMessage:
    """Represents a 1secmail message.

    Parameters
    ----------
    message_id : int
    from_address : str
    to_address : str
    date : str
        The date should follow the strftime format "%Y-%m-%d %H:%M:%S".
    subject : str, optional
    body : str, optional
    text_body : str, optional
    html_body : str, optional
    attachments : list, optional
    mail_handler : onesecmail.OneSecMail, optional
        The 1secmail mailbox to use to fetch the message's content or download attachments.

    Attributes
    ----------
    DATE_OFFSET : str, default: "+0200"
        The message's date UTC offset ('%z').
    id : int
    from_address : str
    to_address : str
    date : datetime.datetime
    subject : str
        The message's subject.
    body : str
        The message's body in any format.
    html_body : str
        The message's HTML body.
    text_body : str
        The message's text body.
    attachments : list of dict
        The message's list of attachments, without their content.
    """

    DATE_OFFSET = "+0200"

    def __init__(
        self,
        message_id,
        from_address,
        to_address,
        date,
        subject="",
        body="",
        text_body="",
        html_body="",
        attachments=None,
        mail_handler=None,
    ):
        self._id = message_id
        self._from_address = from_address
        self._to_address = to_address
        date += self.DATE_OFFSET
        self._date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
        self.subject = subject
        self.body = body
        self.text_body = text_body
        self.html_body = html_body
        self.attachments = attachments or []
        self._mail_handler = mail_handler

    def __repr__(self):
        subject = self.subject[:27] + "..." if len(self.subject) > 27 else self.subject
        return f"<EmailMessage; from='{self.from_address}', subject='{subject}', date='{self.date}'>"

    @property
    def id(self):
        """The message ID. This value should not be changed."""
        return self._id

    @property
    def from_address(self):
        """The sender's email address. This value should not be changed."""
        return self._from_address

    @property
    def to_address(self):
        """The recipient's email address. This value should not be changed."""
        return self._to_address

    @property
    def date(self):
        """The message's date. This value should not be changed."""
        return self._date

    @classmethod
    def from_dict(cls, data, **kwargs):
        """Creates an EmailMessage from a message dictionary.

        Parameters
        ----------
        data : dict
            The message dictionary. Used keys are 'id', 'from', 'to',
            'subject', 'date', 'attachments', 'body', 'textBody' and 'htmlBody'.
        **kwargs : dict, optional
            Additional kwargs will be passed into the EmailMessage constructor.
        """
        message_data = {
            "message_id": data["id"],
            "from_address": data["from"],
            "to_address": data["to"],
            "subject": data["subject"],
            "date": data["date"],
            "attachments": data.get("attachments"),
            "body": data.get("body"),
            "text_body": data.get("textBody"),
            "html_body": data.get("htmlBody"),
        }
        return cls(**message_data, **kwargs)

    def fetch_content(self, message_data=None):
        """Fetchs the message data.

        Fetchs the email message content (subject,
        body, textBody, htmlBody and attachments) into the
        EmailMessage object.

        Parameters
        ----------
        message_data : dict, optional
            A dictionary containing the message data to be incorporated
            by the EmailMessage object. If None is provided, the message
            content will be fetch using the `OneSecMail.get_message_as_dict()`
            method.

        Raises
        ------
        NotImplementedError
            If message_data is None and the EmailMessages' mail_handler
            is not set.
        """
        if message_data is None:
            if self._mail_handler is None:
                raise NotImplementedError(
                    "EmailMessage object can't fetch its content without a mail handler"
                )
            self.fetch_content(self._mail_handler.get_message_as_dict(self.id))
        else:
            self.subject = message_data.get("subject", self.subject)
            self.body = message_data.get("body", self.body)
            self.text_body = message_data.get("textBody", self.text_body)
            self.html_body = message_data.get("htmlBody", self.html_body)
            self.attachments = message_data.get("attachments", self.attachments)

    def get_attachment_content(self, filename):
        """Gets the content of an attachment.

        Parameters
        ----------
        filename : str
            The filename of the attachment.

        Returns
        -------
        bytes
            The content of the attachment.
        """
        return self._mail_handler.get_attachment_content(self.id, filename)

    def download_attachment(self, filename, save_path):
        """Downloads an attachment to a local file.

        Parameters
        ----------
        filename : str
            The filename of the attachment.
        save_path : path-like object
            The file path in which the attachment will be saved.
        """
        return self._mail_handler.download_attachment(self.id, filename, save_path)
