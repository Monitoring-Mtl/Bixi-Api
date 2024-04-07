from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class TripModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    startStationName: str | None
    endStationName: str | None
    startTimeMs: int | None
    endTimeMs: int | None
    durationMs: int | None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class TripStatModel(BaseModel):
    averageDuration: float | None = None
    minDuration: int | None = None
    maxDuration: int | None = None
    stdDevDuration: float | None = None
    tripCount: int | None = None
