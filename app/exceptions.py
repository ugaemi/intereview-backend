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


def username_exist_exception():
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="이미 존재하는 아이디입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def not_match_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="일치하는 정보가 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def not_verification():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="유효하지 않은 코드입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
