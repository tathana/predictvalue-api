import pandas as pd
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()

# forecast_service.py
# → services
# → app
# → backend
# → PredictValue  ✅
PROJECT_ROOT = CURRENT_FILE.parents[3]

# ===== Directories =====
BASE_FORECAST_DIR = PROJECT_ROOT / "outputs" / "forecasts"
BASE_PREPARED_DIR = PROJECT_ROOT / "data" / "prepared"


# =====================================================
# Forecast (Future data) — ใช้กับ n8n และเว็บ
# =====================================================
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

    # convert Timestamp → string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df


# =====================================================
# Prepared (Historical data) — ใช้สำหรับเว็บกราฟ
# =====================================================
def load_prepared_csv(station: str) -> pd.DataFrame:
    """
    Load historical (prepared) time-series data for a station
    """
    file_name = f"{station}_prepared.csv"
    file_path = BASE_PREPARED_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Prepared file not found: {file_path}")

    df = pd.read_csv(
        file_path,
        parse_dates=[0]
    )

    # ให้ column แรกเป็น date เสมอ
    df.rename(columns={df.columns[0]: "date"}, inplace=True)

    # convert Timestamp → string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df
