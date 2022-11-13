import certifi
from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine


class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(
            config("MONGO_DB_HOST"), tlsCAFile=certifi.where()
        )
        self.engine = AIOEngine(client=self.client, database=config("MONGO_DB_NAME"))
        print("MongoDB와 성공적으로 연결이 되었습니다.")

    def close(self):
        self.client.close()
        print("MongoDB와 성공적으로 연결이 해제되었습니다.")


mongodb = MongoDB()
