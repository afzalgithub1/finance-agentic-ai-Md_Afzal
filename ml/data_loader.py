from pathlib import Path
import re

import pandas as pd


# -----------------------------------------------------
# Paths
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "market_data"
    / "master_5year_daily_stock_prices.csv"
)


# -----------------------------------------------------
# Data Loading
# -----------------------------------------------------

def load_stock_data() -> pd.DataFrame:
    """
    Load historical stock price data.

    Returns:
        pd.DataFrame
    """

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Stock data file not found:\n{DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    df["Date"] = pd.to_datetime(df["Date"])

    df.sort_values(
        by=["Company_Name", "Date"],
        inplace=True,
    )

    df.reset_index(
        drop=True,
        inplace=True,
    )

    return df


# -----------------------------------------------------
# Utility Functions
# -----------------------------------------------------

def normalize_company_name(name: str) -> str:
    """
    Normalize company names for matching.

    Examples
    --------
    HDFC Bank
    HDFC_BANK
    hdfc-bank

    become

    hdfcbank
    """

    return re.sub(
        r"[^a-zA-Z0-9]",
        "",
        name,
    ).lower()


# -----------------------------------------------------
# Company Data
# -----------------------------------------------------

def get_company_data(
    df: pd.DataFrame,
    company_name: str,
) -> pd.DataFrame:
    """
    Return all rows for a company.

    Parameters
    ----------
    df : pandas.DataFrame

    company_name : str
        Examples:
            HDFC Bank
            HDFC_BANK
            ICICI Bank
            Reliance

    Returns
    -------
    pandas.DataFrame
    """

    normalized_target = normalize_company_name(company_name)

    normalized_companies = (
        df["Company_Name"]
        .astype(str)
        .apply(normalize_company_name)
    )

    company_df = df.loc[
        normalized_companies == normalized_target
    ].copy()

    if company_df.empty:

        available_companies = sorted(
            df["Company_Name"].unique()
        )

        raise ValueError(
            f"Company '{company_name}' not found.\n\n"
            f"Available companies:\n"
            + "\n".join(available_companies)
        )

    company_df.sort_values(
        by="Date",
        inplace=True,
    )

    company_df.reset_index(
        drop=True,
        inplace=True,
    )

    return company_df


# -----------------------------------------------------
# Dataset Information
# -----------------------------------------------------

def list_available_companies(
    df: pd.DataFrame,
) -> list[str]:
    """
    Return all available companies.
    """

    return sorted(
        df["Company_Name"].unique().tolist()
    )


def get_company_count(
    df: pd.DataFrame,
) -> int:
    """
    Number of unique companies.
    """

    return df["Company_Name"].nunique()