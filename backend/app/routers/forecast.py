from fastapi import APIRouter, Query, HTTPException
from backend.app.services.forecast_service import (
    load_forecast_csv,
    load_prepared_csv
)
from backend.app.schemas import (
    ForecastResponse,
    TimeSeriesResponse
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

# =====================================================
# 1️⃣ Forecast-only (ใช้กับ n8n / automation)
# =====================================================
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


# =====================================================
# 2️⃣ TimeSeries (Actual + Forecast) — ใช้กับ Web
# =====================================================
@router.get("/timeseries", response_model=TimeSeriesResponse)
def get_timeseries(
    station: str = Query(..., example="CP01"),
    parameter: str = Query(..., example="secchi"),
    horizon: int = Query(
        12,
        ge=1,
        le=52,
        description="Number of future steps"
    )
):
    try:
        past_df = load_prepared_csv(station)
        future_df = load_forecast_csv(
            station=station,
            resolution="monthly",
            horizon=horizon
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if parameter not in past_df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Parameter '{parameter}' not found in prepared data"
        )

    return {
        "station": station,
        "parameter": parameter,
        "actual": [
            {
                "date": row["date"],
                "value": row[parameter]
            }
            for _, row in past_df.iterrows()
            if row[parameter] is not None
        ],
        "forecast": [
            {
                "date": row["date"],
                "value": row.get(parameter)
            }
            for _, row in future_df.iterrows()
            if row.get(parameter) is not None
        ]
    }
