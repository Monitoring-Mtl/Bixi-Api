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

    async def get_average_duration(
        self,
        minStartTimeMs: int,
        maxStartTimeMs: int,
        startStationName: str | None = None,
        endStationName: str | None = None,
    ):
        segments = create_segments(minStartTimeMs, maxStartTimeMs)
        tasks = [
            self.aggregate_duration(start, end, startStationName, endStationName)
            for start, end in segments
        ]
        results = await gather(*tasks)
        total_duration = sum(r["sumDuration"] for r in results if "sumDuration" in r)
        total_trips = sum(r["countTrips"] for r in results if "countTrips" in r)
        print("Calculating average duration")
        return {
            "averageDuration": total_duration / total_trips if total_trips else None,
            "tripCount": total_trips,
        }

    async def aggregate_duration(
        self, minStartTimeMs, maxStartTimeMs, startStationName, endStationName
    ):
        filter_criteria = {
            "startTimeMs": {"$gt": minStartTimeMs, "$lte": maxStartTimeMs},
            "durationMs": {"$ne": None},
        }
        if startStationName:
            filter_criteria["startStationName"] = startStationName
        if endStationName:
            filter_criteria["endStationName"] = endStationName
        aggregation_pipeline = [
            {"$match": filter_criteria},
            {
                "$group": {
                    "_id": None,
                    "sumDuration": {"$sum": "$durationMs"},
                    "countTrips": {"$count": {}},
                }
            },
        ]
        cursor = self.collection.aggregate(aggregation_pipeline)
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


class StationRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_arrondissements(self):
        pipeline = [
            {"$match": {"arrondissement": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": "$arrondissement"}},
            {"$sort": {"_id": 1}},
        ]
        cursor = self.collection.aggregate(pipeline)
        return [doc["_id"] for doc in await cursor.to_list(length=None)]

    async def get_stations_by_name(self, name: str):
        query = {"_id": name}
        cursor = self.collection.find(query).sort("_id", 1)
        return await cursor.to_list(length=None)

    async def get_station_by_arrondissement(self, arrondissement: str):
        query = {"arrondissement": arrondissement}
        cursor = self.collection.find(query).sort("_id", 1)
        return await cursor.to_list(length=None)

    async def get_stations(self):
        cursor = self.collection.find({}).sort("_id", 1)
        return await cursor.to_list(length=None)
