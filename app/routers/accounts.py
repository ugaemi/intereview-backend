from datetime import timedelta

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import token_exception
from app.models.accounts import User
from app.schemas.accounts import CreateUser
from app.services.accounts import (
    get_password_hash,
    authenticate_user,
    create_access_token,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = User()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.name = create_user.name
    create_user_model.password = get_password_hash(create_user.password)
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
