from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY
from app.database import get_db
from app.enums.accounts import Platform
from app.exceptions import (
    token_exception,
    get_user_exception,
    username_exist_exception,
    not_match_exception,
)
from app.models.accounts import User
from app.schemas.accounts import FindUsername, CreateUser
from app.services.accounts import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    oauth2_bearer,
)

router = APIRouter(
    prefix="/api/v1/accounts",
    tags=["accounts"],
)


@router.post("/")
async def create_new_user(data: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first() is not None:
        raise username_exist_exception()
    create_user_model = User()
    create_user_model.email = data.email
    create_user_model.username = data.username
    create_user_model.name = data.name
    create_user_model.password = get_password_hash(data.password)
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
        print(payload)
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
    else:
        user = db.query(User).filter(User.phone == data.platform_data).first()
        if user is None or user.name != data.name:
            raise not_match_exception()
