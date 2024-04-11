from functools import wraps

from cache import MongoDBCache
from constants import TRIP_CACHE_TTL
from repository import TripRepository


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
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = await func(self, *args, **kwargs)
            try:
                await cache.set(cache_key, result, ttl)
            finally:
                return result

        return wrapper

    return decorator


class TripController:
    def __init__(self, trip_repository: TripRepository, cache: MongoDBCache):
        self.trip_repository = trip_repository
        self.cache = cache

    @use_cache(key_prefix="trip_stats")
    async def get_trip_stats(self, minStartTimeMs: int, maxStartTimeMs: int):
        return await self.trip_repository.get_trip_stats(minStartTimeMs, maxStartTimeMs)

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
