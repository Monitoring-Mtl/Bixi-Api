import os

ATLAS_URI = os.environ["ATLAS_URI"]
MONGO_DATABASE_NAME = os.environ["MONGO_DATABASE_NAME"]
BIXI_TRIP_COLLECTION = os.environ["BIXI_TRIP_COLLECTION"]
MAX_INT64 = 2**63 - 1000  # because swagger rounds to a number that exceeds the limit
