"""
Unit and Integration Tests for VELOOP Enterprise Data Quality Suite.
Phase 5 (Days 22-23) Automated Quality Verification.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

base_dir = Path(__file__).resolve().parent.parent
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from data_loader import DataLoader
from data_quality_rules import DataQualityRulesEngine


@pytest.fixture(scope="module")
def loader():
    raw_dir = base_dir / "data" / "raw"
    return DataLoader(raw_data_dir=raw_dir)


@pytest.fixture(scope="module")
def clean_users(loader):
    return loader.load_users_clean()


@pytest.fixture(scope="module")
def messy_users(loader):
    return loader.load_users_messy()


@pytest.fixture(scope="module")
def sessions(loader):
    return loader.load_sessions()


@pytest.fixture(scope="module")
def tasks(loader):
    return loader.load_task_activity()


@pytest.fixture(scope="module")
def events(loader):
    return loader.load_feature_events()


# ====================================================================
# 1. Clean Dataset Assertions (Must Pass 100%)
# ====================================================================

def test_clean_users_mandatory_nulls(clean_users):
    """Assert clean users table has 0 nulls in mandatory core fields."""
    mandatory_cols = [
        "user_id", "full_name", "email", "age", "gender", "state",
        "city", "registration_datetime", "acquisition_source", "primary_device",
        "platform", "account_status", "email_verification_status", "onboarding_status",
        "lifetime_sessions", "active_days", "xp_balance", "country"
    ]
    res = DataQualityRulesEngine.check_mandatory_nulls(clean_users, mandatory_cols, "clean_users")
    assert res["passed"] is True, f"Clean users failed null check: {res['details']}"


def test_clean_users_uniqueness(clean_users):
    """Assert clean users primary key user_id and email are strictly unique."""
    id_res = DataQualityRulesEngine.check_uniqueness(clean_users, "user_id", "clean_users")
    assert id_res["passed"] is True, f"Clean users duplicate IDs found: {id_res['violations_count']}"

    email_res = DataQualityRulesEngine.check_uniqueness(clean_users, "email", "clean_users")
    assert email_res["passed"] is True, f"Clean users duplicate emails found: {email_res['violations_count']}"


def test_clean_users_id_and_email_regex(clean_users):
    """Assert clean users match ID and email syntax patterns."""
    id_res = DataQualityRulesEngine.check_regex_format(clean_users, "user_id", DataQualityRulesEngine.USER_ID_REGEX, "clean_users")
    assert id_res["passed"] is True, f"Clean user_id regex violation: {id_res['details']}"

    email_res = DataQualityRulesEngine.check_regex_format(clean_users, "email", DataQualityRulesEngine.EMAIL_REGEX, "clean_users")
    assert email_res["passed"] is True, f"Clean email regex violation: {email_res['details']}"


def test_clean_users_datetime_validity(clean_users):
    """Assert all timestamps in clean users parse successfully."""
    reg_res = DataQualityRulesEngine.check_datetime_parseability(clean_users, "registration_datetime", "clean_users")
    assert reg_res["passed"] is True, f"Clean registration date failed: {reg_res['details']}"

    log_res = DataQualityRulesEngine.check_datetime_parseability(clean_users, "last_login_datetime", "clean_users")
    assert log_res["passed"] is True, f"Clean last login date failed: {log_res['details']}"


def test_clean_users_chronology(clean_users):
    """Assert registration_datetime <= last_login_datetime across clean users."""
    chrono_res = DataQualityRulesEngine.check_chronology(clean_users, "registration_datetime", "last_login_datetime", "clean_users")
    assert chrono_res["passed"] is True, f"Clean users chronology error: {chrono_res['details']}"


def test_clean_users_numeric_ranges(clean_users):
    """Assert user age and xp balance adhere to valid domain ranges."""
    age_res = DataQualityRulesEngine.check_numeric_range(clean_users, "age", 13, 100, "clean_users")
    assert age_res["passed"] is True, f"Clean users age out of bounds: {age_res['details']}"

    xp_res = DataQualityRulesEngine.check_numeric_range(clean_users, "xp_balance", 0, 1000000, "clean_users")
    assert xp_res["passed"] is True, f"Clean users negative xp balance: {xp_res['details']}"


# ====================================================================
# 2. Messy Dataset Assertions (Demonstrates Rule Enforcement)
# ====================================================================

def test_messy_users_detects_duplicates(messy_users):
    """Verify that the engine accurately detects the 8 duplicate rows in messy audit data."""
    id_res = DataQualityRulesEngine.check_uniqueness(messy_users, "user_id", "messy_users")
    assert not id_res["passed"]
    assert id_res["violations_count"] == 16  # 8 duplicate pairs = 16 rows involved
    assert len(id_res["duplicate_keys"]) == 8


def test_messy_users_detects_unparseable_datetime(messy_users):
    """Verify that the engine accurately flags the invalid date string '2026-14-02 12:00'."""
    reg_res = DataQualityRulesEngine.check_datetime_parseability(messy_users, "registration_datetime", "messy_users")
    assert reg_res["passed"] is False
    assert reg_res["violations_count"] == 1
    assert "2026-14-02 12:00" in reg_res["sample_invalids"]


def test_messy_users_detects_missing_mandatory_fields(messy_users):
    """Verify that the engine accurately detects null values in mandatory fields."""
    mandatory_cols = ["age", "gender", "city", "registration_datetime", "acquisition_source", "primary_device"]
    res = DataQualityRulesEngine.check_mandatory_nulls(messy_users, mandatory_cols, "messy_users")
    assert res["passed"] is False
    assert res["violations_count"] >= 5
    assert "age" in res["failing_columns"]
    assert "city" in res["failing_columns"]


# ====================================================================
# 3. Cross-Dataset Referential Integrity
# ====================================================================

def test_referential_integrity_sessions_to_users(sessions, clean_users):
    """Assert 100% of session user_ids exist in the clean users master table."""
    res = DataQualityRulesEngine.check_referential_integrity(
        child_df=sessions, parent_df=clean_users,
        foreign_key="user_id", parent_key="user_id",
        child_name="sessions", parent_name="users"
    )
    assert res["passed"] is True, f"Found orphan sessions: {res['details']}"


def test_referential_integrity_tasks_to_users(tasks, clean_users):
    """Assert 100% of task user_ids exist in the clean users master table."""
    res = DataQualityRulesEngine.check_referential_integrity(
        child_df=tasks, parent_df=clean_users,
        foreign_key="user_id", parent_key="user_id",
        child_name="tasks", parent_name="users"
    )
    assert res["passed"] is True, f"Found orphan tasks: {res['details']}"


def test_referential_integrity_events_to_users(events, clean_users):
    """Assert 100% of feature event user_ids exist in the clean users master table."""
    res = DataQualityRulesEngine.check_referential_integrity(
        child_df=events, parent_df=clean_users,
        foreign_key="user_id", parent_key="user_id",
        child_name="feature_events", parent_name="users"
    )
    assert res["passed"] is True, f"Found orphan events: {res['details']}"
