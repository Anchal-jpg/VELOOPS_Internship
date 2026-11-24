"""
VELOOP Product Analytics - Duplicate Analysis Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

from typing import Dict, List, Optional, Any
import pandas as pd


class DuplicateAnalyzer:
    """
    Identifies full row duplicates, key-level collisions, and multi-column anomalies.
    """

    def __init__(self, df: pd.DataFrame, dataset_name: str = "Dataset"):
        self.df = df
        self.dataset_name = dataset_name

    def find_full_row_duplicates(self) -> Dict[str, Any]:
        """Check for completely identical rows across all columns."""
        dup_mask = self.df.duplicated(keep=False)
        dup_count = self.df.duplicated().sum()
        dup_rows = self.df[dup_mask]

        return {
            "dataset_name": self.dataset_name,
            "total_rows": len(self.df),
            "duplicate_count": int(dup_count),
            "duplicate_percentage": round((dup_count / len(self.df)) * 100, 3) if len(self.df) > 0 else 0.0,
            "has_full_duplicates": dup_count > 0,
            "sample_duplicates": dup_rows.head(6) if dup_count > 0 else pd.DataFrame(),
        }

    def check_key_duplicates(self, key_columns: List[str]) -> Dict[str, Any]:
        """
        Check for duplicate values on a single column or combination of columns (composite key).
        """
        missing_keys = [k for k in key_columns if k not in self.df.columns]
        if missing_keys:
            raise KeyError(f"Columns not found in dataset: {missing_keys}")

        dup_mask = self.df.duplicated(subset=key_columns, keep=False)
        dup_count = self.df.duplicated(subset=key_columns).sum()
        dup_rows = self.df[dup_mask].sort_values(by=key_columns)

        return {
            "dataset_name": self.dataset_name,
            "key_columns": key_columns,
            "total_rows": len(self.df),
            "duplicate_key_count": int(dup_count),
            "has_key_duplicates": dup_count > 0,
            "sample_duplicate_groups": dup_rows.head(10) if dup_count > 0 else pd.DataFrame(),
        }

    def compare_clean_vs_messy(
        self, clean_df: pd.DataFrame, messy_df: pd.DataFrame, id_col: str
    ) -> Dict[str, Any]:
        """
        Compare clean dataset against messy audit dataset to isolate introduced duplicates and defects.
        """
        clean_dups = clean_df.duplicated(subset=[id_col]).sum()
        messy_dups = messy_df.duplicated(subset=[id_col]).sum()

        return {
            "clean_total_rows": len(clean_df),
            "messy_total_rows": len(messy_df),
            "clean_id_duplicates": int(clean_dups),
            "messy_id_duplicates": int(messy_dups),
            "injected_duplicates": int(messy_dups - clean_dups),
        }

