from __future__ import annotations


class AppError(Exception):
    """Base class for application-level errors (GUI/domain/service)."""

    def __init__(self, message: str = "An error occurred."):
        self.__message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.__message


class DataNotLoadedError(AppError):
    """Raised when an operation requires data, but no CSV was loaded."""

    def __init__(self, message: str = "No data loaded. Please load a CSV file first."):
        super().__init__(message)


class InvalidInputError(AppError):
    """Raised when user input from the GUI is invalid or incomplete."""

    def __init__(self, message: str = "Invalid input. Please check your values."):
        super().__init__(message)


class GUIActionError(AppError):
    """Raised when a GUI action cannot be completed."""

    def __init__(self, message: str = "The requested action could not be completed."):
        super().__init__(message)
