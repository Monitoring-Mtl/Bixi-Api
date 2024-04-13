from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from trips.constants import MAX_INT64, YEAR
from trips.models import TripAverageModel, TripModel
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
    controller.get_average_duration = AsyncMock(
        return_value=TripAverageModel(averageDuration=250.0, tripCount=100)
    )
    use_controller(controller)
    return controller


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_get_average_duration(client, mock_controller):
    response = client.get(f"/trips/duration/average?minStartTime=0&maxStartTime={YEAR}")
    assert response.status_code == 200
    assert response.json() == {"averageDuration": 250.0, "tripCount": 100}


def test_get_average_duration_bad_range(client, mock_controller):
    response = client.get(
        "/trips/duration/average?minStartTime=31536000000&maxStartTime=0"
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "start_time_max_ms must be greater than start_time_min_ms"
    )


def test_get_average_duration_too_long_range(client, mock_controller):
    response = client.get(
        f"/trips/duration/average?minStartTime=0&maxStartTime={YEAR+1}"
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "the range must not exceed 1 year"


def test_get_average_duration_negative_min_time(client, mock_controller):
    response = client.get("/trips/duration/average?minStartTime=-1")
    assert response.status_code == 422


def test_get_average_duration_non_integer_time(client, mock_controller):
    response = client.get("/trips/duration/average?minStartTime=abc")
    assert response.status_code == 422


def test_get_average_duration_excessive_max_time(client, mock_controller):
    response = client.get(f"/trips/duration/average?maxStartTime={MAX_INT64+1}")
    assert response.status_code == 422


def test_get_average_duration_missing_parameters(client, mock_controller):
    response = client.get("/trips/duration/average")
    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_minimum_start_time(client, mock_controller):
    mock_controller.get_minimum_start_time = AsyncMock(
        return_value=TripModel(startTimeMs=1609459200000)
    )
    response = client.get("/trips/time/start/minimum")
    assert response.status_code == 200
    expected_response = TripModel(startTimeMs=1609459200000).model_dump()
    print(response.json())
    assert response.json() == expected_response


def test_get_maximum_start_time(client, mock_controller):
    mock_controller.get_maximum_start_time = AsyncMock(
        return_value=TripModel(startTimeMs=1704062400000)
    )
    response = client.get("/trips/time/start/maximum")
    assert response.status_code == 200
    expected_response = TripModel(startTimeMs=1704062400000).model_dump()
    assert response.json() == expected_response


def test_get_minimum_end_time(client, mock_controller):
    mock_controller.get_minimum_end_time = AsyncMock(
        return_value=TripModel(endTimeMs=1609459300000)
    )
    response = client.get("/trips/time/end/minimum")
    assert response.status_code == 200
    expected_response = TripModel(endTimeMs=1609459300000).model_dump()
    assert response.json() == expected_response


def test_get_maximum_end_time(client, mock_controller):
    mock_controller.get_maximum_end_time = AsyncMock(
        return_value=TripModel(endTimeMs=1704062500000)
    )
    response = client.get("/trips/time/end/maximum")
    assert response.status_code == 200
    expected_response = TripModel(endTimeMs=1704062500000).model_dump()
    assert response.json() == expected_response
