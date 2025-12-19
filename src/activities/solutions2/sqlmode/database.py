# database.py
from __future__ import annotations

from pathlib import Path
from sqlmodel import SQLModel, create_engine

# ✅ 关键：导入 models，让表注册到 SQLModel.metadata
import models  # noqa: F401

# ✅ 把数据库固定放在本文件同级目录（sqlmode 文件夹里）
BASE_DIR = Path(__file__).resolve().parent
sqlite_file_path = BASE_DIR / "database.db"

engine = create_engine(f"sqlite:///{sqlite_file_path}", echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
