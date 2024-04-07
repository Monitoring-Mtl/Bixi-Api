from fastapi import FastAPI
from mangum import Mangum
from routes import trip_router

app = FastAPI()
app.include_router(trip_router)
handler = Mangum(app)
