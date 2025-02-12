from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Literal, Optional
from uuid import UUID, uuid4
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Name(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    second_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)

class User_Base(BaseModel):
    name: Name
    email: EmailStr = Field(..., min_length=1, max_length=40)
    address: Optional[str] = Field(None, min_length=5, max_length=30)
    num_phone: str = Field(..., pattern=r'^\d{10}$')
    role: Literal["User", "Admin"] = "User"

class Create_User(User_Base):
    password: str = Field(..., min_length=8, max_length=30)

    @field_validator("password")
    @classmethod
    def hash_password(cls, password: str) -> str:
        "Returns the hashed password"

        return pwd_context.hash(password)
    
class User(User_Base):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str = Field(..., exclude=True)
    allowed_domains = ["gmail.com"]

    @field_validator("email")
    @classmethod
    def verify_email(cls, email: str) -> str:
        "Verify the email"

        domain = email.split("@")[-1]
        if domain not in cls.allowed_domains:
            raise ValueError("The email must be from {}".format(cls.allowed_domains))
        return email
