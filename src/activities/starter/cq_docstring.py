""" Examples of docstring styles and functions and class that are un-documented. """
import sqlite3

import pandas as pd
from matplotlib import pyplot as plt
import os
import io


# Google-style docstring specification: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
def get_column_names_g(db_path: str, table_name: str) -> list:
    """Retrieves a list of column names for the specified database table.

    Args:
        db_path: Path to the database file
        table_name: Name of the table

    Returns:
        col_names: List of column names
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    col_names = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return col_names


# Numpy-style docstring: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard
def get_column_names_n(db_path: str, table_name: str) -> list:
    """
        Retrieves a list of column names for the specified database table.

        Parameters
        ----------
        db_path : str
            Path to the database file.
        table_name : str
            Name of the table.

        Returns
        -------
        col_names: list
            List of column names.
        """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    col_names = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return col_names


# Sphinx/reStructuredText style docstring: https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html
# AI prompt:   /doc Sphinx format docstring
def get_column_names_s(db_path: str, table_name: str) -> list:
    """
        Retrieves a list of column names for the specified database table.

        :param db_path: Path to the database file.
        :type db_path: str
        :param table_name: Name of the table.
        :type table_name: str
        :return: List of column names.
        :rtype: list
        """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    col_names = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return col_names


# Copilot in VSCode / PyCharm
# Place the cursor under the function name and generate a docstring e.g. '/doc Google-style docstring'
def generate_histogram(df: pd.DataFrame):
    """Generate and save histograms for a DataFrame.
    Creates and saves three plots:
    1. All plottable columns -> "output/histogram_df.png"
    2. Columns ["participants_m", "participants_f"] -> "output/histogram_participants.png"
    3. Rows with df['type'] == 'summer' -> "output/histogram_summer.png"
    Args:
        df (pd.DataFrame): DataFrame containing numeric columns to plot. Should include
            'participants_m', 'participants_f', and 'type' for the specific plots.
    Raises:
        KeyError: If required columns ('participants_m', 'participants_f', 'type') are missing.
    Returns:
        None
    """
    
    # Histogram of any columns with values of a data type that can be plotted
    df.hist(
        sharey=False,  # defines whether y-axes will be shared among subplots.
        figsize=(12, 8)  # a tuple (width, height) in inches
    )
    plt.savefig("output/histogram_df.png")

    # Histograms of specific columns only
    df[["participants_m", "participants_f"]].hist()
    plt.savefig("output/histogram_participants.png")

    # Histograms based on filtered values
    summer_df = df[df['type'] == 'summer']
    summer_df.hist(sharey=False, figsize=(12, 8))
    plt.savefig("output/histogram_summer.png")


# Copilot in VSCode / PyCharm
# If you are happy to use gen-AI tools, place the cursor under the docstring and ask the AI to generate the code
def describe(csv_data_file: str) -> dict:
    """Opens the data as a pandas DataFrame applies pandas functions to describe the data.

    Applies the following pandas functions to the DataFrame and prints the output to file instead of terminal:
        df.shape
        dd.head(num)
        df.tail(num)
        df.columns
        df.dtypes
        df.describe()
        df.info()

       Args:
       csv_data_file (str): File path of the .csv format data file.

    """
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)

    try:
        df = pd.read_csv(csv_data_file)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV file '{csv_data_file}': {e}")

    results = {}
    results["shape"] = df.shape
    results["head"] = df.head().to_dict(orient="records")
    results["tail"] = df.tail().to_dict(orient="records")
    results["columns"] = df.columns.tolist()
    results["dtypes"] = {col: str(dtype) for col, dtype in df.dtypes.items()}
    results["describe"] = df.describe(include="all").to_dict()

    buf = io.StringIO()
    df.info(buf=buf)
    results["info"] = buf.getvalue()

    outfile = os.path.join(out_dir, f"{os.path.splitext(os.path.basename(csv_data_file))[0]}_describe.txt")
    with open(outfile, "w", encoding="utf-8") as fh:
        fh.write(f"Source file: {csv_data_file}\n\n")
        fh.write("SHAPE:\n")
        fh.write(f"{results['shape']}\n\n")
        fh.write("COLUMNS:\n")
        for c in results["columns"]:
            fh.write(f" - {c}\n")
        fh.write("\nDTYPES:\n")
        for k, v in results["dtypes"].items():
            fh.write(f" - {k}: {v}\n")
        fh.write("\nHEAD:\n")
        fh.write(df.head().to_string(index=False))
        fh.write("\n\nTAIL:\n")
        fh.write(df.tail().to_string(index=False))
        fh.write("\n\nDESCRIBE:\n")
        fh.write(df.describe(include="all").to_string())
        fh.write("\n\nINFO:\n")
        fh.write(results["info"])

    return results
 
