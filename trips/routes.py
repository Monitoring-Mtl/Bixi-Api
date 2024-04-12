from constants import MAX_INT64
from controller import TripController
from fastapi import APIRouter, HTTPException, Query
from models import TripModel, TripStatModel

health_router = APIRouter(prefix="/health")
trip_router = APIRouter(prefix="/trips")


def use_controller(new_controller: TripController):
    global controller
    controller = new_controller


@health_router.get("", tags=["health"])
async def health():
    return {"message": "ok"}


@trip_router.get("/duration/stats", tags=["trips"], response_model=TripStatModel)
async def get_trip_stats(
    minStartTime: int = Query(default=0, ge=0, description="in milliseconds"),
    maxStartTime: int = Query(
        default=MAX_INT64 - 1000, le=MAX_INT64, description="in milliseconds"
    ),
):
    if minStartTime > maxStartTime:
        detail = "start_time_max_ms must be greater than start_time_min_ms"
        raise HTTPException(status_code=400, detail=detail)
    return await controller.get_trip_stats(minStartTime, maxStartTime)


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
