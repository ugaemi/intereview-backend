from pydantic import BaseModel, Field, EmailStr, validator

from app.enums.accounts import Platform
from app.services.accounts import get_valid_phone


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: EmailStr
    name: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)
    phone: str = Field(min_length=11)

    @validator("phone")
    def phone_valid(cls, v):
        if not get_valid_phone(v):
            raise ValueError("전화번호 형식에 맞지 않습니다.")
        return v


class FindUsername(BaseModel):
    platform: Platform
    platform_data: EmailStr | str
    name: str = Field(min_length=2, max_length=20)


class VerifyCodeForUsername(BaseModel):
    platform: Platform
    platform_data: EmailStr | str
    code: str


class GetResetPasswordLink(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: EmailStr


class ResetPassword(BaseModel):
    username: str
    code: str
    password: str
    password2: str

    @validator("password2")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v
