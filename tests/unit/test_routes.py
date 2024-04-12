from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from trips.constants import MAX_INT64
from trips.models import TripModel, TripStatModel
from trips.routes import health_router, trip_router, use_controller


@pytest.fixture(scope="module")
def app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(health_router)
    fastapi_app.include_router(trip_router)
    return fastapi_app


@pytest.fixture(scope="module")
def client(app):
    return TestClient(app)


@pytest.fixture(scope="module")
def mock_controller():
    controller = MagicMock()
    controller.get_trip_stats = AsyncMock(
        return_value=TripStatModel(
            averageDuration=250.0,
            minDuration=50,
            maxDuration=600,
            stdDevDuration=125.0,
            tripCount=100,
        )
    )
    use_controller(controller)
    return controller


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_get_trip_stats(client, mock_controller):
    response = client.get(
        "/trips/duration/stats?minStartTime=1609459200000&maxStartTime=1704062400000"
    )
    assert response.status_code == 200
    assert response.json() == {
        "averageDuration": 250.0,
        "minDuration": 50,
        "maxDuration": 600,
        "stdDevDuration": 125.0,
        "tripCount": 100,
    }


def test_get_trip_stats_bad_range(client, mock_controller):
    response = client.get(
        "/trips/duration/stats?minStartTime=1704062400000&maxStartTime=1609459200000"
    )
    assert response.status_code == 400


def test_get_trip_stats_negative_min_time(client, mock_controller):
    response = client.get("/trips/duration/stats?minStartTime=-1")
    assert response.status_code == 422


def test_get_trip_stats_non_integer_time(client, mock_controller):
    response = client.get("/trips/duration/stats?minStartTime=abc")
    assert response.status_code == 422


def test_get_trip_stats_excessive_max_time(client, mock_controller):
    response = client.get(f"/trips/duration/stats?maxStartTime={MAX_INT64+1}")
    assert response.status_code == 422


def test_get_trip_stats_missing_parameters(client, mock_controller):
    response = client.get("/trips/duration/stats")
    assert response.status_code == 200
    assert "averageDuration" in response.json()


def test_get_minimum_start_time(client, mock_controller):
    mock_controller.get_minimum_start_time = AsyncMock(return_value=TripModel(startTimeMs=1609459200000))
    response = client.get("/trips/time/start/minimum")
    assert response.status_code == 200
    expected_response = TripModel(startTimeMs=1609459200000).model_dump()
    print(response.json())
    assert response.json() == expected_response

def test_get_maximum_start_time(client, mock_controller):
    mock_controller.get_maximum_start_time = AsyncMock(return_value=TripModel(startTimeMs=1704062400000))
    response = client.get("/trips/time/start/maximum")
    assert response.status_code == 200
    expected_response = TripModel(startTimeMs=1704062400000).model_dump()
    assert response.json() == expected_response

def test_get_minimum_end_time(client, mock_controller):
    mock_controller.get_minimum_end_time = AsyncMock(return_value=TripModel(endTimeMs=1609459300000))
    response = client.get("/trips/time/end/minimum")
    assert response.status_code == 200
    expected_response = TripModel(endTimeMs=1609459300000).model_dump()
    assert response.json() == expected_response

def test_get_maximum_end_time(client, mock_controller):
    mock_controller.get_maximum_end_time = AsyncMock(return_value=TripModel(endTimeMs=1704062500000))
    response = client.get("/trips/time/end/maximum")
    assert response.status_code == 200
    expected_response = TripModel(endTimeMs=1704062500000).model_dump()
    assert response.json() == expected_response
