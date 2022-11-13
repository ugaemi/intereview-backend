from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app.mongodb import mongodb
from app.routers.api.v1 import accounts, career

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(accounts.router)
app.include_router(career.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
