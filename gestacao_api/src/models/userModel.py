from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, sa_column_kwargs={"unique": True})
    password: str
    email: str = Field(index=True, sa_column_kwargs={"unique": True})

    last_menstrual_period: Optional[date]
    pregnancy_date: Optional[date]

    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

