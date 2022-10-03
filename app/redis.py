import aioredis

from app.config import REDIS_HOST

REDIS_DB = {
    "VERIFICATION_CODE": 0,
}


def get_redis(db: str):
    return aioredis.from_url(
        REDIS_HOST,
        encoding="utf-8",
        decode_responses=True,
        db=REDIS_DB[db],
    )


DB_VERIFICATION_CODE = get_redis("VERIFICATION_CODE")
