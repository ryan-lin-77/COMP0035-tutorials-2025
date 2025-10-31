import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path





if __name__ == '__main__':
    data_dir = Path(__file__).parent.parent / 'data'

    # 拼接 CSV 与 Excel 文件路径
    data_file_1 = data_dir / "paralympics_raw.csv"
    data_file_2 = data_dir / "paralympics_all_raw.xlsx"
    df_csv = pd.read_csv(data_file_1)

    df_excel_1 = pd.read_excel(data_file_2, sheet_name=0)
    df_excel_2 = pd.read_excel(data_file_2, sheet_name=1)
