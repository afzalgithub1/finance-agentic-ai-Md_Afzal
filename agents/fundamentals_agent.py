from pathlib import Path
import json
import pandas as pd

from rag.company_detector import detect_company


class FundamentalsAgent:

    METRIC_MAP = {
        "pe": "Stock P/E",
        "p/e": "Stock P/E",
        "stock pe": "Stock P/E",

        "roe": "ROE",
        "roce": "ROCE",
        "eps": "EPS",

        "market cap": "Market Cap",
        "book value": "Book Value",
        "current price": "Current Price",
        "price": "Current Price",
        "dividend": "Dividend Yield",
        "dividend yield": "Dividend Yield",
        "face value": "Face Value",
        "debt": "Debt",

        "revenue": "Revenue",
        "sales": "Sales",
        "operating profit": "Operating Profit",
        "expenses": "Expenses",
        "profit before tax": "Profit before tax",

        "cash flow": "Cash from Operating Activity"
    }

    def __init__(self):

        self.base_path = Path("data/fundamentals")

        with open("config/company_fundamental_map.json") as f:
            self.company_folder_map = json.load(f)

    def _get_company_folder(self, company):

        return self.company_folder_map.get(company)

    def _load_company_data(self, folder):

        folder_path = self.base_path / folder

        data = {}

        for csv_file in folder_path.glob("*.csv"):

            file_name = csv_file.stem

            try:
                data[file_name] = pd.read_csv(csv_file)
            except Exception as e:
                print(f"Unable to read {csv_file}: {e}")

        return data

    def _detect_metric(self, question):

        question = question.lower()

        for keyword, metric in self.METRIC_MAP.items():

            if keyword in question:
                return metric

        return None
    
    def _find_metric(self, dataframes, metric):

        # Search Basic Info
        for name, df in dataframes.items():

            if "Basic_Info" in name:

                if metric in df.columns:
                    return df.iloc[0][metric], name

        # Search remaining CSVs
        for name, df in dataframes.items():

            if "Basic_Info" in name:
                continue

            first_column = df.columns[0]

            if metric in df[first_column].values:

                row = df[df[first_column] == metric]

                return row.iloc[0, -1], name

        return None, None

    # def get_metric(self, company, metric):
    # """
    # Returns the raw value of a metric for a company.
    # Used by the comparison agent.
    # """

    # folder = self._get_company_folder(company)

    # if not folder:
    #     return None

    # data = self._load_company_data(folder)

    # value, _ = self._find_metric(data, metric)

    # return value
    

    def get_metric(self, company, metric):
        """
        Returns the raw value of a metric for a company.
        Used by the comparison agent.
        """

        folder = self._get_company_folder(company)

        if not folder:
            return None

        data = self._load_company_data(folder)

        value, _ = self._find_metric(data, metric)

        return value

    def run(self, question):

        company = detect_company(question)

        if not company:
            return {
                "agent": "Fundamentals",
                "answer": "Could not detect company."
            }

        folder = self._get_company_folder(company)

        if not folder:
            return {
                "agent": "Fundamentals",
                "answer": "Company data not available."
            }

        data = self._load_company_data(folder)

        metric = self._detect_metric(question)

        if metric is None:

            return {
                "agent": "Fundamentals",
                "answer": "Metric not supported."
            }

        value, source = self._find_metric(data, metric)

        if value is None:
            return {
                "agent": "Fundamentals",
                "answer": f"{metric} not found."
            }

        return {
            "agent": "Fundamentals",
            "company": company,
            "answer": f"{metric} of {folder} is {value}",
            "source": source
        }