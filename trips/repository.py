from asyncio import gather

from constants import DAY
from motor.motor_asyncio import AsyncIOMotorCollection


def create_segments(minStartTimeMs, maxStartTimeMs, segment_length_ms=DAY):
    return [
        (start, min(start + segment_length_ms - 1, maxStartTimeMs))
        for start in range(minStartTimeMs, maxStartTimeMs, segment_length_ms)
    ]


class TripRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_average_duration(self, minStartTimeMs: int, maxStartTimeMs: int):
        segments = create_segments(minStartTimeMs, maxStartTimeMs)
        tasks = [self.get_durations(start, end) for start, end in segments]
        results = await gather(*tasks)
        total_duration = sum(r["sumDuration"] for r in results if "sumDuration" in r)
        total_trips = sum(r["countTrips"] for r in results if "countTrips" in r)
        print(f"Calculating average duration from {minStartTimeMs} to {maxStartTimeMs}")
        return {
            "averageDuration": total_duration / total_trips if total_trips else None,
            "tripCount": total_trips,
        }

    async def get_durations(self, minStartTimeMs, maxStartTimeMs):
        matching = {
            "$match": {
                "startTimeMs": {"$gt": minStartTimeMs, "$lte": maxStartTimeMs},
                "durationMs": {"$ne": None},
            }
        }
        grouping = {
            "$group": {
                "_id": None,
                "sumDuration": {"$sum": "$durationMs"},
                "countTrips": {"$count": {}},
            }
        }
        cursor = self.collection.aggregate([matching, grouping])
        result = await cursor.to_list(length=1)
        return result[0] if result else {}

    async def get_minimum_start_time(self):
        return await self.collection.find_one(
            {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", 1)]
        )

    async def get_maximum_start_time(self):
        return await self.collection.find_one(
            {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", -1)]
        )

    async def get_minimum_end_time(self):
        return await self.collection.find_one(
            {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", 1)]
        )

    async def get_maximum_end_time(self):
        return await self.collection.find_one(
            {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", -1)]
        )

    async def get_minimum_duration(self):
        return await self.collection.find_one(
            {"durationMs": {"$ne": None}}, sort=[("durationMs", 1)], limit=1
        )

    async def get_maximum_duration(self):
        return await self.collection.find_one(
            {"durationMs": {"$ne": None}}, sort=[("durationMs", -1)], limit=1
        )
