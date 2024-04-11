from cache import MongoDBCache
from constants import ATLAS_URI, CACHE_COLLECTION, MONGO_DATABASE_NAME
from controller import TripController
from motor.motor_asyncio import AsyncIOMotorClient
from repository import TripRepository

mongo_client = AsyncIOMotorClient(ATLAS_URI)
db = mongo_client[MONGO_DATABASE_NAME]
repository = TripRepository(db)
cache_collection = db[CACHE_COLLECTION]
cache = MongoDBCache(cache_collection)
controller = TripController(repository, cache)


async def get_controller():
    return controller
