from enum import Enum


class Platform(str, Enum):
    email: str = "email"
    phone: str = "phone"
