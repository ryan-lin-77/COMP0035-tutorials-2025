import sqlite3
from importlib import resources
from src.activities import data  



def sample_select_queries(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Select all rows and columns from the student table
    cur.execute('SELECT * FROM student')
    rows = cur.fetchall()  # Fetches more than 1 row
    print("\nAll rows and columns from the student table\n")
    for row in rows:
        print(row)

    # Select the student_id column
    cur.execute('SELECT student_id FROM student WHERE student_name="Alice Brown"')
    row = cur.fetchone()  # Fetches the first result
    print("\nSelect the student_id: \n", row[0])

    cur.execute('SELECT teacher_name, teacher_email FROM teacher WHERE teacher_id in (1, 2)')
    rows = cur.fetchall()  # Fetches all rows from the result
    print("\nTeacher name and email where the teacher is id 1 or 2\n")
    for row in rows:
        print(row)

    # 1️⃣ Find all rows and columns for the courses table
    print("\nAll rows and columns from the courses table\n")
    cur.execute("SELECT * FROM course;")
    for row in cur.fetchall():
        print(row)

    # 2️⃣ Find the course code for 'Chemistry'
    print("\nCourse code for 'Chemistry'\n")
    cur.execute("SELECT course_code FROM course WHERE course_name = 'Chemistry';")
    row = cur.fetchone()
    if row:
        print(row[0])
    else:
        print("No Chemistry course found.")

    # 3️⃣ Find all courses where the schedule includes Monday
    print("\nAll courses where the schedule includes Monday\n")
    cur.execute("SELECT course_name FROM course WHERE course_schedule LIKE '%Mon%';")
    for row in cur.fetchall():
        print(row[0])

    con.close()


def main():
    db_path = resources.files(data).joinpath("sample.db")
    sample_select_queries(db_path)


if __name__ == "__main__":
    main()
