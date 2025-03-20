from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Literal, Optional, ClassVar
from passlib.context import CryptContext
from app.models.base_model import BaseEntity
from uuid import UUID, uuid4

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Name(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    second_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)


    @field_validator("first_name")
    @classmethod
    def verify_first_name(cls, value):
        """
        Verifying that first_name only receives 1 argument
        """

        if " " in value:
            raise ValueError("first_name should contain only one word")
        return value
    

    @field_validator("second_name")
    @classmethod
    def verify_second_name(cls, value):
        """
        Verifying that second_name only receives 1 argument
        """

        if value is not None and " " in value:
            raise ValueError("second_name should contain only one word")
        return value
    

class User_Base(BaseEntity):
    name: Name
    email: EmailStr = Field(..., min_length=1, max_length=40)
    address: Optional[str] = Field(None, min_length=5, max_length=30)
    num_phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    role: Literal["Client", "Owner"] = Field(...)

    allowed_domains: ClassVar[list[str]] = ["gmail.com"]

    @field_validator("email", mode="before")
    @classmethod
    def verify_email(cls, email: str) -> str:
        """Verify the email domain."""
        domain = email.split("@")[-1]
        if domain not in cls.allowed_domains:
            raise ValueError(f"The email must be from {cls.allowed_domains}")
        return email
    

class Create_User(User_Base):
    password: str = Field(..., min_length=8, max_length=60)

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Returns the hashed password"""
        return pwd_context.hash(password)
    
    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data["hashed_password"] = data.pop("password")
        return data
    
class User(User_Base):
    hashed_password: str

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify if the entered password matches the hashed password."""
        return pwd_context.verify(plain_password, hashed_password)
