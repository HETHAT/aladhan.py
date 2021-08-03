__all__ = (
    "AladhanException",
    "HTTPException",
    "BadRequest",
    "InternalServerError",
    "InvalidArgument",
    "InvalidMethod",
    "InvalidTune",
    "InvalidSchool",
    "InvalidMidnightMode",
    "InvalidTimezone",
    "InvalidLatAdjMethod",
    "InvalidAdjustment",
)


class AladhanException(Exception):
    """
    Base exception class for aladhan.py

    Ideally speaking, this could be caught to handle any exceptions
        thrown from this library.

    Attributes
    ----------

        message: str
            Exception's message.
    """

    __slots__ = ("message",)

    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)


class HTTPException(AladhanException):
    """Exception that’s thrown when an HTTP request operation fails.

    Attributes
    ----------
        response: dict
            API's response.
        code: int
            Response's code.
    """

    __slots__ = "response", "code"

    def __init__(self, response, message: str = None):
        self.response = response
        self.code = response.get("code", 0)
        super().__init__(message or response.get("data"))

    @classmethod
    def from_res(cls, res):
        return {400: BadRequest, 500: InternalServerError}.get(
            res.get("code"), cls
        )(res)


class BadRequest(HTTPException):
    """Exception that’s thrown for when status code 400 occurs."""


class InternalServerError(HTTPException):
    """Exception that’s thrown for when status code 500 occurs."""


class InvalidArgument(AladhanException, ValueError):
    """Exception that’s thrown when an argument to a function is invalid
    some way (e.g. wrong value or wrong type)."""


class InvalidMethod(InvalidArgument):
    """Exception that’s thrown when method argument is invalid."""


class InvalidTune(InvalidArgument):
    """Exception that’s thrown when tune argument is invalid."""


class InvalidSchool(InvalidArgument):
    """Exception that’s thrown when school argument is invalid."""


class InvalidMidnightMode(InvalidArgument):
    """Exception that’s thrown when midnight mode argument is invalid."""


class InvalidTimezone(InvalidArgument):
    """Exception that’s thrown when timezone argument is invalid."""


class InvalidLatAdjMethod(InvalidArgument):
    """Exception that’s thrown when latitude adjustment method argument
    is invalid."""


class InvalidAdjustment(InvalidArgument):
    """Exception that’s thrown when adjustment argument is invalid."""
