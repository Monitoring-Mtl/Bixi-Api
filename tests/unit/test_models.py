import pytest
from pydantic import ValidationError

from trips.models import StationModel, TripAverageModel, TripModel


def test_trip_model_creation_from_dict():
    data = {
        "id": "trip_id",
        "startStationName": "Station A",
        "endStationName": "Station B",
        "startTimeMs": 1620000000,
        "endTimeMs": 1620003600,
        "durationMs": 3600,
    }
    trip = TripModel(**data)
    assert trip.startStationName == "Station A"
    assert trip.endStationName == "Station B"
    assert trip.id == "trip_id"


def test_trip_model_alias():
    trip = TripModel(_id="123")
    assert trip.id == "123"


def test_trip_model_defaults():
    trip = TripModel()
    assert trip.id is None
    assert trip.startStationName is None
    assert trip.endStationName is None
    assert trip.startTimeMs is None
    assert trip.endTimeMs is None
    assert trip.durationMs is None


def test_trip_model_validation_error():
    with pytest.raises(ValidationError):
        TripModel(startStationName="Station A", startTimeMs="not_an_int")


def test_trip_stat_model_creation_from_dict():
    data = {"averageDuration": 3600.0, "tripCount": 10}
    stats = TripAverageModel(**data)
    assert stats.averageDuration == 3600.0
    assert stats.tripCount == 10


def test_trip_stat_model_defaults():
    stats = TripAverageModel()
    assert stats.averageDuration is None
    assert stats.tripCount is None


def test_trip_stat_model_validation_error():
    with pytest.raises(ValidationError):
        TripAverageModel(tripCount="not_an_int")


def test_station_model_creation_from_dict():
    data = {
        "_id": "station_001",
        "arrondissement": "7th",
        "latitude": 48.8588443,
        "longitude": 2.2943506,
    }
    station = StationModel(**data)
    assert station.name == "station_001"
    assert station.arrondissement == "7th"
    assert station.latitude == 48.8588443
    assert station.longitude == 2.2943506


def test_station_model_defaults():
    station = StationModel()
    assert station.name is None
    assert station.arrondissement is None
    assert station.latitude is None
    assert station.longitude is None


def test_station_model_validation_error():
    with pytest.raises(ValidationError):
        StationModel(latitude="not_a_float", longitude="not_a_float")
