from fastapi import HTTPException
from starlette import status


def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="자격 증명에 실패했습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="아이디 혹은 비밀번호가 맞지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
