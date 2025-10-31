import importlib.resources
import sqlite3

import pandas as pd

from activities import data


def print_data(file_path):
    """
    Attempts to open and read the contents of a file, handling potential errors gracefully.

    Demonstrates the use of `try`, `except`, `else`, and `finally` blocks:
    - `try`: Attempts to open the file.
    - `except FileNotFoundError`: Handles the case where the file does not exist.
    - `except Exception`: Handles any other errors.
    - `else`: Executes if no exception occurs, print the file's contents.
    - `finally`: Executes regardless of whether an exception occurred, printing a completion message.

    Args:
        file_path: The path to the file to open.

    Raises:
        FileNotFoundError: If the file does not exist.

    """
    try:
        data = file_path.read_text()
    except FileNotFoundError as e:
        print(f'Sorry, could not find that file. Error {e}')
    else:
        print(data)
    finally:
        print('Finished attempting to read the file.')


def print_data_group_example(file_path):
    """
    Attempts to open and read the contents of a file, handling potential errors gracefully.

    Demonstrates the use of exception groups (requires Python > 3.11)

    Args:
        file_path: The path to the file to open.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file does not grant permission to open.

    """
    try:
        data = file_path.read_text()
    except* FileNotFoundError as fnf_errors:
        for e in fnf_errors.exceptions:
            # Example also using the e.add_note method
            e.add_note("File not found while trying to locate the traffic data set")
            raise
    except* PermissionError as perm_errors:
        for e in perm_errors.exceptions:
            print(f"Permission error: {e}")
    else:
        print(f'File contents: {data}')
    finally:
        print('Finished attempting to read the file.')


def print_data_pattern_example(file_path):
    """
    Attempts to open and read the contents of a file, handling potential errors gracefully.

    Demonstrates the use of structural pattern matching (requires Python > 3.10)

    Args:
        file_path: The path to the file to open.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file does not grant permission to open.

    """
    try:
        data = file_path.read_text()
    except Exception as e:
        match e:
            case FileNotFoundError():
                print(f"File not found: {e}")
            case PermissionError():
                print(f"Permission error: {e}")
    else:
        print(f'File contents: {data}')
    finally:
        print('Finished attempting to read the file.')


# Activity 4.7 add exception handling to this function
def create_db(schema_path, db_path):
    """ Create a SQLite database using the provided schema file.

    Args:
        schema_path (str): Path to the SQL schema file.
        db_path (str): Path where the SQLite database will be created.
        Raises:
        FileNotFoundError: If the schema file does not exist.
        sqlite3.DatabaseError: If there is a SQL execution error.
        sqlite3.OperationalError: If the database cannot be created or written.
    """
    try:
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

    except FileNotFoundError:
        print(f"Schema file not found: {schema_path}")
        return
    except Exception as e:
        print(f"Error reading schema file: {e}")
        return
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error: {e}")
    finally:
        if conn:
            conn.close()

    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    # Execute the schema SQL
    cursor.executescript(schema_sql)

    # Commit and close the connection
    conn.commit()
    conn.close()


# Activity 4.7 add exception handling to this function
def describe(file_path):
    """Uses pandas DataFrame functions to describe the data.

    Applies the following pandas functions to the DataFrame and prints the output to file instead of terminal:
        df.shape
        df.head(num)
    NB some functions removed to shorten the output for the exception handling activity!

       Args:
           file_path: The path to the .csv file.

        Raises:
            FileNotFoundError: If the file does not exist.
            pd.errors.EmptyDataError: If the CSV file is empty.
             pd.errors.ParserError: If the CSV cannot be parsed.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"Empty CSV file: {file_path}")
        return
    except pd.errors.ParserError:
        print(f"Error parsing CSV file: {file_path}")
        return

    # 2.3 Describe
    pd.set_option("display.max_columns", None)  # Change the pandas display options to print all columns
    print("\nThe number of rows and columns\n", df.shape)
    print("\nThe first 5 rows\n", df.head(5))


if __name__ == '__main__':
    # Sample data files
    not_file = importlib.resources.files(data).joinpath("traffic.csv")  # exists
    is_file = importlib.resources.files(data).joinpath("student_data.csv")  # does not exist

    print_data(not_file)
    print_data(is_file)

    print_data_group_example(not_file)
    print_data_group_example(is_file)

    print_data_pattern_example(not_file)
    print_data_pattern_example(is_file)
