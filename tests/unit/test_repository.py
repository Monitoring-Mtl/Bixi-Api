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
async def test_get_average_duration_empty_results(repo, mock_collection):
    mock_collection.aggregate.return_value.to_list = AsyncMock(return_value=[])
    min_start, max_start = 0, 86400000
    result = await repo.get_average_duration(min_start, max_start)
    assert result == {"averageDuration": None, "tripCount": 0}


@pytest.mark.asyncio
async def test_get_average_duration(repo, mock_collection):
    mock_collection.aggregate.return_value.to_list = AsyncMock(
        side_effect=[
            [{"sumDuration": 1000, "countTrips": 10}],
            [{"sumDuration": 500, "countTrips": 5}],
            []
        ]
    )
    min_start, max_start = 0, 3 * 86400000
    result = await repo.get_average_duration(min_start, max_start)
    assert result == {"averageDuration": 100, "tripCount": 15}


@pytest.mark.asyncio
async def test_get_durations_no_results(repo, mock_collection):
    mock_collection.aggregate.return_value.to_list = AsyncMock(return_value=[])
    result = await repo.get_durations(0, 86400000)
    assert result == {}


@pytest.mark.asyncio
async def test_get_durations(repo, mock_collection):
    minStartTimeMs, maxStartTimeMs = 0, 86400000
    expected_result = {"_id": None, "sumDuration": 500, "countTrips": 5}
    mock_collection.aggregate.return_value.to_list = AsyncMock(
        return_value=[expected_result]
    )
    await repo.get_durations(minStartTimeMs, maxStartTimeMs)
    mock_collection.aggregate.assert_called_once_with(
        [
            {
                "$match": {
                    "startTimeMs": {"$gt": minStartTimeMs, "$lte": maxStartTimeMs},
                    "durationMs": {"$ne": None},
                }
            },
            {
                "$group": {
                    "_id": None,
                    "sumDuration": {"$sum": "$durationMs"},
                    "countTrips": {"$count": {}},
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
