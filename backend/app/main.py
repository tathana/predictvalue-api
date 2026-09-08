from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import forecast, map as map_router

app = FastAPI(
    title="PredictValue API",
    description="Water Quality Forecast & Map API",
    version="1.1.0",
)

# ======================
# CORS CONFIG
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# Routers
# ======================
app.include_router(forecast.router)
app.include_router(map_router.router)



@app.get("/")
def root():
    return {"message": "PredictValue API is running", "docs": "/docs"}
