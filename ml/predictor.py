from pathlib import Path

import joblib
import pandas as pd

from ml.data_loader import (
    load_stock_data,
    get_company_data,
)

from ml.feature_engineering import (
    create_features,
)


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "saved_models"

MODEL_FILE = MODEL_DIR / "stock_price_model.joblib"

ENCODER_FILE = MODEL_DIR / "company_encoder.joblib"

FEATURE_FILE = MODEL_DIR / "feature_columns.joblib"


# ============================================================
# Load Saved Objects
# ============================================================

model = joblib.load(MODEL_FILE)

company_encoder = joblib.load(ENCODER_FILE)

feature_columns = joblib.load(FEATURE_FILE)


# ============================================================
# Load Dataset
# ============================================================

master_df = load_stock_data()


# ============================================================
# Prediction Function
# ============================================================

def predict_next_close(company_name: str) -> dict:
    """
    Predict the next day's closing price for a company.

    Parameters
    ----------
    company_name : str

    Returns
    -------
    dict
    """

    company_df = get_company_data(
        master_df,
        company_name,
    )

    company_df = create_features(
        company_df,
    )

    latest_row = company_df.iloc[-1].copy()

    latest_row["Company_Code"] = company_encoder.transform(
        [latest_row["Company_Name"]]
    )[0]

    X = pd.DataFrame(
        [latest_row]
    )[feature_columns]

    prediction = model.predict(X)[0]

    return {
        "company": latest_row["Company_Name"],
        "last_close": float(latest_row["Close"]),
        "predicted_close": float(prediction),
        "prediction_date": "Next Trading Day",
    }


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    result = predict_next_close(
        "HDFC_BANK"
    )

    print()

    print("=" * 70)
    print("Prediction Result")
    print("=" * 70)

    for key, value in result.items():
        print(f"{key:20}: {value}")