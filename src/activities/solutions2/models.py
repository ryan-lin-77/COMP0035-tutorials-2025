

from sqlmodel import Field, SQLModel
from typing import Optional


class team(SQLModel, table=True):
    code: str | None = Field(default=None, primary_key=True)
    name: str = Field()
    region: str = Field(
        sa_column_kwargs={
            "nullable": False
        }
    )
    sub_region: str
    member_type: str
    notes: str
    country_id: Optional[int] = Field(
        default=None,
        foreign_key="country.id",
    )
class country(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    country: str = Field()

class diabillity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field()