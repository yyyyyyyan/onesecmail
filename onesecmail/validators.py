import re
from datetime import datetime
from datetime import timezone


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


class DateRangeValidator:
    def __init__(self, min_date=None, max_date=None):
        if min_date is None:
            self.min_date = datetime.min.replace(tzinfo=timezone.utc)
        else:
            self.min_date = (
                min_date.astimezone() if min_date.tzinfo is None else min_date
            )
        if max_date is None:
            self.max_date = datetime.max.replace(tzinfo=timezone.utc)
        else:
            self.max_date = (
                max_date.astimezone() if max_date.tzinfo is None else max_date
            )

    def __call__(self, message):
        return self.min_date < message.date < self.max_date
