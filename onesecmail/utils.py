"""Contains utility functions for 1secmail's API requests."""
from requests.structures import CaseInsensitiveDict

from onesecmail import __title__
from onesecmail import __version__


def get_default_user_agent():
    """Gets the default user agent.

    Generates the default user agent to be used in
    the API requests.

    Returns
    -------
    str
        The user agent formed by the package's title and version.
    """
    return f"{__title__}/{__version__}"


def get_default_headers():
    """Gets the default request headers.

    Returns
    -------
    requests.structures.CaseInsensitiveDict
        The request headers containing the default user agent.
    """
    return CaseInsensitiveDict({"User-Agent": get_default_user_agent()})
