"""Io utilities for loading and saving data."""

import pandas as pd
from pathlib import Path

from src.dataclasses.datetimeparser import DateTimeParser, DateTimeParserUNIX, DateTimeParserDATETIME


def load_data(filepath: Path, datetime_parser: DateTimeParser) -> pd.DataFrame:
    """Load data from a file and parse the datetime column."""
    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath} does not exist.")

    try:
        if filepath.suffix.lower() in [".csv"]:
            df = pd.read_csv(filepath)
        elif filepath.suffix.lower() in [".xls", ".xlsx"]:
            df = pd.read_excel(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
    except Exception as e:
        raise ValueError(f"Failed to load data from {filepath}: {e}")

    if datetime_parser.index_column not in df.columns:
        raise ValueError(f"Column '{datetime_parser.index_column}' not found in data.")

    if isinstance(datetime_parser, DateTimeParserUNIX):
        df[datetime_parser.index_column] = pd.to_datetime(df[datetime_parser.index_column], unit=datetime_parser.format, errors="coerce", utc=True)
    elif isinstance(datetime_parser, DateTimeParserDATETIME):
        df[datetime_parser.index_column] = pd.to_datetime(df[datetime_parser.index_column], format=datetime_parser.format, errors="coerce")
    else:
        raise ValueError(f"Unsupported DateTimeParser type")

    return df


def save_data(df: pd.DataFrame, filepath: Path):
    """Save DataFrame to a file."""
    df.to_csv(filepath, index=False)
