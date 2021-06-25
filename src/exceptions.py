"""This file will store the custom exceptions that might be triggered."""


class DuplicateEntryError(Exception):
    """Exception that will be raised when the program finds duplicate entries."""


class InternalServerError(Exception):
    """Exception that will be raised if there is an internal server error."""


class InvalidCharacterGenderError(Exception):
    """Exception that will be raised when the program finds an invalid gender."""


class NoMainCharactersError(Exception):
    """Exception that will be raised if there are no main characters."""


class NoMediaFoundError(Exception):
    """Exception that will be raised when the program finds a media that contains nothing."""


class TooManyRequestsError(Exception):
    """Exception that will be raised when the program hits a rate limiter."""
