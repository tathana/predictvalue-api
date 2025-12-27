import pandas as pd
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# forecast_service.py
# → services
# → app
# → backend
# → PredictValue  ✅
PROJECT_ROOT = CURRENT_FILE.parents[3]

BASE_FORECAST_DIR = PROJECT_ROOT / "outputs" / "forecasts"

def load_forecast_csv(
    station: str,
    resolution: str,
    horizon: int
) -> pd.DataFrame:

    file_name = f"{station}_{resolution}_forecast.csv"
    file_path = BASE_FORECAST_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Forecast file not found: {file_path}")

    df = pd.read_csv(
        file_path,
        parse_dates=[0],
        index_col=0
    )

    df = df.head(horizon)
    df.reset_index(inplace=True)
    df.rename(columns={df.columns[0]: "date"}, inplace=True)

    # ✅ FIX: convert Timestamp → string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df
