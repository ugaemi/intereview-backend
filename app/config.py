from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

MAIL_FROM = config("MAIL_FROM")
MAIL_PASSWORD = config("MAIL_PASSWORD")
MAIL_PORT = 587
MAIL_SERVER = "smtp.gmail.com"
MAIL_FROM_NAME = "intereview"

REDIS_HOST = config("REDIS_HOST")
