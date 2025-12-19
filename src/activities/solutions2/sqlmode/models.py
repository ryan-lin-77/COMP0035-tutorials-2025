from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import CheckConstraint, Column, ForeignKey

class team(SQLModel, table=True):
    code: str = Field(primary_key=True)
    name: str
    region: str  # 默认就是 NOT NULL（你不写 Optional 就不会是 NULL）
    sub_region: str
    member_type: str
    notes: str

    country_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            ForeignKey("country.id", ondelete="SET NULL", onupdate="CASCADE"),
            nullable=True
        )
    )

    __table_args__ = (
        CheckConstraint("region IN ('Asia', 'Europe', 'Africa', 'America', 'Oceania')"),
        CheckConstraint("member_type IN ('country', 'team', 'dissolved', 'construct')"),
    )

class country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    country: str = Field()

class diabillity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field()