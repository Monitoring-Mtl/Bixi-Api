from constants import MAX_INT64
from controller import TripController
from dependencies import get_controller
from fastapi import APIRouter, Depends, HTTPException, Query
from models import TripModel, TripStatModel

trip_router = APIRouter(prefix="/trips")


@trip_router.get("/health", tags=["health"])
async def health():
    return {"message": "ok"}


@trip_router.get("/duration/stats", tags=["trips"], response_model=TripStatModel)
async def get_trip_stats(
    controller: TripController = Depends(get_controller),
    min_start_time: int = Query(default=0, ge=0),
    max_start_time: int = Query(default=MAX_INT64, le=MAX_INT64),
):
    if min_start_time > max_start_time:
        detail = "start_time_max_ms must be greater than start_time_min_ms"
        raise HTTPException(status_code=400, detail=detail)
    return await controller.get_trip_stats(min_start_time, max_start_time)


@trip_router.get("/time/start/minimum", tags=["trips"], response_model=TripModel)
async def get_minimum_start_time(controller: TripController = Depends(get_controller)):
    return await controller.get_minimum_start_time()


@trip_router.get("/time/start/maximum", tags=["trips"], response_model=TripModel)
async def get_maximum_start_time(controller: TripController = Depends(get_controller)):
    return await controller.get_maximum_start_time()


@trip_router.get("/time/end/minimum", tags=["trips"], response_model=TripModel)
async def get_minimum_end_time(controller: TripController = Depends(get_controller)):
    return await controller.get_minimum_end_time()


@trip_router.get("/time/end/maximum", tags=["trips"], response_model=TripModel)
async def get_maximum_end_time(controller: TripController = Depends(get_controller)):
    return await controller.get_maximum_end_time()
