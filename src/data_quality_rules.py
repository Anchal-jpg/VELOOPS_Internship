"""
VELOP Product Analytics - Enterprise Data Quality Rules Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Phase 5 (Days 22-23) Advanced Data Profiling & Quality Engine

Implements comprehensive verification checks across the 6 core Data Quality dimensions:
1. Completeness (Null constraints on required attributes)
2. Uniqueness (Primary key and candidate key deduplication)
3. Validity (Regex syntax, ISO datetime formatting, enum checks)
4. Consistency (Cross-field chronology and logic integrity)
5. Accuracy / Range (Boundary conditions and anomaly bounds)
6. Referential Integrity (Foreign key mapping across entities)
"""

import re
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


class DataQualityRulesEngine:
    """
    Automated engine executing data quality assertions on VELOOP datasets.
    """

    USER_ID_REGEX = re.compile(r"^VLUSR\d{6}$")
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    SESSION_ID_REGEX = re.compile(r"^SESS\d{7}$")
    TASK_ID_REGEX = re.compile(r"^[A-Z0-9_-]+$")

    # ----------------------------------------------------
    # 1. Completeness Checks
    # ----------------------------------------------------
    @classmethod
    def check_mandatory_nulls(cls, df: pd.DataFrame, required_columns: List[str], entity_name: str) -> Dict[str, Any]:
        """Verify that no mandatory columns contain null or NaN values."""
        present_cols = [c for c in required_columns if c in df.columns]
        missing_counts = df[present_cols].isnull().sum()
        failing_cols = missing_counts[missing_counts > 0].to_dict()
        
        passed = bool(len(failing_cols) == 0)
        total_violations = sum(failing_cols.values())
        
        return {
            "check_name": f"{entity_name}_mandatory_null_check",
            "dimension": "Completeness",
            "entity": entity_name,
            "passed": passed,
            "violations_count": total_violations,
            "failing_columns": failing_cols,
            "severity": "P0 - Critical" if total_violations > 0 else "PASS",
            "details": f"Found {total_violations} null values across mandatory columns: {failing_cols}" if not passed else "All mandatory columns 100% complete."
        }

    # ----------------------------------------------------
    # 2. Uniqueness Checks
    # ----------------------------------------------------
    @classmethod
    def check_uniqueness(cls, df: pd.DataFrame, column: str, entity_name: str) -> Dict[str, Any]:
        """Verify that a unique identifier contains zero duplicates."""
        if column not in df.columns:
            return {"check_name": f"{entity_name}_{column}_uniqueness", "passed": False, "violations_count": 0, "details": "Column missing"}
        
        dups_mask = df[column].duplicated(keep=False)
        dup_count = dups_mask.sum()
        dup_keys = df.loc[dups_mask, column].unique().tolist()
        
        passed = bool(dup_count == 0)
        return {
            "check_name": f"{entity_name}_{column}_uniqueness",
            "dimension": "Uniqueness",
            "entity": entity_name,
            "passed": passed,
            "violations_count": int(dup_count),
            "duplicate_keys": dup_keys[:10],
            "severity": "P0 - Critical" if not passed else "PASS",
            "details": f"Detected {dup_count} duplicate rows for key '{column}'." if not passed else f"Key '{column}' is 100% unique."
        }

    # ----------------------------------------------------
    # 3. Validity Checks (Regex & Enums)
    # ----------------------------------------------------
    @classmethod
    def check_regex_format(cls, df: pd.DataFrame, column: str, pattern: re.Pattern, entity_name: str) -> Dict[str, Any]:
        """Validate string format against standard regex pattern."""
        if column not in df.columns:
            return {"check_name": f"{entity_name}_{column}_regex", "passed": False, "violations_count": 0, "details": "Column missing"}
        
        non_null_series = df[column].dropna().astype(str)
        invalid_mask = ~non_null_series.str.match(pattern)
        invalid_count = invalid_mask.sum()
        
        passed = bool(invalid_count == 0)
        return {
            "check_name": f"{entity_name}_{column}_format_validity",
            "dimension": "Validity",
            "entity": entity_name,
            "passed": passed,
            "violations_count": int(invalid_count),
            "sample_invalids": non_null_series[invalid_mask].head(5).tolist(),
            "severity": "P1 - High" if not passed else "PASS",
            "details": f"{invalid_count} records violated regex {pattern.pattern}." if not passed else f"All records match pattern {pattern.pattern}."
        }

    @classmethod
    def check_datetime_parseability(cls, df: pd.DataFrame, column: str, entity_name: str) -> Dict[str, Any]:
        """Check whether datetime strings conform to valid parseable ISO-8601 timestamps."""
        if column not in df.columns:
            return {"check_name": f"{entity_name}_{column}_date_validity", "passed": False, "violations_count": 0, "details": "Column missing"}
        
        raw_series = df[column].dropna()
        parsed = pd.to_datetime(raw_series, errors="coerce")
        unparseable = raw_series[parsed.isnull()]
        unparseable_count = len(unparseable)
        
        passed = bool(unparseable_count == 0)
        return {
            "check_name": f"{entity_name}_{column}_date_parseability",
            "dimension": "Validity",
            "entity": entity_name,
            "passed": passed,
            "violations_count": int(unparseable_count),
            "sample_invalids": unparseable.head(5).tolist(),
            "severity": "P0 - Critical" if not passed else "PASS",
            "details": f"{unparseable_count} invalid date values found (e.g. invalid month/day)." if not passed else "All timestamps parseable."
        }

    @classmethod
    def check_allowed_values(cls, df: pd.DataFrame, column: str, allowed_set: set, entity_name: str) -> Dict[str, Any]:
        """Check if column values strictly belong to an authorized enumeration set."""
        if column not in df.columns:
            return {"check_name": f"{entity_name}_{column}_enum_validity", "passed": False, "violations_count": 0, "details": "Column missing"}
        
        non_null = df[column].dropna()
        invalid_mask = ~non_null.isin(allowed_set)
        invalid_count = invalid_mask.sum()
        
        passed = bool(invalid_count == 0)
        return {
            "check_name": f"{entity_name}_{column}_enum_validity",
            "dimension": "Validity",
            "entity": entity_name,
            "passed": passed,
            "violations_count": int(invalid_count),
            "unexpected_values": non_null[invalid_mask].unique().tolist()[:5],
            "severity": "P1 - High" if not passed else "PASS",
            "details": f"{invalid_count} records contain values outside allowed set." if not passed else "All values conform to authorized enum."
        }

    # ----------------------------------------------------
    # 4. Consistency Checks (Chronology & Logic)
    # ----------------------------------------------------
    @classmethod
    def check_chronology(cls, df: pd.DataFrame, earlier_col: str, later_col: str, entity_name: str) -> Dict[str, Any]:
        """Assert that earlier_col timestamp <= later_col timestamp."""
        if earlier_col not in df.columns or later_col not in df.columns:
            return {"check_name": f"{entity_name}_chronology_check", "passed": False, "violations_count": 0, "details": "Columns missing"}
        
        valid_both = df.dropna(subset=[earlier_col, later_col]).copy()
        dt_earlier = pd.to_datetime(valid_both[earlier_col], errors="coerce")
        dt_later = pd.to_datetime(valid_both[later_col], errors="coerce")
        
        valid_dates = valid_both[dt_earlier.notnull() & dt_later.notnull()]
        e_valid = dt_earlier[valid_dates.index]
        l_valid = dt_later[valid_dates.index]
        
        violations = valid_dates[e_valid > l_valid]
        v_count = len(violations)
        
        passed = bool(v_count == 0)
        return {
            "check_name": f"{entity_name}_{earlier_col}_before_{later_col}",
            "dimension": "Consistency",
            "entity": entity_name,
            "passed": passed,
            "violations_count": v_count,
            "severity": "P0 - Critical" if not passed else "PASS",
            "details": f"Chronology violation: {v_count} records show {earlier_col} > {later_col}." if not passed else f"Temporal chronology verified ({earlier_col} <= {later_col})."
        }

    # ----------------------------------------------------
    # 5. Accuracy & Numeric Range Checks
    # ----------------------------------------------------
    @classmethod
    def check_numeric_range(cls, df: pd.DataFrame, column: str, min_val: float, max_val: float, entity_name: str) -> Dict[str, Any]:
        """Verify numeric values fall within legitimate domain bounds."""
        if column not in df.columns:
            return {"check_name": f"{entity_name}_{column}_range", "passed": False, "violations_count": 0, "details": "Column missing"}
        
        series = pd.to_numeric(df[column], errors="coerce").dropna()
        out_of_bounds = series[(series < min_val) | (series > max_val)]
        v_count = len(out_of_bounds)
        
        passed = bool(v_count == 0)
        return {
            "check_name": f"{entity_name}_{column}_range_check",
            "dimension": "Accuracy",
            "entity": entity_name,
            "passed": passed,
            "violations_count": v_count,
            "outliers_sample": out_of_bounds.head(5).tolist(),
            "severity": "P1 - High" if not passed else "PASS",
            "details": f"{v_count} records outside bounds [{min_val}, {max_val}]." if not passed else f"All numeric values within valid bounds [{min_val}, {max_val}]."
        }

    # ----------------------------------------------------
    # 6. Referential Integrity (Foreign Keys)
    # ----------------------------------------------------
    @classmethod
    def check_referential_integrity(cls, child_df: pd.DataFrame, parent_df: pd.DataFrame, foreign_key: str, parent_key: str, child_name: str, parent_name: str) -> Dict[str, Any]:
        """Assert that every foreign key in child_df exists in parent_df."""
        if foreign_key not in child_df.columns or parent_key not in parent_df.columns:
            return {"check_name": f"{child_name}_to_{parent_name}_fk_check", "passed": False, "violations_count": 0, "details": "Key missing"}
        
        parent_keys = set(parent_df[parent_key].dropna().unique())
        child_series = child_df[foreign_key].dropna()
        orphans = child_series[~child_series.isin(parent_keys)]
        orphan_count = len(orphans)
        
        passed = bool(orphan_count == 0)
        return {
            "check_name": f"{child_name}_to_{parent_name}_foreign_key_integrity",
            "dimension": "Referential Integrity",
            "entity": f"{child_name} -> {parent_name}",
            "passed": passed,
            "violations_count": orphan_count,
            "orphan_samples": orphans.unique().tolist()[:5],
            "severity": "P0 - Critical" if not passed else "PASS",
            "details": f"{orphan_count} orphan records found in {child_name} referencing nonexistent {parent_key}." if not passed else f"100% referential integrity verified ({child_name}.{foreign_key} -> {parent_name}.{parent_key})."
        }
