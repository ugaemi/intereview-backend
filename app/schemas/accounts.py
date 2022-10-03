from pydantic import BaseModel, Field, EmailStr, validator

from app.enums.accounts import Platform


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: EmailStr
    name: str = Field(min_length=3, max_length=30)
    password: str
    phone: str


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
