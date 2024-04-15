import constants
from cache import MongoDBCache
from controller import Controller
from fastapi import FastAPI
from mangum import Mangum
from motor.motor_asyncio import AsyncIOMotorClient
from repository import StationRepository, TripRepository
from routes import health_router, stations_router, trip_router, use_controller

mongo_client = AsyncIOMotorClient(constants.ATLAS_URI)
db = mongo_client[constants.MONGO_DATABASE_NAME]
trip_repository = TripRepository(db[constants.BIXI_TRIP_COLLECTION])
station_repository = StationRepository(db[constants.BIXI_LOCATION_COLLECTION])
cache = MongoDBCache(db[constants.CACHE_COLLECTION])
controller = Controller(trip_repository, station_repository, cache)
use_controller(controller)

app = FastAPI(root_path=f"/{constants.STAGE_NAME}")
app.include_router(health_router)
app.include_router(trip_router)
app.include_router(stations_router)
handler = Mangum(app)
