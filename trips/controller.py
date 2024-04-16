import traceback
from functools import wraps

from cache import MongoDBCache
from constants import TRIP_CACHE_TTL
from repository import StationRepository, TripRepository


def use_cache(key_prefix, ttl=TRIP_CACHE_TTL):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            cache: MongoDBCache = self.cache
            cache_key = (
                f"{key_prefix}_"
                + "_".join(map(str, args))
                + "_"
                + "_".join(f"{k}_{v}" for k, v in kwargs.items())
            )
            print(f"Cache key: {cache_key}")
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                print("Returning cached result")
                return cached_result
            result = await func(self, *args, **kwargs)
            try:
                await cache.set(cache_key, result, ttl)
                print("Cache updated")
            except Exception as e:
                print(f"An error occurred during cache set: {e}")
                traceback.print_exc()
            finally:
                return result

        return wrapper

    return decorator


class Controller:
    def __init__(
        self,
        trip_repository: TripRepository,
        station_repository: StationRepository,
        cache: MongoDBCache,
    ):
        self.trip_repository = trip_repository
        self.station_repository = station_repository
        self.cache = cache

    @use_cache(key_prefix="average_duration")
    async def get_average_duration(
        self,
        minStartTimeMs: int,
        maxStartTimeMs: int,
        startStationName: str | None = None,
        endStationName: str | None = None,
    ):
        return await self.trip_repository.get_average_duration(
            minStartTimeMs, maxStartTimeMs, startStationName, endStationName
        )

    @use_cache(key_prefix="minimum_start_time")
    async def get_minimum_start_time(self):
        return await self.trip_repository.get_minimum_start_time()

    @use_cache(key_prefix="maximum_start_time")
    async def get_maximum_start_time(self):
        return await self.trip_repository.get_maximum_start_time()

    @use_cache(key_prefix="minimum_end_time")
    async def get_minimum_end_time(self):
        return await self.trip_repository.get_minimum_end_time()

    @use_cache(key_prefix="maximum_end_time")
    async def get_maximum_end_time(self):
        return await self.trip_repository.get_maximum_end_time()

    @use_cache(key_prefix="arrondissements")
    async def get_arrondissements(self):
        return await self.station_repository.get_arrondissements()

    @use_cache(key_prefix="stations")
    async def get_stations(self, name: str | None, arrondissement: str | None):
        if name:
            return await self.station_repository.get_stations_by_name(name)
        if arrondissement:
            return await self.station_repository.get_station_by_arrondissement(
                arrondissement
            )
        return await self.station_repository.get_stations()
