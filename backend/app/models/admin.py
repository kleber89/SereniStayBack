from pydantic import field_validator, Field, BaseModel, EmailStr
from typing import Literal, Optional
from user import Name
from base_model import BaseEntity
from passlib.context import CryptContext
from typing import ClassVar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Admin_Base(BaseEntity):
    name: Name
    email: EmailStr = Field(..., min_length=1, max_length=40)
    address: Optional[str] = Field(None, min_length=5, max_length=30)
    num_phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    permissions: list[str] = ["manage_users", "manage_services", "manage_spa"]
    role: Literal["Admin"] = "Admin"


class Create_Admin(Admin_Base):
    password: str = Field(..., min_length=8, max_length=60)

    @field_validator("password", mode="before")
    def hash_password(cls, password: str) -> str:
        "Returns the hashed password"

        return pwd_context.hash(password)
    

class Admin(Admin_Base):
    hashed_password: str = Field(..., exclude=True)

    allowed_domains: ClassVar[list[str]] = ["gmail.com"]

    @field_validator("email", mode="before")
    def verify_email(cls, email: str) -> str:
        "Verify the email"

        domain = email.split("@")[-1]

        if domain not in cls.allowed_domains:
            raise ValueError(f"The email must be from {cls.allowed_domains}")
        return email
    
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si la contraseña ingresada coincide con la contraseña hasheada.
        """
        return pwd_context.verify(plain_password, hashed_password)
