"""Io utilities for loading and saving data."""

import pandas as pd
from pathlib import Path

from src.dto import DateTimeFormat


def load_data(filepath: Path, datetime_col: str, datetime_format: DateTimeFormat) -> pd.DataFrame:
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

    if datetime_col not in df.columns:
        raise ValueError(f"Column '{datetime_col}' not found in data.")

    if datetime_format.type == "UNIX":
        df[datetime_col] = pd.to_datetime(df[datetime_col], unit=datetime_format.value, errors="coerce", utc=True)
    elif datetime_format.type == "DATETIME":
        df[datetime_col] = pd.to_datetime(df[datetime_col], format=datetime_format.value, errors="coerce")
    else:
        raise ValueError(f"Unsupported DateTimeFormat type: {datetime_format.type}")

    return df


def save_data(df: pd.DataFrame, filepath: Path):
    """Save DataFrame to a file."""
    df.to_csv(filepath, index=False)
