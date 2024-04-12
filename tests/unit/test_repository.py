from unittest.mock import AsyncMock

import pytest
from motor.motor_asyncio import AsyncIOMotorCollection

from trips.repository import TripRepository


@pytest.fixture
def mock_collection():
    return AsyncMock(spec=AsyncIOMotorCollection)


@pytest.fixture
def repo(mock_collection):
    return TripRepository(mock_collection)


@pytest.mark.asyncio
async def test_get_trip_stats(repo: TripRepository, mock_collection):
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = [
        {
            "_id": None,
            "averageDuration": 300000,
            "minDuration": 60000,
            "maxDuration": 1200000,
            "stdDevDuration": 150000,
            "tripCount": 100,
        }
    ]
    mock_collection.aggregate.return_value = mock_cursor
    result = await repo.get_trip_stats(1609459200000, 1612137600000)
    assert result == {
        "_id": None,
        "averageDuration": 300000,
        "minDuration": 60000,
        "maxDuration": 1200000,
        "stdDevDuration": 150000,
        "tripCount": 100,
    }

    mock_collection.aggregate.assert_called_once_with(
        [
            {
                "$match": {
                    "startTimeMs": {"$gte": 1609459200000, "$lte": 1612137600000},
                    "durationMs": {"$ne": None},
                }
            },
            {
                "$group": {
                    "_id": None,
                    "averageDuration": {"$avg": "$durationMs"},
                    "minDuration": {"$min": "$durationMs"},
                    "maxDuration": {"$max": "$durationMs"},
                    "stdDevDuration": {"$stdDevPop": "$durationMs"},
                    "tripCount": {"$count": {}},
                }
            },
        ]
    )


@pytest.mark.asyncio
async def test_get_minimum_start_time(repo: TripRepository, mock_collection):
    mock_collection.find_one = AsyncMock(return_value={"startTimeMs": 1609459200000})
    result = await repo.get_minimum_start_time()
    assert result == {"startTimeMs": 1609459200000}
    mock_collection.find_one.assert_called_with(
        {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", 1)]
    )


@pytest.mark.asyncio
async def test_get_maximum_start_time(repo: TripRepository, mock_collection):
    mock_collection.find_one = AsyncMock(return_value={"startTimeMs": 1612137600000})
    result = await repo.get_maximum_start_time()
    assert result == {"startTimeMs": 1612137600000}
    mock_collection.find_one.assert_called_with(
        {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", -1)]
    )


@pytest.mark.asyncio
async def test_get_minimum_end_time(repo: TripRepository, mock_collection):
    mock_collection.find_one = AsyncMock(return_value={"endTimeMs": 1609459201000})
    result = await repo.get_minimum_end_time()
    assert result == {"endTimeMs": 1609459201000}
    mock_collection.find_one.assert_called_with(
        {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", 1)]
    )


@pytest.mark.asyncio
async def test_get_maximum_end_time(repo: TripRepository, mock_collection):
    mock_collection.find_one = AsyncMock(return_value={"endTimeMs": 1612137601000})
    result = await repo.get_maximum_end_time()
    assert result == {"endTimeMs": 1612137601000}
    mock_collection.find_one.assert_called_with(
        {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", -1)]
    )


@pytest.mark.asyncio
async def test_get_minimum_duration(repo: TripRepository, mock_collection):
    mock_collection.find_one = AsyncMock(return_value={"durationMs": 60000})
    result = await repo.get_minimum_duration()
    assert result == {"durationMs": 60000}
    mock_collection.find_one.assert_called_with(
        {"durationMs": {"$ne": None}}, sort=[("durationMs", 1)], limit=1
    )


@pytest.mark.asyncio
async def test_get_maximum_duration(repo: TripRepository, mock_collection):
    mock_collection.find_one = AsyncMock(return_value={"durationMs": 1200000})
    result = await repo.get_maximum_duration()
    assert result == {"durationMs": 1200000}
    mock_collection.find_one.assert_called_with(
        {"durationMs": {"$ne": None}}, sort=[("durationMs", -1)], limit=1
    )
