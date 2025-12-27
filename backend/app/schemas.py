from typing import List, Optional
from pydantic import BaseModel

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
