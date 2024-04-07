from constants import BIXI_TRIP_COLLECTION
from motor.motor_asyncio import AsyncIOMotorDatabase


class TripRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_trip_stats(self, minStartTimeMs: int, maxStartTimeMs: int) -> dict:
        matching = {
            "$match": {
                "startTimeMs": {"$gte": minStartTimeMs, "$lte": maxStartTimeMs},
                "durationMs": {"$ne": None},
            }
        }
        grouping = {
            "$group": {
                "_id": None,
                "averageDuration": {"$avg": "$durationMs"},
                "minDuration": {"$min": "$durationMs"},
                "maxDuration": {"$max": "$durationMs"},
                "stdDevDuration": {"$stdDevPop": "$durationMs"},
                "tripCount": {"$count": {}},
            }
        }
        cursor = self.db[BIXI_TRIP_COLLECTION].aggregate([matching, grouping])
        result = await cursor.to_list(length=1)
        if result:
            return result[0]
        return {}

    async def get_minimum_start_time(self):
        return await self.db[BIXI_TRIP_COLLECTION].find_one(
            {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", 1)]
        )

    async def get_maximum_start_time(self):
        return await self.db[BIXI_TRIP_COLLECTION].find_one(
            {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", -1)]
        )

    async def get_minimum_end_time(self):
        return await self.db[BIXI_TRIP_COLLECTION].find_one(
            {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", 1)]
        )

    async def get_maximum_end_time(self):
        return await self.db[BIXI_TRIP_COLLECTION].find_one(
            {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", -1)]
        )

    async def get_minimum_duration(self):
        return await self.db[BIXI_TRIP_COLLECTION].find_one(
            {"durationMs": {"$ne": None}}, sort=[("durationMs", 1)], limit=1
        )

    async def get_maximum_duration(self):
        return await self.db[BIXI_TRIP_COLLECTION].find_one(
            {"durationMs": {"$ne": None}}, sort=[("durationMs", -1)], limit=1
        )
