"""
VELOOP Product Analytics - Missing Value Analysis Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

from typing import Dict, List, Optional
import pandas as pd
import numpy as np


class MissingValueAnalyzer:
    """
    Performs comprehensive missing value profiling, identifying intentional business logic
    omissions versus unexpected data dropouts.
    """

    def __init__(self, df: pd.DataFrame, dataset_name: str = "Dataset"):
        self.df = df
        self.dataset_name = dataset_name

    def summarize_missing(self) -> pd.DataFrame:
        """
        Produce a summary table of all columns with missing values.
        """
        total_rows = len(self.df)
        null_counts = self.df.isnull().sum()
        cols_with_nulls = null_counts[null_counts > 0]

        if cols_with_nulls.empty:
            return pd.DataFrame(columns=[
                "column_name", "missing_count", "missing_percentage", "data_type", "domain_assessment"
            ])

        records = []
        for col, count in cols_with_nulls.items():
            pct = round((count / total_rows) * 100, 2)
            dtype = str(self.df[col].dtype)
            assessment = self._assess_missing_context(col)

            records.append({
                "column_name": col,
                "missing_count": int(count),
                "missing_percentage": pct,
                "data_type": dtype,
                "domain_assessment": assessment,
            })

        result_df = pd.DataFrame(records).sort_values(by="missing_count", ascending=False)
        return result_df

    def _assess_missing_context(self, col: str) -> str:
        """Categorize why a column might contain nulls based on VELOOP business logic."""
        c = col.lower()
        if "referral" in c:
            return "Expected: Organic users do not have a referral code or detail"
        elif "completed" in c:
            return "Expected: Incomplete, abandoned, or failed tasks do not have completion timestamps"
        elif "failure" in c:
            return "Expected: Successful or pending tasks do not have failure reasons"
        elif "exit" in c:
            return "Investigate: Sessions may terminate abruptly or lack explicit exit screen logging"
        elif "login" in c:
            return "Investigate: Inactive or newly registered users may have null last login"
        elif "session" in c and "id" in c:
            return "Defect: Orphan milestones recorded without an active session context"
        return "Unclassified missingness: Requires engineering review"

    def analyze_conditional_missingness(self, condition_col: str, target_col: str) -> pd.DataFrame:
        """
        Analyze how missing values in target_col distribute across categories of condition_col.
        Useful for checking e.g. task_status vs failure_reason.
        """
        return self.df.groupby(condition_col)[target_col].apply(
            lambda s: pd.Series({
                "total_records": len(s),
                "null_count": s.isnull().sum(),
                "null_pct": round((s.isnull().sum() / len(s)) * 100, 2) if len(s) > 0 else 0.0
            })
        ).unstack()

