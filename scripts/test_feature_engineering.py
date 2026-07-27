from ml.data_loader import load_stock_data, get_company_data
from ml.feature_engineering import create_features

df = load_stock_data()

company_df = get_company_data(
    df,
    "HDFC Bank"
)

feature_df = create_features(company_df)

print(feature_df.head())

print()

print(feature_df.columns.tolist())

print()

print("Rows :", len(feature_df))