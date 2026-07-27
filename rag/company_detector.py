import json
import os
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMPANY_FILE = os.path.join(
    PROJECT_ROOT,
    "config",
    "companies.json"
)

with open(COMPANY_FILE, "r") as f:
    COMPANY_ALIASES = json.load(f)


def detect_company(question: str):

    question = question.upper()

    for ticker, aliases in COMPANY_ALIASES.items():

        for alias in aliases:

            pattern = r"\b" + re.escape(alias.upper()) + r"\b"

            if re.search(pattern, question):
                return ticker

    return None