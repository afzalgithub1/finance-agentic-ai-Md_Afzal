from pathlib import Path
import json
from datetime import datetime
import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from xgboost import XGBRegressor

from ml.data_loader import (
    load_stock_data,
    get_company_data,
    list_available_companies,
)

from ml.feature_engineering import (
    create_features,
    FEATURE_COLUMNS,
)


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR / "saved_models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MODEL_FILE = MODEL_DIR / "stock_price_model.joblib"

ENCODER_FILE = MODEL_DIR / "company_encoder.joblib"

FEATURE_FILE = MODEL_DIR / "feature_columns.joblib"


# ============================================================
# Model Features
# ============================================================

MODEL_FEATURES = FEATURE_COLUMNS + [
    "Company_Code"
]


# ============================================================
# Helper Functions
# ============================================================




def split_company_data(
    company_df: pd.DataFrame,
    train_ratio: float = 0.80,
):
    """
    Perform chronological train-test split
    for one company.

    Parameters
    ----------
    company_df : pd.DataFrame

    train_ratio : float

    Returns
    -------
    train_df, test_df
    """

    split_index = int(
        len(company_df) * train_ratio
    )

    train_df = company_df.iloc[
        :split_index
    ]

    test_df = company_df.iloc[
        split_index:
    ]

    return train_df, test_df

# ============================================================
# Dataset Preparation
# ============================================================

print("=" * 70)
print("Loading Historical Stock Data...")
print("=" * 70)

master_df = load_stock_data()

companies = list_available_companies(master_df)

company_encoder = LabelEncoder()

company_encoder.fit(
    master_df["Company_Name"]
)

print(f"Companies Found : {len(companies)}")
print(f"Companies       : {companies}")

print()

training_frames = []
testing_frames = []

# ============================================================
# Prepare Dataset Company Wise
# ============================================================

for company in companies:

    print(f"Preparing : {company}")

    company_df = get_company_data(
        master_df,
        company,
    )

    company_df = create_features(
        company_df,
    )

    train_df, test_df = split_company_data(
        company_df,
    )

    training_frames.append(
        train_df,
    )

    testing_frames.append(
        test_df,
    )

print()

print("=" * 70)
print("Combining Company Datasets...")
print("=" * 70)


train_df = pd.concat(
    training_frames,
    ignore_index=True,
)

test_df = pd.concat(
    testing_frames,
    ignore_index=True,
)

train_df = train_df.reset_index(drop=True)

test_df = test_df.reset_index(drop=True)

print(f"Training Rows : {len(train_df)}")
print(f"Testing Rows  : {len(test_df)}")

print()

# ============================================================
# Encode Company Names
# ============================================================

train_df["Company_Code"] = company_encoder.transform(
    train_df["Company_Name"]
)

test_df["Company_Code"] = company_encoder.transform(
    test_df["Company_Name"]
)

print()

print("Company Encoding Completed")

company_mapping = dict(
    zip(
        company_encoder.classes_,
        company_encoder.transform(
            company_encoder.classes_
        ),
    )
)

print(company_mapping)

print()

# ============================================================
# Prepare Training Data
# ============================================================

X_train = train_df[
    MODEL_FEATURES
]

y_train = train_df[
    "Target"
]

X_test = test_df[
    MODEL_FEATURES
]

y_test = test_df[
    "Target"
]

print("=" * 70)
print("Dataset Ready")
print("=" * 70)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

print(f"Features         : {len(MODEL_FEATURES)}")

print()

# ============================================================
# Train XGBoost Model
# ============================================================

print("=" * 70)
print("Training XGBoost Model...")
print("=" * 70)

model = XGBRegressor(

    objective="reg:squarederror",

    eval_metric="rmse",

    n_estimators=500,

    learning_rate=0.05,

    max_depth=8,

    min_child_weight=3,

    subsample=0.8,

    colsample_bytree=0.8,

    random_state=42,

    n_jobs=-1,

    verbosity=1,
)

model.fit(
    X_train,
    y_train,
)

print()

print("Model Training Completed")

print()


# ============================================================
# Model Evaluation
# ============================================================

predictions = model.predict(
    X_test
)

mae = mean_absolute_error(
    y_test,
    predictions,
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions,
    )
)

r2 = r2_score(
    y_test,
    predictions,
)

print("=" * 70)
print("Overall Model Performance")
print("=" * 70)

print(f"MAE  : {mae:.4f}")

print(f"RMSE : {rmse:.4f}")

print(f"R²   : {r2:.4f}")

print()


# ============================================================
# Feature Importance
# ============================================================

importance_df = (
    pd.DataFrame(
        {
            "Feature": MODEL_FEATURES,
            "Importance": model.feature_importances_,
        }
    )
    .sort_values(
        by="Importance",
        ascending=False,
    )
)

importance_df.to_csv(
    MODEL_DIR / "feature_importance.csv",
    index=False,
)

print("=" * 70)
print("Top 10 Important Features")
print("=" * 70)

print(
    importance_df.head(10).to_string(
        index=False
    )
)

print()


# ============================================================
# Save Model
# ============================================================

joblib.dump(
    model,
    MODEL_FILE,
)

joblib.dump(
    company_encoder,
    ENCODER_FILE,
)

joblib.dump(
    MODEL_FEATURES,
    FEATURE_FILE,
)

print("=" * 70)
print("Model Saved Successfully")
print("=" * 70)

print(f"Model    : {MODEL_FILE}")
print(f"Encoder  : {ENCODER_FILE}")
print(f"Features : {FEATURE_FILE}")

print()


# ============================================================
# Save Metadata
# ============================================================

metadata = {
    "model": "XGBoost",
    "version": "1.0",
    "trained_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "companies": len(companies),
    "training_rows": len(train_df),
    "testing_rows": len(test_df),
    "features": MODEL_FEATURES,
}

metadata_file = MODEL_DIR / "model_metadata.json"

with open(
    metadata_file,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        metadata,
        f,
        indent=4,
    )

print(f"Metadata : {metadata_file}")

print()

print("=" * 70)
print("Training Completed Successfully")
print("=" * 70)


# ============================================================
# Prediction Example
# ============================================================

example = X_test.iloc[:5]

pred = model.predict(example)

print()

print("Sample Predictions")

for i in range(len(pred)):

    print(
        f"Prediction {i + 1}: {pred[i]:.2f}"
    )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    pass