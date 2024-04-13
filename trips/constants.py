import os

from dotenv import load_dotenv

load_dotenv()
ATLAS_URI = os.environ["ATLAS_URI"]
MONGO_DATABASE_NAME = os.environ["MONGO_DATABASE_NAME"]
BIXI_TRIP_COLLECTION = os.environ["BIXI_TRIP_COLLECTION"]
CACHE_COLLECTION = os.environ["BIXI_CACHE_COLLECTION"]
TRIP_CACHE_TTL = int(os.getenv("TRIP_CACHE_TTL", "2678400"))
MAX_INT64 = 2**63
STAGE_NAME = os.getenv("STAGE_NAME", "")
YEAR = 31536000000
DAY = 86400000
