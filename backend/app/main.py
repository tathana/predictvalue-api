from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import forecast

app = FastAPI(
    title="PredictValue API",
    description="Water Quality Forecast API (Statistical Mock)",
    version="1.0.0"
)

# ✅ CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",              # local dev
        "http://localhost:5173",
        "https://predictvalue.vercel.app",    # (เผื่อ deploy frontend)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register router
app.include_router(forecast.router)

@app.get("/")
def root():
    return {
        "message": "PredictValue API is running",
        "docs": "/docs"
    }
