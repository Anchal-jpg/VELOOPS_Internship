"""
VELOOP Product Analytics - Data Validation Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np


class DataValidator:
    """
    Validates domain business rules, temporal ordering, and integrity constraints
    across VELOOP entities.
    """

    @staticmethod
    def validate_users(users_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Validate integrity constraints on the Users entity."""
        results = []

        # Rule 1: user_id format
        invalid_ids = users_df[~users_df["user_id"].astype(str).str.match(r"^VLUSR\d{6}$")]
        results.append({
            "rule": "user_id_format_check",
            "entity": "users",
            "passed": len(invalid_ids) == 0,
            "violations_count": len(invalid_ids),
            "severity": "CRITICAL",
            "description": r"User ID must match regex ^VLUSR\d{6}$",
        })

        # Rule 2: Registration <= Last Login
        if "registration_datetime" in users_df.columns and "last_login_datetime" in users_df.columns:
            has_both = users_df.dropna(subset=["registration_datetime", "last_login_datetime"])
            reg_dt = pd.to_datetime(has_both["registration_datetime"])
            login_dt = pd.to_datetime(has_both["last_login_datetime"])
            chronology_violations = has_both[reg_dt > login_dt]
            results.append({
                "rule": "user_registration_before_last_login",
                "entity": "users",
                "passed": len(chronology_violations) == 0,
                "violations_count": len(chronology_violations),
                "severity": "HIGH",
                "description": "Registration timestamp cannot be after last login timestamp",
            })

        # Rule 3: Age bounds check (e.g. 13 to 100)
        if "age" in users_df.columns:
            valid_age = users_df["age"].dropna()
            age_violations = valid_age[(valid_age < 13) | (valid_age > 100)]
            results.append({
                "rule": "user_age_reasonable_bounds",
                "entity": "users",
                "passed": len(age_violations) == 0,
                "violations_count": len(age_violations),
                "severity": "MEDIUM",
                "description": "User age must fall between 13 and 100",
            })

        # Rule 4: XP Balance non-negative
        if "xp_balance" in users_df.columns:
            valid_xp = users_df["xp_balance"].dropna()
            xp_violations = valid_xp[valid_xp < 0]
            results.append({
                "rule": "user_xp_balance_non_negative",
                "entity": "users",
                "passed": len(xp_violations) == 0,
                "violations_count": len(xp_violations),
                "severity": "HIGH",
                "description": "XP balance must never be negative",
            })

        return results

    @staticmethod
    def validate_sessions(sessions_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Validate integrity constraints on the Sessions entity."""
        results = []

        # Rule 1: session_id format
        invalid_ids = sessions_df[~sessions_df["session_id"].astype(str).str.match(r"^SESS\d{7}$")]
        results.append({
            "rule": "session_id_format_check",
            "entity": "sessions",
            "passed": len(invalid_ids) == 0,
            "violations_count": len(invalid_ids),
            "severity": "CRITICAL",
            "description": r"Session ID must match regex ^SESS\d{7}$",
        })

        # Rule 2: session_start <= session_end
        s_start = pd.to_datetime(sessions_df["session_start"])
        s_end = pd.to_datetime(sessions_df["session_end"])
        chrono_violations = sessions_df[s_start > s_end]
        results.append({
            "rule": "session_start_before_end",
            "entity": "sessions",
            "passed": len(chrono_violations) == 0,
            "violations_count": len(chrono_violations),
            "severity": "CRITICAL",
            "description": "Session start timestamp must be <= session end timestamp",
        })

        # Rule 3: duration match
        calc_duration = (s_end - s_start).dt.total_seconds()
        duration_diff = (sessions_df["session_duration_seconds"] - calc_duration).abs()
        mismatch = sessions_df[duration_diff > 2]  # tolerance of 2 seconds
        results.append({
            "rule": "session_duration_consistency",
            "entity": "sessions",
            "passed": len(mismatch) == 0,
            "violations_count": len(mismatch),
            "severity": "MEDIUM",
            "description": "Recorded session duration must match end - start within 2s tolerance",
        })

        return results

    @staticmethod
    def validate_tasks(tasks_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Validate integrity constraints on the Task Activity entity."""
        results = []

        # Rule 1: Task status enums
        allowed_statuses = {"Completed", "Abandoned", "Failed", "Pending"}
        invalid_statuses = tasks_df[~tasks_df["task_status"].isin(allowed_statuses)]
        results.append({
            "rule": "task_status_enum_validity",
            "entity": "task_activity",
            "passed": len(invalid_statuses) == 0,
            "violations_count": len(invalid_statuses),
            "severity": "HIGH",
            "description": f"Task status must be in {allowed_statuses}",
        })

        # Rule 2: Completed tasks must have completed_at timestamp
        completed = tasks_df[tasks_df["task_status"] == "Completed"]
        missing_comp_time = completed[completed["task_completed_at"].isnull()]
        results.append({
            "rule": "completed_task_has_completion_time",
            "entity": "task_activity",
            "passed": len(missing_comp_time) == 0,
            "violations_count": len(missing_comp_time),
            "severity": "HIGH",
            "description": "Completed tasks must have a valid task_completed_at timestamp",
        })

        # Rule 3: Completed tasks must have reward_status == 'Credited'
        completed_uncredited = completed[completed["reward_status"] != "Credited"]
        results.append({
            "rule": "completed_task_reward_credited",
            "entity": "task_activity",
            "passed": len(completed_uncredited) == 0,
            "violations_count": len(completed_uncredited),
            "severity": "HIGH",
            "description": "Completed tasks in current simulated data should be Credited",
        })

        # Rule 4: Failed tasks must have failure_reason
        failed = tasks_df[tasks_df["task_status"] == "Failed"]
        missing_reason = failed[failed["failure_reason"].isnull()]
        results.append({
            "rule": "failed_task_has_failure_reason",
            "entity": "task_activity",
            "passed": len(missing_reason) == 0,
            "violations_count": len(missing_reason),
            "severity": "MEDIUM",
            "description": "Failed tasks should specify a non-null failure reason",
        })

        return results
