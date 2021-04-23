from datetime import datetime


class EmailMessage:
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
        date_offset="+0000",
    ):
        self._id = message_id
        self._from_address = from_address
        self._to_address = to_address
        date += date_offset
        self._date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
        self.subject = subject
        self.body = body
        self.text_body = text_body
        self.html_body = html_body
        self.attachments = attachments or []

    def __repr__(self):
        subject = self.subject[:27] + "..." if len(self.subject) > 27 else self.subject
        return f"<EmailMessage; from='{self.from_address}', subject='{subject}', date='{self.date}'>"

    @property
    def id(self):
        return self._id

    @property
    def from_address(self):
        return self._from_address

    @property
    def to_address(self):
        return self._to_address

    @property
    def date(self):
        return self._date

    @classmethod
    def from_dict(cls, data, **kwargs):
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

    def fetch_content(self, message_data):
        self.subject = message_data.get("subject", self.subject)
        self.body = message_data.get("body", self.body)
        self.text_body = message_data.get("textBody", self.text_body)
        self.html_body = message_data.get("htmlBody", self.html_body)
        self.attachments = message_data.get("attachments", self.attachments)
