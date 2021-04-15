from requests.structures import CaseInsensitiveDict

from onesecmail import __title__
from onesecmail import __version__


def get_default_user_agent():
    """Return a string representing the default user agent.

    :rtype: str
    """
    return f"{__title__}/{__version__}"


def get_default_headers():
    """Return a dictionary representing the default request headers.

    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({"User-Agent": get_default_user_agent()})
