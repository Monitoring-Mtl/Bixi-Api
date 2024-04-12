from unittest.mock import AsyncMock

import pytest

from trips.cache import MongoDBCache


@pytest.fixture
def collection_mock():
    collection = AsyncMock()
    return collection


@pytest.fixture
def mongo_db_cache(collection_mock):
    return MongoDBCache(collection=collection_mock)


@pytest.mark.asyncio
async def test_set_inserts_correctly(mongo_db_cache, collection_mock):
    await mongo_db_cache.set("test_key", "test_value", 3600)
    collection_mock.update_one.assert_called_once()
    args, kwargs = collection_mock.update_one.call_args
    assert args[0] == {"_id": "test_key"}
    assert "value" in args[1]["$set"]
    assert kwargs == {"upsert": True}
    collection_mock.create_index.assert_called_once_with(
        "createdAt", expireAfterSeconds=3600
    )


@pytest.mark.asyncio
async def test_get_returns_value(mongo_db_cache, collection_mock):
    collection_mock.find_one.return_value = {"_id": "test_key", "value": "test_value"}
    result = await mongo_db_cache.get("test_key")
    assert result == "test_value"
    collection_mock.find_one.assert_called_once_with({"_id": "test_key"})


@pytest.mark.asyncio
async def test_get_returns_none_if_not_found(mongo_db_cache, collection_mock):
    collection_mock.find_one.return_value = None
    result = await mongo_db_cache.get("nonexistent_key")
    assert result is None


@pytest.mark.asyncio
async def test_delete_removes_key(mongo_db_cache, collection_mock):
    await mongo_db_cache.delete("test_key")
    collection_mock.delete_one.assert_called_once_with({"_id": "test_key"})
