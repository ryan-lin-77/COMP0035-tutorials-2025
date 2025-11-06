import sqlite3
from importlib import resources

from activities import starter



def create_db(sql_script_path, db_path):

    # 读取 SQL 文件内容
    with open(sql_script_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

    print(f"✅ Database created successfully at: {db_path}")

if __name__ == "__main__":
    sql_script_path = resources.files(starter).joinpath("student_schema.sql")
    db_path = "src/activities/solutions2/student.db"
    create_db(sql_script_path, db_path)