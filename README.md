```
                                                   _ _
    ___  _ __   ___  ___  ___  ___ _ __ ___   __ _(_) |
   / _ \| '_ \ / _ \/ __|/ _ \/ __| '_ ` _ \ / _` | | |
  | (_) | | | |  __/\__ \  __/ (__| | | | | | (_| | | |
   \___/|_| |_|\___||___/\___|\___|_| |_| |_|\__,_|_|_|
```

# onesecmail

The unofficial Python client for the [1secmail API](https://www.1secmail.com/api/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install onesecmail:
```bash
pip install onesecmail
```

## Usage

Initialize a `OneSecMail` object using one of the class methods:

```python
>>> from onesecmail import OneSecMail
>>> # Uses 1secmail's genRandomMailbox action to get a random adress:
>>> mailbox = OneSecMail.get_random_mailbox()
>>> print(mailbox)
<OneSecMail [p8qhrjor@wwjmp.com]>
>>> # Generates a random address using uuid.uuid4():
>>> mailbox = OneSecMail.generate_random_mailbox()
>>> print(mailbox)
<OneSecMail [c05a619fe9a544dab818bde19a74c714@1secmail.net]>
>>> # Creates a mailbox using a pre-determined address:
>>> mailbox = OneSecMail.from_address("c05a619fe9a544dab818bde19a74c714@1secmail.net")
>>> print(mailbox)
<OneSecMail [c05a619fe9a544dab818bde19a74c714@1secmail.net]>
```

To retrieve a specific email message, you can use the methods `OneSecMail.get_message()` or `OneSecMail.get_message_as_dict()`:

```python
>>> message = mailbox.get_message(212959953)
>>> print(message)
<EmailMessage; from='contact@yyyyyyyan.tech', subject='Hello!', date='2021-06-25 23:49:12+02:00'>
>>> message.body
'Hi\n'
>>> message_data = mailbox.get_message_as_dict(212959953)
>>> print(message_data)
{'id': 212959953,
 'from': 'contact@yyyyyyyan.tech',
 'subject': 'Hello!',
 'date': '2021-06-25 23:49:12',
 'attachments': [],
 'body': 'Hi!\n',
 'textBody': 'Hi!\n',
 'htmlBody': '',
 'to': '101c71a3206c42668ca7bda6fe225138@1secmail.com'}
```

To get all messages of a mailbox, use the `OneSecMail.get_messages()` method:

```python
>>> messages = mailbox.get_messages()
>>> messages
[<EmailMessage; from='contact@yyyyyyyan.tech', subject='Random Email', date='2021-06-28 00:03:27+02:00'>,
 <EmailMessage; from='contact@yyyyyyyan.tech', subject='First Email', date='2021-06-28 01:06:27+02:00'>,
 <EmailMessage; from='yan@orestes.tech', subject='Second Email', date='2021-06-28 01:06:51+02:00'>]
```

You can also use the `get_messages()` method to search for email messages, by using validator functions/classes:

```python
>>> from onesecmail.validators import FromAddressValidator
>>> from_validator = FromAddressValidator("contact@yyyyyyyan.tech")
>>> mailbox.get_messages(validators=[from_validator])
[<EmailMessage; from='contact@yyyyyyyan.tech', subject='Random Email', date='2021-06-28 00:03:27+02:00'>,
 <EmailMessage; from='contact@yyyyyyyan.tech', subject='First Email', date='2021-06-28 01:06:27+02:00'>]
>>> from onesecmail.validators import DateRangeValidator
>>> from datetime import datetime
>>> date_validator = DateRangeValidator(min_date=datetime.strptime("2021-06-28 01+02:00", "%Y-%m-%d %H%z"))
>>> mailbox.get_messages(validators=[from_validator, date_validator])
[<EmailMessage; from='contact@yyyyyyyan.tech', subject='First Email', date='2021-06-28 01:06:27+02:00'>]]
>>> from onesecmail.validators import SubjectValidator
>>> mailbox.get_messages(validators=[SubjectValidator("(First|Second) Email")])
[<EmailMessage; from='contact@yyyyyyyan.tech', subject='First Email', date='2021-06-28 01:06:27+02:00'>,
 <EmailMessage; from='yan@orestes.tech', subject='Second Email', date='2021-06-28 01:06:51+02:00'>]]
```

To download an attachment, use either the `download_attachment()` method available on both `OneSecMail` and `EmailMessage` classes:

```python
>>> message = mailbox.get_message(213684185)
>>> message.attachments
[{'filename': 'attachment.c', 'contentType': 'text/x-csrc', 'size': 2636}]
# These do the same:
>>> message.download_attachment("attachment.c", "local-file.c")
>>> mailbox.download_attachment(213684185, "attachment.c", "local-file.c")
```

## Contributing

Pull Requests are welcome, whether it's regarding features, tests or documentation.

Just make sure you install the pre-commit hooks in your cloned repo before commiting any changes:

```bash
git clone https://github.com/yyyyyyyan/onesecmail.git
cd onesecmail
pip install -r requirements_dev.txt
pre-commit install
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yyyyyyyan/onesecmail/blob/main/LICENSE) file for details.
