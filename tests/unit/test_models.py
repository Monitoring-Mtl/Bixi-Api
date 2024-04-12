import pytest
from pydantic import ValidationError

from trips.models import TripModel, TripStatModel


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
    data = {
        "averageDuration": 3600.0,
        "minDuration": 1800,
        "maxDuration": 5400,
        "stdDevDuration": 600.0,
        "tripCount": 10,
    }
    stats = TripStatModel(**data)
    assert stats.averageDuration == 3600.0
    assert stats.minDuration == 1800
    assert stats.maxDuration == 5400
    assert stats.stdDevDuration == 600.0
    assert stats.tripCount == 10


def test_trip_stat_model_defaults():
    stats = TripStatModel()
    assert stats.averageDuration is None
    assert stats.minDuration is None
    assert stats.maxDuration is None
    assert stats.stdDevDuration is None
    assert stats.tripCount is None


def test_trip_stat_model_validation_error():
    with pytest.raises(ValidationError):
        TripStatModel(tripCount="not_an_int")
