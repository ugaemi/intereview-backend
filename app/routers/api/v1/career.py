from datetime import datetime
from typing import List

import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import COMPANY_SEARCH_API_ENDPOINT, COMPANY_OPEN_API_KEY
from app.database import get_db
from app.models.accounts import User
from app.models.career import UserCareer
from app.routers.api.v1.accounts import get_current_user
from app.schemas.career import SimpleCareer

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
    response = requests.get(
        f"{COMPANY_SEARCH_API_ENDPOINT}?serviceKey={COMPANY_OPEN_API_KEY}&pageNo={page}"
        f"&numOfRows=10&resultType=json&corpNm={keyword}&basDt={datetime.now().strftime('%Y%m%d')}",
        verify=False,
    )
    if response.status_code == 200:
        result = response.json()
        print(result)
