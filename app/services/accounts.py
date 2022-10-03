import random
import string
from datetime import timedelta, datetime
from typing import Optional

import phonenumbers
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from phonenumbers import PhoneNumber

from app.config import SECRET_KEY, ALGORITHM
from app.exceptions import invalid_phone_exception
from app.models.accounts import User

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="users/token")


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db) -> bool | User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
) -> str:
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def generate_verification_code(size: int) -> str:
    return "".join([random.choice(string.digits) for _ in range(size)])


def get_valid_phone(number: str) -> PhoneNumber:
    parsed_number = phonenumbers.parse(number)
    if not phonenumbers.is_possible_number(parsed_number):
        raise invalid_phone_exception()
    return parsed_number
