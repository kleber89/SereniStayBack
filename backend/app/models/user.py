from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Literal, Optional
from passlib.context import CryptContext
from typing import ClassVar
from app.models.base_model import BaseEntity


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Name(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=30)
    second_name: Optional[str] = Field(None, min_length=1, max_length=30)
    last_name: str = Field(..., min_length=1, max_length=30)

class User_Base(BaseEntity):
    name: Name
    email: EmailStr = Field(..., min_length=1, max_length=40)
    address: Optional[str] = Field(None, min_length=5, max_length=30)
    num_phone: Optional[str] = Field(None, pattern=r'^\d{10}$')
    role: Literal["User"] = "User"

class Create_User(User_Base):
    password: str = Field(..., min_length=8, max_length=60)

    @field_validator("password", mode="before")
    def hash_password(cls, password: str) -> str:
        "Returns the hashed password"

        return pwd_context.hash(password)
    
class User(User_Base):
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
