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
        detail=[
            {
                "loc": ["body", "username"],
                "msg": "아이디 혹은 비밀번호가 맞지 않습니다.",
                "type": "value_error.unauthorized",
            },
            {
                "loc": ["body", "password"],
                "msg": "아이디 혹은 비밀번호가 맞지 않습니다.",
                "type": "value_error.unauthorized",
            },
        ],
        headers={"WWW-Authenticate": "Bearer"},
    )


def username_exist_exception():
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=[
            {
                "loc": ["body", "username"],
                "msg": "이미 존재하는 아이디입니다.",
                "type": "value_error.conflict",
            }
        ],
    )


def email_exist_exception():
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=[
            {
                "loc": ["body", "email"],
                "msg": "이미 존재하는 이메일입니다.",
                "type": "value_error.conflict",
            }
        ],
    )


def not_match_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="일치하는 정보가 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def not_verification_exception():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="유효하지 않은 코드입니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def invalid_phone_exception():
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="전화번호 형식에 맞지 않습니다.",
    )
