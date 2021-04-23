import re


class RegexValidator:
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, text):
        return re.match(self.pattern, text) is not None


class FromAddressValidator(RegexValidator):
    def __call__(self, message):
        return super().__call__(message.from_address)


class SubjectValidator(RegexValidator):
    def __call__(self, message):
        return super().__call__(message.subject)
