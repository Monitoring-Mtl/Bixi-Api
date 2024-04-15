from unittest.mock import AsyncMock

import pytest
from motor.motor_asyncio import AsyncIOMotorCollection

from trips.repository import StationRepository, TripRepository


@pytest.fixture
def mock_trip_collection():
    return AsyncMock(spec=AsyncIOMotorCollection)


@pytest.fixture
def mock_station_collection():
    return AsyncMock(spec=AsyncIOMotorCollection)


@pytest.fixture
def trip_repo(mock_trip_collection):
    return TripRepository(mock_trip_collection)


@pytest.fixture
def station_repo(mock_station_collection):
    return StationRepository(mock_station_collection)


@pytest.mark.asyncio
async def test_get_average_duration_empty_results(trip_repo, mock_trip_collection):
    mock_trip_collection.aggregate.return_value.to_list = AsyncMock(return_value=[])
    min_start, max_start = 0, 86400000
    result = await trip_repo.get_average_duration(min_start, max_start)
    assert result == {"averageDuration": None, "tripCount": 0}


@pytest.mark.asyncio
async def test_get_average_duration(trip_repo, mock_trip_collection):
    mock_trip_collection.aggregate.return_value.to_list = AsyncMock(
        side_effect=[
            [{"sumDuration": 1000, "countTrips": 10}],
            [{"sumDuration": 500, "countTrips": 5}],
            [],
        ]
    )
    min_start, max_start = 0, 3 * 86400000
    result = await trip_repo.get_average_duration(min_start, max_start)
    assert result == {"averageDuration": 100, "tripCount": 15}


@pytest.mark.asyncio
async def test_get_durations_no_results(trip_repo, mock_trip_collection):
    mock_trip_collection.aggregate.return_value.to_list = AsyncMock(return_value=[])
    result = await trip_repo.get_durations(0, 86400000)
    assert result == {}


@pytest.mark.asyncio
async def test_get_durations(trip_repo, mock_trip_collection):
    minStartTimeMs, maxStartTimeMs = 0, 86400000
    expected_result = {"_id": None, "sumDuration": 500, "countTrips": 5}
    mock_trip_collection.aggregate.return_value.to_list = AsyncMock(
        return_value=[expected_result]
    )
    await trip_repo.get_durations(minStartTimeMs, maxStartTimeMs)
    mock_trip_collection.aggregate.assert_called_once_with(
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
async def test_get_minimum_start_time(trip_repo: TripRepository, mock_trip_collection):
    mock_trip_collection.find_one = AsyncMock(
        return_value={"startTimeMs": 1609459200000}
    )
    result = await trip_repo.get_minimum_start_time()
    assert result == {"startTimeMs": 1609459200000}
    mock_trip_collection.find_one.assert_called_with(
        {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", 1)]
    )


@pytest.mark.asyncio
async def test_get_maximum_start_time(trip_repo: TripRepository, mock_trip_collection):
    mock_trip_collection.find_one = AsyncMock(
        return_value={"startTimeMs": 1612137600000}
    )
    result = await trip_repo.get_maximum_start_time()
    assert result == {"startTimeMs": 1612137600000}
    mock_trip_collection.find_one.assert_called_with(
        {"startTimeMs": {"$ne": None}}, sort=[("startTimeMs", -1)]
    )


@pytest.mark.asyncio
async def test_get_minimum_end_time(trip_repo: TripRepository, mock_trip_collection):
    mock_trip_collection.find_one = AsyncMock(return_value={"endTimeMs": 1609459201000})
    result = await trip_repo.get_minimum_end_time()
    assert result == {"endTimeMs": 1609459201000}
    mock_trip_collection.find_one.assert_called_with(
        {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", 1)]
    )


@pytest.mark.asyncio
async def test_get_maximum_end_time(trip_repo: TripRepository, mock_trip_collection):
    mock_trip_collection.find_one = AsyncMock(return_value={"endTimeMs": 1612137601000})
    result = await trip_repo.get_maximum_end_time()
    assert result == {"endTimeMs": 1612137601000}
    mock_trip_collection.find_one.assert_called_with(
        {"endTimeMs": {"$ne": None}}, sort=[("endTimeMs", -1)]
    )


@pytest.mark.asyncio
async def test_get_minimum_duration(trip_repo: TripRepository, mock_trip_collection):
    mock_trip_collection.find_one = AsyncMock(return_value={"durationMs": 60000})
    result = await trip_repo.get_minimum_duration()
    assert result == {"durationMs": 60000}
    mock_trip_collection.find_one.assert_called_with(
        {"durationMs": {"$ne": None}}, sort=[("durationMs", 1)], limit=1
    )


@pytest.mark.asyncio
async def test_get_maximum_duration(trip_repo: TripRepository, mock_trip_collection):
    mock_trip_collection.find_one = AsyncMock(return_value={"durationMs": 1200000})
    result = await trip_repo.get_maximum_duration()
    assert result == {"durationMs": 1200000}
    mock_trip_collection.find_one.assert_called_with(
        {"durationMs": {"$ne": None}}, sort=[("durationMs", -1)], limit=1
    )


@pytest.mark.asyncio
async def test_get_arrondissements(station_repo, mock_station_collection):
    mock_station_collection.aggregate.return_value.to_list = AsyncMock(
        return_value=[{"_id": "10"}, {"_id": "11"}, {"_id": "12"}]
    )
    arrondissements = await station_repo.get_arrondissements()
    assert arrondissements == ["10", "11", "12"]
    mock_station_collection.aggregate.assert_called_once_with(
        [
            {"$match": {"arrondissement": {"$exists": True, "$ne": None}}},
            {"$group": {"_id": "$arrondissement"}},
            {"$sort": {"_id": 1}},
        ]
    )


@pytest.mark.asyncio
async def test_get_stations_by_name(station_repo, mock_station_collection):
    station_name = "Station1"
    mock_station_collection.find.return_value.sort.return_value.to_list = AsyncMock(
        return_value=[{"_id": station_name, "location": "Location1"}]
    )
    stations = await station_repo.get_stations_by_name(station_name)
    assert stations == [{"_id": station_name, "location": "Location1"}]
    mock_station_collection.find.assert_called_once_with({"_id": station_name})
    mock_station_collection.find.return_value.sort.assert_called_once_with("_id", 1)


@pytest.mark.asyncio
async def test_get_station_by_arrondissement(station_repo, mock_station_collection):
    arrondissement = "11"
    mock_station_collection.find.return_value.sort.return_value.to_list = AsyncMock(
        return_value=[{"_id": "Station1", "arrondissement": arrondissement}]
    )
    stations = await station_repo.get_station_by_arrondissement(arrondissement)
    assert stations == [{"_id": "Station1", "arrondissement": arrondissement}]
    mock_station_collection.find.assert_called_once_with(
        {"arrondissement": arrondissement}
    )
    mock_station_collection.find.return_value.sort.assert_called_once_with("_id", 1)


@pytest.mark.asyncio
async def test_get_stations(station_repo, mock_station_collection):
    mock_station_collection.find.return_value.sort.return_value.to_list = AsyncMock(
        return_value=[{"_id": "Station1"}, {"_id": "Station2"}]
    )
    stations = await station_repo.get_stations()
    assert stations == [{"_id": "Station1"}, {"_id": "Station2"}]
    mock_station_collection.find.assert_called_once_with({})
    mock_station_collection.find.return_value.sort.assert_called_once_with("_id", 1)
