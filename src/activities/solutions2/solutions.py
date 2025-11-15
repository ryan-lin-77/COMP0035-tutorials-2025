import pandas as pd

import matplotlib.pyplot as plt
from pathlib import Path


def describe_dataframe(df):

    print("Data Shape:", df.shape)
    print("Columns:", df.columns)

    print("Data types:")
    print(df.dtypes)

    print("Info:")
    print(df.info())

    print("First few rows:")
    print(df.head())

    print("Missing values per column:")
    print(df.isnull().sum())

    print("Summary statistics:")
    print(df.describe())


 

def box_plots(df, title=None):
    num = df.select_dtypes(include="number")
    if num.shape[1] == 0:
        print(f"[skip] No numeric columns to plot: {title or 'DataFrame'}")

        return

    num.plot.box(figsize=(10,8), grid=True, title=title)
    plt.tight_layout()
    df.plot(x="start", y="participants", kind="line", title="Number of Participants Over Time")





if __name__ == '__main__':
    data_dir = Path(__file__).parent.parent / 'data'

    # 拼接 CSV 与 Excel 文件路径
    data_file_1 = data_dir / "paralympics_raw.csv"
    data_file_2 = data_dir / "paralympics_all_raw.xlsx"
    df_csv = pd.read_csv(data_file_1)

    df_excel_1 = pd.read_excel(data_file_2, sheet_name=0)
    df_excel_2 = pd.read_excel(data_file_2, sheet_name=1)

    print("\n=== CSV Data ===")
    describe_dataframe(df_csv)
    box_plots(df_csv, "CSV Data")

    print("\n=== Excel Sheet 1 ===")
    describe_dataframe(df_excel_1)
    box_plots(df_excel_1, "Excel Sheet 1")

    print("\n=== Excel Sheet 2 ===")
    describe_dataframe(df_excel_2)
    box_plots(df_excel_2, "Excel Sheet 2")

    plt.show()

