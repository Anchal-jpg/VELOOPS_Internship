"""
VELOOP Product Analytics - Column Summary Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np


class ColumnSummaryAnalyzer:
    """
    Computes statistical, temporal, and categorical profiles for tabular dataset columns.
    """

    def __init__(self, df: pd.DataFrame, dataset_name: str = "Dataset"):
        self.df = df
        self.dataset_name = dataset_name

    def summarize_numeric_columns(self) -> pd.DataFrame:
        """Detailed metrics for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return pd.DataFrame()

        rows = []
        for col in numeric_cols:
            s = self.df[col].dropna()
            if len(s) == 0:
                continue
            rows.append({
                "column_name": col,
                "count": int(s.count()),
                "mean": round(float(s.mean()), 2),
                "std": round(float(s.std()), 2) if len(s) > 1 else 0.0,
                "min": round(float(s.min()), 2),
                "q25": round(float(s.quantile(0.25)), 2),
                "median": round(float(s.median()), 2),
                "q75": round(float(s.quantile(0.75)), 2),
                "max": round(float(s.max()), 2),
            })
        return pd.DataFrame(rows)

    def summarize_datetime_columns(self) -> pd.DataFrame:
        """Metrics for timestamp and date columns."""
        datetime_cols = []
        for col in self.df.columns:
            if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                datetime_cols.append(col)
            elif "date" in col.lower() or "time" in col.lower() or "at" in col.lower():
                try:
                    pd.to_datetime(self.df[col].dropna().head(10))
                    datetime_cols.append(col)
                except Exception:
                    pass

        if not datetime_cols:
            return pd.DataFrame()

        rows = []
        for col in datetime_cols:
            s = pd.to_datetime(self.df[col], errors="coerce").dropna()
            if len(s) == 0:
                continue
            min_dt = s.min()
            max_dt = s.max()
            span_days = round((max_dt - min_dt).total_seconds() / 86400, 1)

            rows.append({
                "column_name": col,
                "valid_timestamps": int(s.count()),
                "earliest_date": str(min_dt),
                "latest_date": str(max_dt),
                "time_span_days": span_days,
            })
        return pd.DataFrame(rows)

    def summarize_categorical_columns(self, max_top_values: int = 5) -> pd.DataFrame:
        """Metrics for categorical and text columns."""
        cat_cols = self.df.select_dtypes(include=["object", "string", "category"]).columns
        # Filter out potential datetime columns if already converted
        cat_cols = [c for c in cat_cols if not ("date" in c.lower() or "time" in c.lower())]

        rows = []
        total_rows = len(self.df)
        for col in cat_cols:
            s = self.df[col].dropna()
            n_unique = s.nunique()
            top_counts = s.value_counts().head(max_top_values)
            top_str_list = [f"{k} ({v}, {round((v/total_rows)*100, 1)}%)" for k, v in top_counts.items()]
            top_summary = "; ".join(top_str_list)

            rows.append({
                "column_name": col,
                "distinct_count": n_unique,
                "top_categories": top_summary,
            })
        return pd.DataFrame(rows)

