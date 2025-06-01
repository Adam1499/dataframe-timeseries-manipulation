import matplotlib.pyplot as plt
from pathlib import Path

from src.dto import DateTimeFormat
from src.io_utils import load_data, save_data
from src.noise import add_gaussian_noise
from src.resample import resample_dataframe

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def main(
    input_path: Path,
    output_path: Path,
    datetime_col: str,
    datetime_format: DateTimeFormat,
    output_frequency: str,
    no_negative: bool,
    add_noise_to_zeros: bool,
):
    df = load_data(input_path, datetime_col, datetime_format)
    df = df.set_index(datetime_col)
    df_modified = resample_dataframe(df, output_frequency)
    df_modified = add_gaussian_noise(df=df_modified, no_negative=no_negative, add_noise_to_zeros=add_noise_to_zeros)
    df_modified = df_modified.reset_index()
    save_data(df_modified, output_path)

    # --- Visualization for user feedback ---
    plt.figure(figsize=(12, 6))
    for col in df_modified.select_dtypes(include=["number"]).columns:
        if col != datetime_col:
            plt.plot(df_modified[datetime_col], df_modified[col], label=col)
    plt.xlabel(datetime_col)
    plt.ylabel("Values")
    plt.title("Resampled and Noised Data")
    plt.legend()
    plt.grid(True)
    plt.show()
    print("OK")


# --------------------------------------------------------------------
# For typical usage, you only need to modify the section below:
# Set input/output file paths and other parameters here as needed.
# --------------------------------------------------------------------

if __name__ == "__main__":
    main(
        input_path=INPUT_DIR / "Fisher.csv",
        output_path=OUTPUT_DIR / "Fischer_modified.csv",
        datetime_col="data_time",
        datetime_format=DateTimeFormat(type="UNIX", value="ms"),
        output_frequency="30s",
        no_negative=True,
        add_noise_to_zeros=False,
    )
