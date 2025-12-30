from typing import List, Optional
from pydantic import BaseModel


# =====================================================
# 🔹 ของเดิม (ใช้กับ /forecast, n8n)
# =====================================================
class ForecastItem(BaseModel):
    date: str
    secchi: Optional[float] = None
    chlorophyll_a: Optional[float] = None
    tsi: Optional[float] = None
    turbidity: Optional[float] = None
    salinity: Optional[float] = None
    do: Optional[float] = None
    ph: Optional[float] = None


class ForecastResponse(BaseModel):
    station: str
    resolution: str
    horizon: int
    forecast: List[ForecastItem]


# =====================================================
# 🔹 ของใหม่ (ใช้กับเว็บ /forecast/timeseries)
# =====================================================
class TimeSeriesPoint(BaseModel):
    date: str
    value: Optional[float]


class TimeSeriesResponse(BaseModel):
    station: str
    parameter: str
    actual: List[TimeSeriesPoint]
    forecast: List[TimeSeriesPoint]
