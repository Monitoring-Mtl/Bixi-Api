from abc import ABC, abstractmethod
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorCollection


class Cache(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value, ttl: int) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass


class MongoDBCache(Cache):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def set(self, key: str, value, ttl: int) -> None:
        await self.collection.update_one(
            {"_id": key},
            {"$set": {"value": value, "createdAt": datetime.now(timezone.utc)}},
            upsert=True,
        )
        await self.collection.create_index("createdAt", expireAfterSeconds=ttl)

    async def get(self, key: str):
        result = await self.collection.find_one({"_id": key})
        return result["value"] if result else None

    async def delete(self, key: str) -> None:
        await self.collection.delete_one({"_id": key})
