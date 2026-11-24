"""
VELOOP Product Analytics - Dataset Inspector Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np


class DatasetInspector:
    """
    Examines schema structure, records, memory footprint, potential primary keys,
    and cross-table relationships for VELOOP datasets.
    """

    def __init__(self, df: pd.DataFrame, dataset_name: str = "Dataset"):
        self.df = df
        self.dataset_name = dataset_name

    def get_basic_info(self) -> Dict[str, Any]:
        """Return basic metadata: row count, column count, memory footprint."""
        return {
            "dataset_name": self.dataset_name,
            "row_count": len(self.df),
            "column_count": len(self.df.columns),
            "memory_mb": round(self.df.memory_usage(deep=True).sum() / (1024 * 1024), 3),
        }

    def inspect_columns(self) -> pd.DataFrame:
        """
        Generate detailed column-by-column schema profile.
        Returns DataFrame with columns:
        [column_name, data_type, non_null_count, null_count, null_pct, unique_count, sample_value]
        """
        rows = []
        total_rows = len(self.df)

        for col in self.df.columns:
            series = self.df[col]
            non_null = int(series.count())
            null_count = int(series.isnull().sum())
            null_pct = round((null_count / total_rows) * 100, 2) if total_rows > 0 else 0.0
            unique_count = int(series.nunique(dropna=True))

            # Grab first valid sample
            valid_samples = series.dropna()
            sample_val = str(valid_samples.iloc[0]) if len(valid_samples) > 0 else "None"
            if len(sample_val) > 50:
                sample_val = sample_val[:47] + "..."

            rows.append({
                "column_name": col,
                "data_type": str(series.dtype),
                "non_null_count": non_null,
                "null_count": null_count,
                "null_pct": null_pct,
                "unique_count": unique_count,
                "sample_value": sample_val,
            })

        return pd.DataFrame(rows)

    def identify_potential_primary_keys(self) -> List[str]:
        """Identify columns that are strictly non-null and 100% unique."""
        total_rows = len(self.df)
        candidates = []
        for col in self.df.columns:
            if self.df[col].isnull().sum() == 0 and self.df[col].nunique() == total_rows:
                candidates.append(col)
        return candidates

    @staticmethod
    def check_referential_integrity(
        child_df: pd.DataFrame,
        child_col: str,
        parent_df: pd.DataFrame,
        parent_col: str,
        relation_name: str = "Relationship"
    ) -> Dict[str, Any]:
        """
        Check if all values in child_col exist in parent_col.
        Identifies orphan foreign keys.
        """
        child_series = child_df[child_col].dropna()
        parent_set = set(parent_df[parent_col].dropna().unique())

        child_unique = set(child_series.unique())
        orphans = child_unique - parent_set
        total_child_records = len(child_series)
        orphan_records = child_df[child_col].isin(orphans).sum()

        return {
            "relation_name": relation_name,
            "child_column": child_col,
            "parent_column": parent_col,
            "total_child_records": total_child_records,
            "distinct_child_values": len(child_unique),
            "distinct_parent_values": len(parent_set),
            "orphan_distinct_count": len(orphans),
            "orphan_record_count": int(orphan_records),
            "orphan_samples": list(orphans)[:5],
            "is_valid_fk": len(orphans) == 0,
        }

