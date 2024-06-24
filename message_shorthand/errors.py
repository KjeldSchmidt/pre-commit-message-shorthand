"""Custom Errors for the message_shorthand module."""

from typing import Self


class SubstitutionMapJsonError(Exception):
    """Error raised when the substitution map is not valid JSON."""

    ERROR_MESSAGE = "The provided substitution map is not valid JSON"

    def __init__(self: Self) -> None:
        """Construct this error."""
        super().__init__(SubstitutionMapJsonError.ERROR_MESSAGE)


class SubstitutionMapInvalidError(Exception):
    """
    Error raised when the substitution map is invalid.

    Specifically, this occurs when the map is valid json, but not all key/value
    pairs simply map strings to strings.
    """

    ERROR_MESSAGE = "Substitutions do not map from string to string"

    def __init__(self: Self) -> None:
        """Construct this error."""
        super().__init__(SubstitutionMapInvalidError.ERROR_MESSAGE)
