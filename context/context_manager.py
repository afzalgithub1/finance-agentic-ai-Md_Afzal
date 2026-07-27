import json
import os
import re

import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMPANY_FILE = os.path.join(
    PROJECT_ROOT,
    "config",
    "companies.json",
)

with open(COMPANY_FILE, "r") as f:
    COMPANY_ALIASES = json.load(f)


class ConversationContext:

    @staticmethod
    def initialize():

        if "conversation_context" not in st.session_state:

            st.session_state.conversation_context = {
                "companies": [],
                "last_question": None,
                "last_tool": None,
            }

    @staticmethod
    def get_context():

        return st.session_state.conversation_context

    @staticmethod
    def _detect_companies(question: str):

        detected = []

        question = question.upper()

        for ticker, aliases in COMPANY_ALIASES.items():

            for alias in aliases:

                pattern = r"\b" + re.escape(alias.upper()) + r"\b"

                if re.search(pattern, question):

                    if ticker not in detected:
                        detected.append(ticker)

                    break

        return detected

    @staticmethod
    def rewrite_question(question: str):

        context = ConversationContext.get_context()

        companies = context["companies"]

        if not companies:
            return question

        rewritten = question
        lower = question.lower()
        padded = f" {lower} "

        # ----------------------------------------------------
        # Single company in context
        # ----------------------------------------------------

        if len(companies) == 1:

            company = companies[0]

            replacements = {
                " it ": company,
                " its ": f"{company}'s",
                " this company ": company,
                " this stock ": company,
            }

            for old, new in replacements.items():

                if old in padded:

                    rewritten = re.sub(
                        old.strip(),
                        new,
                        rewritten,
                        flags=re.IGNORECASE,
                    )

            # Compare current company with another company
            # Example:
            # Compare it with Reliance

            if "compare" in lower:

                detected = ConversationContext._detect_companies(question)

                if detected:

                    other = detected[0]

                    if other != company:

                        return f"Compare {company} and {other}"

            return rewritten

        # ----------------------------------------------------
        # Multiple companies in context
        # ----------------------------------------------------

        company_text = " and ".join(companies)

        # Which one has higher ROE?
        if (
            "which one" in lower
            or "which company" in lower
        ):

            return (
                f"Compare {company_text} "
                f"based on {question}"
            )

        # Compare it with Reliance
        if "compare" in lower:

            detected = ConversationContext._detect_companies(question)

            if detected:

                new_company = detected[0]

                existing = companies[0]

                if new_company != existing:

                    return f"Compare {existing} and {new_company}"

        replacements = {
            " them ": company_text,
            " they ": company_text,
            " both ": company_text,
            " both companies ": company_text,
            " these companies ": company_text,
        }

        for old, new in replacements.items():

            if old in padded:

                rewritten = re.sub(
                    old.strip(),
                    new,
                    rewritten,
                    flags=re.IGNORECASE,
                )

        return rewritten

    @staticmethod
    def update_context(question: str, tool_used: str):

        context = ConversationContext.get_context()

        companies = ConversationContext._detect_companies(question)

        if companies:
            context["companies"] = companies

        context["last_question"] = question
        context["last_tool"] = tool_used