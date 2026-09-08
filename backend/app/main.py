from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import forecast

app = FastAPI(
    title="PredictValue API",
    description="Water Quality Forecast API (Statistical Mock)",
    version="1.0.0",
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


@app.get("/")
def root():
    return {"message": "PredictValue API is running", "docs": "/docs"}
