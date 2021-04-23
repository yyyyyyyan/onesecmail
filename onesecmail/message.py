from datetime import datetime


class EmailMessage:
    def __init__(
        self,
        message_id,
        from_address,
        date,
        subject="",
        body="",
        text_body="",
        html_body="",
        attachments=None,
        date_offset="+0000",
    ):
        self.id = message_id
        self.from_address = from_address
        date += date_offset
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
        self.subject = subject
        self.body = body
        self.text_body = text_body
        self.html_body = html_body
        self.attachments = attachments or []

    @classmethod
    def from_dict(cls, data, **kwargs):
        message_data = {
            "message_id": data["id"],
            "from_address": data["from"],
            "subject": data["subject"],
            "date": data["date"],
            "attachments": data["attachments"],
            "body": data["body"],
            "text_body": data["textBody"],
            "html_body": data["htmlBody"],
        }
        return cls(**message_data, **kwargs)