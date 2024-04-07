from repository import TripRepository


class TripController:
    def __init__(self, trip_repository: TripRepository):
        self.trip_repository = trip_repository

    async def get_trip_stats(self, start_time_min_ms: int, start_time_max_ms: int):
        return await self.trip_repository.get_trip_stats(
            start_time_min_ms, start_time_max_ms
        )

    async def get_minimum_start_time(self):
        return await self.trip_repository.get_minimum_start_time()

    async def get_maximum_start_time(self):
        return await self.trip_repository.get_maximum_start_time()

    async def get_minimum_end_time(self):
        return await self.trip_repository.get_minimum_end_time()

    async def get_maximum_end_time(self):
        return await self.trip_repository.get_maximum_end_time()
