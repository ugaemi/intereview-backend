from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=12), unique=True, index=True)
    password = Column(String(length=20))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, default=func.now())
    joined_datetime = Column(DateTime, default=func.now())
    withdrawal_datetime = Column(DateTime, nullable=True)
    created_datetime = Column(DateTime, default=func.now())
    updated_datetime = Column(
        DateTime, default=func.now(), onupdate=func.current_timestamp()
    )


class UserInfo(Base):
    __tablename__ = "user_infos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("info", uselist=False))
    name = Column(String(length=20))
    email = Column(String(length=50))
    phone_country_code = Column(String(length=5))
    phone_national_number = Column(String(length=12))
    created_datetime = Column(DateTime, default=func.now())
    updated_datetime = Column(
        DateTime, default=func.now(), onupdate=func.current_timestamp()
    )
