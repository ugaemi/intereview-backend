from pydantic import BaseModel
from pydantic.schema import date


class SimpleCareer(BaseModel):
    name: str
    joined_date: date
    resignation_date: date | None
