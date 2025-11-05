import sqlite3
from pathlib import Path

DB_PATH = Path("src/activities/solutions2/student.db")

def get_conn(db_path: Path):
    conn = sqlite3.connect(db_path)
    # 建议总是开启（SQLite 默认不启用外键约束）
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ---------- 单行插入 ----------
def insert_teacher(name: str, email: str):
    sql = "INSERT INTO teacher (teacher_name, teacher_email) VALUES (?, ?);"
    with get_conn(DB_PATH) as conn:
        conn.execute(sql, (name, email))
        conn.commit()

def insert_course(name: str, code: str, schedule: str, location: str):
    sql = """
    INSERT INTO course (course_name, course_code, course_schedule, course_location)
    VALUES (?, ?, ?, ?);
    """
    with get_conn(DB_PATH) as conn:
        conn.execute(sql, (name, code, schedule, location))
        conn.commit()

def insert_student(name: str, email: str):
    sql = "INSERT INTO student (student_name, student_email) VALUES (?, ?);"
    with get_conn(DB_PATH) as conn:
        conn.execute(sql, (name, email))
        conn.commit()

# ---------- 多行批量插入 ----------
def insert_many_students(rows):
    """
    rows: list[tuple[str, str]] -> [(student_name, student_email), ...]
    """
    sql = "INSERT INTO student (student_name, student_email) VALUES (?, ?);"
    with get_conn(DB_PATH) as conn:
        conn.executemany(sql, rows)
        conn.commit()

# ---------- 简单查询 ----------
def list_table(table: str, limit: int = 10):
    assert table in {"teacher", "course", "student"}, "只允许查看 teacher/course/student 表"
    sql = f"SELECT * FROM {table} LIMIT ?;"
    with get_conn(DB_PATH) as conn:
        cur = conn.execute(sql, (limit,))
        rows = cur.fetchall()
    print(f"--- {table} (最多 {limit} 条) ---")
    for r in rows:
        print(r)
    if not rows:
        print("(empty)")

if __name__ == "__main__":
    # 1) 插入示例老师 / 课程 / 学生（任选其一或全部）
    insert_teacher("John Smith", "john.smith@school.com")
    insert_teacher("Jane Doe", "jane.doe@school.com")

    insert_course("Mathematics", "MATH101", "Mon-Wed-Fri 9am", "Room 101")
    insert_course("Physics", "PHYS201", "Tue-Thu 11am", "Room 202")

    insert_student("Alice Brown", "alice.brown@school.com")
    insert_student("Bob Green", "bob.green@school.com")

    # 2) 批量插入学生
    batch = [
        ("Charlie White", "charlie.white@school.com"),
        ("Harpreet", "harpreet@school.com"),
    ]
    insert_many_students(batch)

    # 3) 查询看看是否写入成功
    list_table("teacher", limit=10)
    list_table("course", limit=10)
    list_table("student", limit=10)
