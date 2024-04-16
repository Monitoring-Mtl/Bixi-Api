from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from trips.constants import MAX_INT64, YEAR
from trips.models import StationModel, TripAverageModel, TripModel
from trips.routes import health_router, stations_router, trip_router, use_controller


@pytest.fixture(scope="module")
def app():
    fastapi_app = FastAPI()
    fastapi_app.include_router(health_router)
    fastapi_app.include_router(trip_router)
    fastapi_app.include_router(stations_router)
    return fastapi_app


@pytest.fixture(scope="module")
def client(app):
    return TestClient(app)


@pytest.fixture(scope="module")
def mock_controller():
    controller = MagicMock()
    controller.get_average_duration = AsyncMock()
    use_controller(controller)
    return controller


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_get_average_duration(client, mock_controller):
    mock_controller.get_average_duration = AsyncMock(
        return_value=TripAverageModel(averageDuration=250.0, tripCount=100)
    )
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


def test_get_average_duration_with_station_names(client, mock_controller):
    response = client.get(
        f"/trips/duration/average?minStartTime=0&maxStartTime={YEAR}&startStationName=StationA&endStationName=StationB"
    )
    print(response.text)
    assert response.status_code == 200
    assert "averageDuration" in response.json() and "tripCount" in response.json()


def test_get_average_duration_only_start_station_name(client, mock_controller):
    response = client.get(
        f"/trips/duration/average?minStartTime=0&maxStartTime={YEAR}&startStationName=StationA"
    )
    assert response.status_code == 200
    assert "averageDuration" in response.json() and "tripCount" in response.json()


def test_get_average_duration_only_end_station_name(client, mock_controller):
    response = client.get(
        f"/trips/duration/average?minStartTime=0&maxStartTime={YEAR}&endStationName=StationB"
    )
    assert response.status_code == 200
    assert "averageDuration" in response.json() and "tripCount" in response.json()


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


def test_get_arrondissements(client, mock_controller):
    mock_controller.get_arrondissements = AsyncMock(
        return_value=["Montreal 1", "Montreal 2", "Montreal 3"]
    )
    response = client.get("/stations/arrondissements")
    assert response.status_code == 200
    assert response.json() == ["Montreal 1", "Montreal 2", "Montreal 3"]


def test_get_stations_by_arrondissement_with_name(client, mock_controller):
    station_instance = StationModel(id=1, name="Station 1", arrondissement="Montreal 1")
    mock_controller.get_stations = AsyncMock(return_value=[station_instance])
    response = client.get("/stations?name=Station 1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Station 1",
            "arrondissement": "Montreal 1",
            "latitude": None,
            "longitude": None,
        }
    ]


def test_get_stations_by_arrondissement_with_arrondissement(client, mock_controller):
    station_instance = StationModel(id=1, name="Station 2", arrondissement="Montreal 2")
    mock_controller.get_stations = AsyncMock(return_value=[station_instance])
    response = client.get("/stations?arrondissement=Montreal 2")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Station 2",
            "arrondissement": "Montreal 2",
            "latitude": None,
            "longitude": None,
        }
    ]


def test_get_stations_by_arrondissement_with_name_and_arrondissement(
    client, mock_controller
):
    station_instance = StationModel(id=1, name="Station 3", arrondissement="Montreal 3")
    mock_controller.get_stations = AsyncMock(return_value=[station_instance])
    response = client.get("/stations?name=Station 3&arrondissement=Montreal 3")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Station 3",
            "arrondissement": "Montreal 3",
            "latitude": None,
            "longitude": None,
        }
    ]


def test_get_stations_by_arrondissement_no_params(client, mock_controller):
    station_1 = StationModel(id=1, name="Station 1", arrondissement="Montreal 1")
    station_2 = StationModel(id=1, name="Station 2", arrondissement="Montreal 2")
    mock_controller.get_stations = AsyncMock(return_value=[station_1, station_2])
    response = client.get("/stations")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Station 1",
            "arrondissement": "Montreal 1",
            "latitude": None,
            "longitude": None,
        },
        {
            "name": "Station 2",
            "arrondissement": "Montreal 2",
            "latitude": None,
            "longitude": None,
        },
    ]
