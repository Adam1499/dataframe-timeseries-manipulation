"""Module for defining datetime format settings in a DataFrame."""

from dataclasses import dataclass


@dataclass
class DateTimeParser:
    """Base class for datetime format settings in a DataFrame."""

    index_column: str


@dataclass
class DateTimeParserUNIX(DateTimeParser):
    """Class for UNIX timestamp format."""

    format: str = "ms"


@dataclass
class DateTimeParserDATETIME(DateTimeParser):
    """Class for datetime format."""

    format: str = "%Y-%m-%d %H:%M:%S%z"
