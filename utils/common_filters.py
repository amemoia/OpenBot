import re

__all__ = [
    "URL_RE",
    "INVITE_URL_RE",
    "MASS_MENTION_RE",
    "filter_urls",
    "filter_invites",
    "filter_mass_mentions",
    "filter_various_mentions",
    "normalize_smartquotes",
]

# regexes
URL_RE = re.compile(r"(https?|s?ftp)://(\S+)", re.I)

INVITE_URL_RE = re.compile(r"(discord.gg|discordapp.com/invite|discord.me)(\S+)", re.I)

MASS_MENTION_RE = re.compile(r"(@)(?=everyone|here)")  # This only matches the @ for sanitizing

OTHER_MENTION_RE = re.compile(r"(<)(@[!&]?|#)(\d+>)")

SMART_QUOTE_REPLACEMENT_DICT = {
    "\u2018": "'",  # Left single quote
    "\u2019": "'",  # Right single quote
    "\u201C": '"',  # Left double quote
    "\u201D": '"',  # Right double quote
}

SMART_QUOTE_REPLACE_RE = re.compile("|".join(SMART_QUOTE_REPLACEMENT_DICT.keys()))


# convenience wrappers
def filter_urls(to_filter: str) -> str:
    """Get a string with URLs sanitized.

    This will match any URLs starting with these protocols:

     - ``http://``
     - ``https://``
     - ``ftp://``
     - ``sftp://``

    Parameters
    ----------
    to_filter : str
        The string to filter.

    Returns
    -------
    str
        The sanitized string.

    """
    return URL_RE.sub("[SANITIZED URL]", to_filter)


def filter_invites(to_filter: str) -> str:
    """Get a string with discord invites sanitized.

    Will match any discord.gg, discordapp.com/invite, or discord.me
    invite URL.

    Parameters
    ----------
    to_filter : str
        The string to filter.

    Returns
    -------
    str
        The sanitized string.

    """
    return INVITE_URL_RE.sub("[SANITIZED INVITE]", to_filter)


def filter_mass_mentions(to_filter: str) -> str:
    """Get a string with mass mentions sanitized.

    Will match any *here* and/or *everyone* mentions.

    Parameters
    ----------
    to_filter : str
        The string to filter.

    Returns
    -------
    str
        The sanitized string.

    """
    return MASS_MENTION_RE.sub("@\u200b", to_filter)


def filter_various_mentions(to_filter: str) -> str:
    """
    Get a string with role, user, and channel mentions sanitized.

    This is mainly for use on user display names, not message content,
    and should be applied sparingly.

    Parameters
    ----------
    to_filter : str
        The string to filter.

    Returns
    -------
    str
        The sanitized string.
    """
    return OTHER_MENTION_RE.sub(r"\1\\\2\3", to_filter)


def normalize_smartquotes(to_normalize: str) -> str:
    """
    Get a string with smart quotes replaced with normal ones

    Parameters
    ----------
    to_normalize : str
        The string to normalize.

    Returns
    -------
    str
        The normalized string.
    """

    def replacement_for(obj):
        return SMART_QUOTE_REPLACEMENT_DICT.get(obj.group(0), "")

    return SMART_QUOTE_REPLACE_RE.sub(replacement_for, to_normalize)
