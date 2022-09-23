from pydantic import BaseModel, Field, EmailStr

from app.enums.accounts import Platform


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: EmailStr
    name: str = Field(min_length=3, max_length=30)
    password: str


class FindUsername(BaseModel):
    platform: Platform
    platform_data: EmailStr | str
    name: str = Field(min_length=2, max_length=20)
