from constants import ATLAS_URI, MONGO_DATABASE_NAME
from controller import TripController
from motor.motor_asyncio import AsyncIOMotorClient
from repository import TripRepository

db = AsyncIOMotorClient(ATLAS_URI)[MONGO_DATABASE_NAME]
repository = TripRepository(db)
controller = TripController(repository)


async def get_controller():
    return controller
