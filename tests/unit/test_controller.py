from unittest.mock import AsyncMock

import pytest

from trips.controller import Controller


@pytest.fixture
def mock_trip_repository():
    return AsyncMock()


@pytest.fixture
def mock_station_repository():
    return AsyncMock()


@pytest.fixture
def mock_cache():
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock()
    return mock


@pytest.fixture
def trip_controller(mock_trip_repository, mock_station_repository, mock_cache):
    return Controller(mock_trip_repository, mock_station_repository, mock_cache)


@pytest.mark.asyncio
async def test_get_average_duration(trip_controller, mock_trip_repository, mock_cache):
    minStartTimeMs = 1609459200000
    maxStartTimeMs = 1609545600000
    expected = {"trips": 42}
    mock_trip_repository.get_average_duration.return_value = expected
    result = await trip_controller.get_average_duration(minStartTimeMs, maxStartTimeMs)
    assert result == expected
    mock_trip_repository.get_average_duration.assert_awaited_once_with(
        minStartTimeMs, maxStartTimeMs
    )
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_minimum_start_time(
    trip_controller, mock_trip_repository, mock_cache
):
    expected = 1609459200000
    mock_trip_repository.get_minimum_start_time.return_value = expected
    result = await trip_controller.get_minimum_start_time()
    assert result == expected
    mock_trip_repository.get_minimum_start_time.assert_awaited_once()
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_maximum_start_time(
    trip_controller, mock_trip_repository, mock_cache
):
    expected = 1609545600000
    mock_trip_repository.get_maximum_start_time.return_value = expected
    result = await trip_controller.get_maximum_start_time()
    assert result == expected
    mock_trip_repository.get_maximum_start_time.assert_awaited_once()
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_minimum_end_time(trip_controller, mock_trip_repository, mock_cache):
    expected = 1609459200000
    mock_trip_repository.get_minimum_end_time.return_value = expected
    result = await trip_controller.get_minimum_end_time()
    assert result == expected
    mock_trip_repository.get_minimum_end_time.assert_awaited_once()
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_maximum_end_time(trip_controller, mock_trip_repository, mock_cache):
    expected = 1609545600000
    mock_trip_repository.get_maximum_end_time.return_value = expected
    result = await trip_controller.get_maximum_end_time()
    assert result == expected
    mock_trip_repository.get_maximum_end_time.assert_awaited_once()
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()


@pytest.mark.asyncio
async def test_use_cache_hit(trip_controller, mock_cache, mock_trip_repository):
    mock_cache.get = AsyncMock(return_value={"cached": "result"})
    result = await trip_controller.get_average_duration(1609459200000, 1609545600000)
    assert result == {"cached": "result"}
    mock_cache.get.assert_awaited_once()
    mock_trip_repository.get_average_duration.assert_not_awaited()


@pytest.mark.asyncio
async def test_use_cache_miss(trip_controller, mock_cache, mock_trip_repository):
    mock_cache.get = AsyncMock(return_value=None)
    mock_trip_repository.get_average_duration = AsyncMock(return_value={"trips": 42})
    result = await trip_controller.get_average_duration(1609459200000, 1609545600000)
    assert result == {"trips": 42}
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()
    mock_trip_repository.get_average_duration.assert_awaited_once_with(
        1609459200000, 1609545600000
    )


@pytest.mark.asyncio
async def test_get_arrondissements(
    trip_controller, mock_station_repository, mock_cache
):
    expected = ["Montreal 1", "Montreal 2", "Montreal 3"]
    mock_station_repository.get_arrondissements.return_value = expected
    result = await trip_controller.get_arrondissements()
    assert result == expected
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()
    mock_station_repository.get_arrondissements.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_stations_by_name(
    trip_controller, mock_station_repository, mock_cache
):
    name = "Louvre"
    expected = [{"name": "Louvre", "arrondissement": "Montreal 1"}]
    mock_station_repository.get_stations_by_name.return_value = expected
    result = await trip_controller.get_stations(name=name, arrondissement=None)
    assert result == expected
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()
    mock_station_repository.get_stations_by_name.assert_awaited_once_with(name)


@pytest.mark.asyncio
async def test_get_station_by_arrondissement(
    trip_controller, mock_station_repository, mock_cache
):
    arrondissement = "Montreal 1"
    expected = [{"name": "Louvre", "arrondissement": "Montreal 1"}]
    mock_station_repository.get_station_by_arrondissement.return_value = expected
    result = await trip_controller.get_stations(
        name=None, arrondissement=arrondissement
    )
    assert result == expected
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()
    mock_station_repository.get_station_by_arrondissement.assert_awaited_once_with(
        arrondissement
    )


@pytest.mark.asyncio
async def test_get_stations_no_filters(
    trip_controller, mock_station_repository, mock_cache
):
    expected = [
        {"name": "Louvre", "arrondissement": "Montreal 1"},
        {"name": "Eiffel Tower", "arrondissement": "Montreal 7"},
    ]
    mock_station_repository.get_stations.return_value = expected
    result = await trip_controller.get_stations(name=None, arrondissement=None)
    assert result == expected
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()
    mock_station_repository.get_stations.assert_awaited_once()
