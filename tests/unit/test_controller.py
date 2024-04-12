from unittest.mock import AsyncMock

import pytest

from trips.controller import TripController


@pytest.fixture
def mock_trip_repository():
    return AsyncMock()


@pytest.fixture
def mock_cache():
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock()
    return mock


@pytest.fixture
def trip_controller(mock_trip_repository, mock_cache):
    return TripController(trip_repository=mock_trip_repository, cache=mock_cache)


@pytest.mark.asyncio
async def test_get_trip_stats(trip_controller, mock_trip_repository, mock_cache):
    minStartTimeMs = 1609459200000
    maxStartTimeMs = 1609545600000
    expected = {"trips": 42}
    mock_trip_repository.get_trip_stats.return_value = expected
    result = await trip_controller.get_trip_stats(minStartTimeMs, maxStartTimeMs)
    assert result == expected
    mock_trip_repository.get_trip_stats.assert_awaited_once_with(
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
    result = await trip_controller.get_trip_stats(1609459200000, 1609545600000)
    assert result == {"cached": "result"}
    mock_cache.get.assert_awaited_once()
    mock_trip_repository.get_trip_stats.assert_not_awaited()


@pytest.mark.asyncio
async def test_use_cache_miss(trip_controller, mock_cache, mock_trip_repository):
    mock_cache.get = AsyncMock(return_value=None)
    mock_trip_repository.get_trip_stats = AsyncMock(return_value={"trips": 42})
    result = await trip_controller.get_trip_stats(1609459200000, 1609545600000)
    assert result == {"trips": 42}
    mock_cache.get.assert_awaited_once()
    mock_cache.set.assert_awaited_once()
    mock_trip_repository.get_trip_stats.assert_awaited_once_with(
        1609459200000, 1609545600000
    )
