from dataclasses import dataclass
from typing import Literal


@dataclass
class DateTimeFormat:
    """Class to represent the format of datetime values in a DataFrame.

    Attributes:
        type (Literal["UNIX", "DATETIME"]): The type of datetime format.
        value (str): The value representing the format, e.g., "ms" for UNIX or a specific format string for DATETIME.
    """

    type: Literal["UNIX", "DATETIME"]
    value: str
