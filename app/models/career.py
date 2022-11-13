from odmantic import Model
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func, Date
from sqlalchemy.orm import relationship, backref

from app.database import Base


class CompanyBasicInfo(Model):
    name: str
    corporate_registration_number: str
    company_registration_number: str
    address: str
    zip_code: str
    homepage_url: str
    phone: str
    base_date: str
    keyword: str

    class Config:
        collection = "companies"


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50))
    corporate_registration_number = Column(String(length=20), nullable=True)
    company_registration_number = Column(String(length=20), nullable=True)
    address = Column(String(length=100), nullable=True)
    address_detail = Column(String(length=100), nullable=True)
    zip_code = Column(String(length=10), nullable=True)
    homepage_url = Column(String(length=200), nullable=True)
    phone_country_code = Column(String(length=5), nullable=True)
    phone_national_number = Column(String(length=12), nullable=True)
    logo_url = Column(String(length=200), nullable=True)
    created_datetime = Column(DateTime, default=func.now())
    updated_datetime = Column(
        DateTime, default=func.now(), onupdate=func.current_timestamp()
    )


class UserCareer(Base):
    __tablename__ = "user_career"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref=backref("career", uselist=True))
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", backref=backref("user_career", uselist=True))
    joined_date = Column(Date)
    resignation_date = Column(Date, nullable=True)
    created_datetime = Column(DateTime, default=func.now())
    updated_datetime = Column(
        DateTime, default=func.now(), onupdate=func.current_timestamp()
    )
