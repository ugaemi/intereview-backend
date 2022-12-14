import datetime

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_mail import MessageSchema, FastMail
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY, TWILIO_PHONE_NUMBER, DASHBOARD_HOST
from app.database import get_db
from app.exceptions import (
    token_exception,
    get_user_exception,
    not_match_exception,
    not_verification_exception,
    invalid_phone_exception,
    username_exist_exception,
)
from app.mail import mail_conf
from app.models.accounts import User, UserInfo
from app.redis import DB_VERIFICATION_CODE
from app.schemas.accounts import (
    FindUsername,
    CreateUser,
    VerifyCodeForUsername,
    GetResetPasswordLink,
    ResetPassword,
)
from app.services.accounts import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    oauth2_bearer,
    generate_verification_code,
    get_valid_phone,
    create_refresh_token,
)
from app.twilio import client
from app.utils.security import OAuth2RefreshRequestForm

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=["accounts"],
)


@router.post("/")
async def create_new_user(data: CreateUser, db: Session = Depends(get_db)):
    valid_phone = get_valid_phone(data.phone)
    try:
        user = User(
            username=data.username,
            password=get_password_hash(data.password),
        )
        db.add(user)
        db.commit()
    except Exception:
        db.rollback()
        raise username_exist_exception()
    user = db.query(User).filter(User.username == user.username).first()
    user_info = UserInfo(
        name=data.name,
        phone_country_code=valid_phone.country_code,
        phone_national_number=valid_phone.national_number,
        user=user,
    )
    db.add(user_info)
    db.commit()


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    access_token = create_access_token(user.username, user.id)
    refresh_token = create_refresh_token(user.username, user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "username": user.username,
        "id": user.id,
    }


@router.post("/token/refresh")
async def refresh_access_token(form_data: OAuth2RefreshRequestForm = Depends()):
    try:
        payload = jwt.decode(
            form_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        access_token = create_access_token(username, user_id)
        return {
            "access_token": access_token,
            "refresh_token": form_data.refresh_token,
            "token_type": "Bearer",
            "username": username,
            "id": user_id,
        }
    except JWTError:
        raise get_user_exception()


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


@router.get("/")
async def get_user_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise not_match_exception()
    return {"joined_date": datetime.datetime.strftime(user.joined_datetime, "%Y-%m-%d")}


@router.post("/withdraw")
async def withdraw_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user["id"]).first()
    if not user:
        raise not_match_exception()
    user.is_active = False
    user.withdrawal_datetime = datetime.datetime.now()
    db.add(user)
    db.commit()


@router.post("/find/username")
async def find_username(data: FindUsername, db: Session = Depends(get_db)):
    valid_phone = get_valid_phone(data.phone)
    if not valid_phone:
        raise invalid_phone_exception()
    user_info = (
        db.query(UserInfo)
        .filter(
            UserInfo.phone_country_code == str(valid_phone.country_code),
            UserInfo.phone_national_number == str(valid_phone.national_number),
        )
        .first()
    )
    if user_info is None or user_info.name != data.name:
        raise not_match_exception()
    verification_code = generate_verification_code(6)
    await DB_VERIFICATION_CODE.set(
        data.phone, verification_code, datetime.timedelta(minutes=5)
    )
    client.messages.create(
        body=f"[????????????] ??????????????? {verification_code}?????????.",
        from_=TWILIO_PHONE_NUMBER,
        to=data.phone,
    )


@router.post("/find/username/verification")
async def verify_code_for_username(
    data: VerifyCodeForUsername, db: Session = Depends(get_db)
) -> dict:
    if await DB_VERIFICATION_CODE.get(f"{data.phone}") != data.code:
        raise not_verification_exception()
    valid_phone = get_valid_phone(data.phone)
    user_info = (
        db.query(UserInfo)
        .filter(
            UserInfo.phone_country_code == str(valid_phone.country_code),
            UserInfo.phone_national_number == str(valid_phone.national_number),
        )
        .first()
    )
    return {"username": user_info.user.username}


@router.post("/reset/password/link")
async def get_reset_password_link(
    data: GetResetPasswordLink, db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .join(UserInfo, User.id == UserInfo.user_id)
        .filter(User.username == data.username, UserInfo.name == data.name)
        .first()
    )
    if not user:
        raise not_match_exception()
    verification_code = generate_verification_code(6)
    message = MessageSchema(
        subject="[????????????] ???????????? ????????? ????????? ??????????????????.",
        recipients=[user.username],
        template_body={
            "link": f"{DASHBOARD_HOST}/accounts/find/password/reset?username={user.username}&code={verification_code}",
        },
    )
    fm = FastMail(mail_conf)
    await DB_VERIFICATION_CODE.set(
        user.username, verification_code, datetime.timedelta(minutes=10)
    )
    await fm.send_message(message, template_name="accounts/reset_password.html")


@router.post("/reset/password")
async def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    if await DB_VERIFICATION_CODE.get(f"{data.username}") != data.code:
        raise not_verification_exception()
    user = db.query(User).filter(User.username == data.username).first()
    user.password = get_password_hash(data.password)
    db.add(user)
    db.commit()


@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    user_info = (
        db.query(UserInfo).filter(UserInfo.user_id == current_user["id"]).first()
    )
    if not user_info:
        raise not_match_exception()
    return {
        "name": user_info.name,
        "email": user_info.user.username,
        "phone": user_info.phone_country_code + user_info.phone_national_number,
    }
