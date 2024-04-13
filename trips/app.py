from cache import MongoDBCache
from constants import (
    ATLAS_URI,
    BIXI_TRIP_COLLECTION,
    CACHE_COLLECTION,
    MONGO_DATABASE_NAME,
    STAGE_NAME,
)
from controller import TripController
from fastapi import FastAPI
from mangum import Mangum
from motor.motor_asyncio import AsyncIOMotorClient
from repository import TripRepository
from routes import health_router, trip_router, use_controller

mongo_client = AsyncIOMotorClient(ATLAS_URI)
db = mongo_client[MONGO_DATABASE_NAME]
repository = TripRepository(db[BIXI_TRIP_COLLECTION])
cache = MongoDBCache(db[CACHE_COLLECTION])
controller = TripController(repository, cache)
use_controller(controller)

app = FastAPI(root_path=f"/{STAGE_NAME}")
app.include_router(health_router)
app.include_router(trip_router)
handler = Mangum(app)
