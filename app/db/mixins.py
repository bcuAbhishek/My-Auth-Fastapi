# app/db/mixins.py

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field


def created_at_column():
    return Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False
        )
    )


def updated_at_column():
    return Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    )
