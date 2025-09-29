from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from app.db.mixins import created_at_column, updated_at_column


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    full_name: str = Field(nullable=False)
    phone_number: str = Field(unique=True, index=True, nullable=True)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(default="user")

    # OAuth fields
    oauth_provider: str = Field(default=None, nullable=True)  # "google", "github", etc.
    oauth_sub: str = Field(
        default=None, nullable=True, unique=True, index=True
    )  # Google's stable user ID

    created_at: datetime = created_at_column()
    updated_at: datetime = updated_at_column()
