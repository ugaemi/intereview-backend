from pydantic import BaseModel, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=12)
    email: str
    name: str = Field(min_length=3, max_length=30)
    password: str
