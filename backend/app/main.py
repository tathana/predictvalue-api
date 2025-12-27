from fastapi import FastAPI
from backend.app.routers import forecast

app = FastAPI(
    title="PredictValue API",
    description="Water Quality Forecast API (Statistical Mock)",
    version="1.0.0"
)

# register router
app.include_router(forecast.router)

@app.get("/")
def root():
    return {
        "message": "PredictValue API is running",
        "docs": "/docs"
    }
