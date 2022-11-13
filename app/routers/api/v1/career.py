from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.accounts import User
from app.models.career import UserCareer, CompanyBasicInfo
from app.mongodb import mongodb
from app.routers.api.v1.accounts import get_current_user
from app.schemas.career import SimpleCareer
from app.services.career import CompanyScraper

router = APIRouter(
    prefix="/api/v1/career",
    tags=["career"],
)


@router.get("/", response_model=List[SimpleCareer])
async def get_simple_career(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return db.query(UserCareer).filter(UserCareer.user_id == current_user["id"]).all()


@router.get("/search/company")
async def search_company(keyword: str, page: int):
    if await mongodb.engine.find_one(
        CompanyBasicInfo, CompanyBasicInfo.keyword == keyword
    ):
        return await mongodb.engine.find(
            CompanyBasicInfo, CompanyBasicInfo.keyword == keyword
        )
    company_scraper = CompanyScraper()
    if data := company_scraper.search(keyword, page=page):
        company_basic_infos = []
        for company in data:
            company_basic_info = CompanyBasicInfo(
                keyword=keyword,
                name=company["corpNm"],
                corporate_registration_number=company["crno"],
                company_registration_number=company["bzno"],
                address=company["enpBsadr"],
                zip_code=company["enpOzpno"],
                homepage_url=company["enpHmpgUrl"],
                phone=company["enpTlno"],
                base_date=company_scraper.base_date,
            )
            company_basic_infos.append(company_basic_info)
        await mongodb.engine.save_all(company_basic_infos)
        return company_basic_infos
