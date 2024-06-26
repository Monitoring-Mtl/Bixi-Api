from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class TripModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    startStationName: str | None = None
    endStationName: str | None = None
    startTimeMs: int | None = None
    endTimeMs: int | None = None
    durationMs: int | None = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class TripAverageModel(BaseModel):
    averageDuration: float | None = None
    tripCount: int | None = None


class StationModel(BaseModel):
    name: PyObjectId | None = Field(alias="_id", default=None)
    arrondissement: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
