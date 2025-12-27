from fastapi import APIRouter, Query, HTTPException
from backend.app.services.forecast_service import load_forecast_csv
from backend.app.schemas import ForecastResponse

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

@router.get("/", response_model=ForecastResponse)
def get_forecast(
    station: str = Query(..., example="CP01"),
    resolution: str = Query(
        "monthly",
        enum=["monthly", "weekly"]
    ),
    horizon: int = Query(
        12,
        ge=1,
        le=52,
        description="Number of future steps"
    )
):
    try:
        df = load_forecast_csv(
            station=station,
            resolution=resolution,
            horizon=horizon
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "station": station,
        "resolution": resolution,
        "horizon": horizon,
        "forecast": df.to_dict(orient="records")
    }
