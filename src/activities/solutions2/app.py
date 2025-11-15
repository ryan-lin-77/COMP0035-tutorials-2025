# app.py
"""
Entry point for creating the Paralympics SQLModel database.
"""

from database import create_db_and_tables


def main() -> None:
    create_db_and_tables()
    print("✅ Database 'paralympics_sqlmodel.db' created (or already exists).")


if __name__ == "__main__":
    main()
