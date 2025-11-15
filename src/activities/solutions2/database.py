# database.py
"""
Database engine and helper functions for creating the SQLite database.
"""

from sqlmodel import SQLModel, create_engine

# 导入 models，确保所有表类都被注册进 SQLModel.metadata
import models


DATABASE_URL = "sqlite:///paralympics_sqlmodel.db"

# echo=True 会在终端打印 SQL 语句，调试时很好用，不想看可以改成 False
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create all tables in the SQLite database."""
    SQLModel.metadata.create_all(engine)
