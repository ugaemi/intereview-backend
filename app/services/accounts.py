import random
import string
from datetime import timedelta, datetime
from typing import Optional

import phonenumbers
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from phonenumbers import PhoneNumber
from phonenumbers.phonenumberutil import NumberParseException

from app.config import SECRET_KEY, ALGORITHM
from app.models.accounts import User

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/accounts/token")


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
        expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def generate_verification_code(size: int) -> str:
    return "".join([random.choice(string.digits) for _ in range(size)])


def get_valid_phone(number: str) -> bool | PhoneNumber:
    try:
        parsed_number = phonenumbers.parse(number)
    except NumberParseException:
        return False
    if not phonenumbers.is_possible_number(parsed_number):
        return False
    return parsed_number
