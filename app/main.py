from fastapi import FastAPI, Request, Response

from app.database import engine, Base, SessionLocal
from app.routers import accounts

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(accounts.router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next) -> Response:
    response = Response("서버 에러", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}
