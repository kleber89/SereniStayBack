from pydantic import field_validator, Field
from typing import Literal
from app.models.user import User_Base
from passlib.context import CryptContext
from uuid import UUID, uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Admin_Base(User_Base):
    permissions: list[str] = ["manage_users", "manage_services", "manage_spa"]
    role: Literal["Admin"] = "Admin"


class Create_Admin(Admin_Base):
    password: str = Field(..., min_length=8, max_length=30)

    @field_validator("password", mode="before")
    def hash_password(cls, password: str) -> str:
        "Returns the hashed password"

        return pwd_context.hash(password)
    

class Admin(Admin_Base):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str = Field(..., exclude=True)

    allowed_domains = ["gmail.com"]

    @field_validator("email", mode="before")
    def verify_email(cls, email: str) -> str:
        "Verify the email"

        domain = email.split("@")[-1]

        if domain not in cls.allowed_domains:
            raise ValueError(f"The email must be from {cls.allowed_domains}")
        return email
    