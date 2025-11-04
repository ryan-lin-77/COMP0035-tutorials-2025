# 直接使用 starter_db 的 main()
from activities.starter.starter_db import main as starter_main


def main():
    # 调用 starter_db.main() —— 它会：
    # 1. 读取 activities.data/paralympics_all_raw.xlsx
    # 2. 打印 COUNTRY CODES 与 GAMES 的数据分析
    starter_main()

    # 下面如果你还想继续用数据（例如额外打印或保存），
    # 可以修改 starter_db.py 里的 main() 让它返回 df_games, df_codes，
    # 或者直接复制那三行（path_para_raw + read_data_to_df + describe）到这里。



if __name__ == "__main__":
    main()