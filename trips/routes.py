from constants import MAX_INT64, YEAR
from controller import Controller
from fastapi import APIRouter, HTTPException, Query
from models import StationModel, TripAverageModel, TripModel

health_router = APIRouter(prefix="/health")
trip_router = APIRouter(prefix="/trips")
stations_router = APIRouter(prefix="/stations")


def use_controller(new_controller: Controller):
    global controller
    controller = new_controller


@health_router.get("", tags=["health"])
async def health():
    return {"message": "ok"}


@trip_router.get("/duration/average", tags=["trips"], response_model=TripAverageModel)
async def get_average_duration(
    minStartTime: int = Query(ge=0, description="in milliseconds"),
    maxStartTime: int = Query(le=MAX_INT64, description="in milliseconds"),
    startStationName: str = Query(None),
    endStationName: str = Query(None),
):
    if minStartTime > maxStartTime:
        detail = "start_time_max_ms must be greater than start_time_min_ms"
        raise HTTPException(status_code=400, detail=detail)
    if maxStartTime - minStartTime > YEAR:
        detail = "the range must not exceed 1 year"
        raise HTTPException(status_code=400, detail=detail)
    return await controller.get_average_duration(
        minStartTime, maxStartTime, startStationName, endStationName
    )


@trip_router.get(
    "/time/start/minimum",
    tags=["trips"],
    response_model=TripModel,
    response_model_by_alias=False,
)
async def get_minimum_start_time():
    return await controller.get_minimum_start_time()


@trip_router.get(
    "/time/start/maximum",
    tags=["trips"],
    response_model=TripModel,
    response_model_by_alias=False,
)
async def get_maximum_start_time():
    return await controller.get_maximum_start_time()


@trip_router.get(
    "/time/end/minimum",
    tags=["trips"],
    response_model=TripModel,
    response_model_by_alias=False,
)
async def get_minimum_end_time():
    return await controller.get_minimum_end_time()


@trip_router.get(
    "/time/end/maximum",
    tags=["trips"],
    response_model=TripModel,
    response_model_by_alias=False,
)
async def get_maximum_end_time():
    return await controller.get_maximum_end_time()


@stations_router.get("/arrondissements", tags=["stations"], response_model=list[str])
async def get_arrondissements():
    return await controller.get_arrondissements()


@stations_router.get(
    "",
    tags=["stations"],
    response_model=list[StationModel],
    response_model_by_alias=False,
)
async def get_stations(
    name: str | None = Query(default=None),
    arrondissement: str | None = Query(default=None),
):
    return await controller.get_stations(name, arrondissement)
