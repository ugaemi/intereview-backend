import datetime
from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import MessageSchema, FastMail
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY, TWILIO_PHONE_NUMBER
from app.database import get_db
from app.enums.accounts import Platform
from app.exceptions import (
    token_exception,
    get_user_exception,
    username_exist_exception,
    not_match_exception,
    not_verification_exception,
)
from app.mail import mail_conf
from app.models.accounts import User
from app.redis import DB_VERIFICATION_CODE
from app.schemas.accounts import FindUsername, CreateUser, VerifyCode
from app.services.accounts import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    oauth2_bearer,
    generate_verification_code,
    get_valid_phone,
)
from app.twilio import client

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=["accounts"],
)


@router.post("/")
async def create_new_user(data: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first() is not None:
        raise username_exist_exception()
    valid_phone = get_valid_phone(data.phone)
    create_user_model = User()
    create_user_model.email = data.email
    create_user_model.username = data.username
    create_user_model.name = data.name
    create_user_model.password = get_password_hash(data.password)
    create_user_model.phone_country_code = valid_phone.country_code
    create_user_model.phone_national_number = valid_phone.national_number
    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


@router.post("/find/username")
async def find_username(data: FindUsername, db: Session = Depends(get_db)):
    if data.platform.value == Platform.email:
        user = db.query(User).filter(User.email == data.platform_data).first()
        if user is None or user.name != data.name:
            raise not_match_exception()
        verification_code = generate_verification_code(6)
        message = MessageSchema(
            subject="[인터리뷰] 인증코드가 도착했습니다.",
            recipients=[data.platform_data],
            template_body={
                "code": verification_code,
            },
        )
        fm = FastMail(mail_conf)
        await DB_VERIFICATION_CODE.set(
            user.email, verification_code, datetime.timedelta(minutes=5)
        )
        await fm.send_message(message, template_name="accounts/verification_code.html")
    else:
        valid_phone = get_valid_phone(data.platform_data)
        user = (
            db.query(User)
            .filter(
                User.phone_country_code == valid_phone.country_code
                and User.phone_national_number == valid_phone.national_number
            )
            .first()
        )
        if user is None or user.name != data.name:
            raise not_match_exception()
        verification_code = generate_verification_code(6)
        await DB_VERIFICATION_CODE.set(
            data.platform_data, verification_code, datetime.timedelta(minutes=5)
        )
        client.messages.create(
            body=f"[인터리뷰] 인증코드는 {verification_code}입니다.",
            from_=TWILIO_PHONE_NUMBER,
            to=data.platform_data,
        )


@router.post("/find/verification")
async def verify_code(data: VerifyCode, db: Session = Depends(get_db)) -> dict:
    if await DB_VERIFICATION_CODE.get(f"{data.email}") != data.code:
        raise not_verification_exception()
    user = db.query(User).filter(User.email == data.email).first()
    return {"username": user.username}
