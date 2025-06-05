"""Main script."""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from src.dataclasses.datetimeparser import DateTimeParser, DateTimeParserDATETIME, DateTimeParserUNIX
from src.dataclasses.noise import NoiseSettings, BasicNoise, WithoutNoise
from src.dataclasses.resample import ResampleSettings, BasicResample, WithoutResample
from src.io_utils import load_data, save_data
from src.noise import noise_dataframe
from src.resample import resample_dataframe

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def main(
    input_path: Path,
    output_path: Path,
    datetime_settings: DateTimeParser,
    resample_settings: ResampleSettings,
    noise_settings: NoiseSettings,
):
    """Main function to load data, resample, add noise, and save the modified DataFrame."""
    df = load_data(input_path, datetime_settings)
    df = df.set_index(datetime_settings.index_column)

    df_modified = resample_dataframe(df, resample_settings)
    df_modified = noise_dataframe(df=df_modified, noise_settings=noise_settings)

    df_modified = df_modified.reset_index()
    save_data(df_modified, output_path)

    # # --- Visualization for user feedback ---
    # plt.figure(figsize=(12, 6))
    # for col in df_modified.select_dtypes(include=["number"]).columns:
    #     if col != datetime_col:
    #         plt.plot(df_modified[datetime_col], df_modified[col], label=col)
    # plt.xlabel(datetime_col)
    # plt.ylabel("Values")
    # plt.title("Resampled and Noised Data")
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # print("OK")


# --------------------------------------------------------------------
# For typical usage, you only need to modify the section below:
# Set input/output file paths and other parameters here as needed.
# --------------------------------------------------------------------

if __name__ == "__main__":
    input_folder = INPUT_DIR / "emflex_prod"
    for file in input_folder.glob("*.csv"):
        main(
            input_path=input_folder / file.name,
            output_path=OUTPUT_DIR / file.name,
            datetime_settings=DateTimeParserDATETIME(index_column="timestamp"),
            resample_settings=BasicResample("15t"),
            noise_settings=WithoutNoise(),
        )
