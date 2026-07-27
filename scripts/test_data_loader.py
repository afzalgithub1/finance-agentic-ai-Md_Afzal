from ml.data_loader import (
    load_stock_data,
    get_company_data,
    list_available_companies,
    get_company_count,
)

df = load_stock_data()

print("=" * 60)
print("Dataset Loaded Successfully")
print("=" * 60)

print(df.head())

print()

print(f"Total Rows      : {len(df)}")
print(f"Total Companies : {get_company_count(df)}")

print()

print("Companies:")
print(list_available_companies(df))

print()

company_df = get_company_data(df, "HDFC Bank")

print("=" * 60)
print("HDFC Bank")
print("=" * 60)

print(company_df.head())

print()

print(f"Rows : {len(company_df)}")