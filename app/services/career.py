from datetime import datetime
from typing import List

import requests
from dateutil.relativedelta import relativedelta
from decouple import config


class CompanyScraper:
    OPEN_API_KEY = config("COMPANY_OPEN_API_KEY")
    SEARCH_API_ENDPOINT = (
        "https://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getCorpOutline"
    )

    def __init__(self):
        self.base_date = (datetime.now() + relativedelta(days=-7)).strftime("%Y%m%d")

    def search(self, keyword: str, page: int) -> List[dict]:
        response = requests.get(
            f"{self.SEARCH_API_ENDPOINT}?serviceKey={self.OPEN_API_KEY}&pageNo={page}"
            f"&numOfRows=10&resultType=json&corpNm={keyword}&basDt={self.base_date}",
            verify=False,
        )
        if response.status_code == 200:
            result = response.json()
            companies = result["response"]["body"]["items"]["item"]
            return companies
        print(response)
        return []
