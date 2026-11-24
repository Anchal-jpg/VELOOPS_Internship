"""
Unit tests for DataValidator module.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

base_dir = Path(__file__).resolve().parent.parent
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from data_loader import DataLoader
from data_validation import DataValidator


@pytest.fixture(scope="module")
def loader():
    raw_dir = base_dir / "data" / "raw"
    return DataLoader(raw_data_dir=raw_dir)


def test_validate_clean_users(loader):
    df = loader.load_users_clean()
    results = DataValidator.validate_users(df)
    for res in results:
        assert res["passed"] is True, f"Rule failed: {res['rule']} with {res['violations_count']} violations"


def test_validate_clean_sessions(loader):
    df = loader.load_sessions()
    results = DataValidator.validate_sessions(df)
    for res in results:
        assert res["passed"] is True, f"Rule failed: {res['rule']} with {res['violations_count']} violations"


def test_validate_clean_tasks(loader):
    df = loader.load_task_activity()
    results = DataValidator.validate_tasks(df)
    for res in results:
        assert res["passed"] is True, f"Rule failed: {res['rule']} with {res['violations_count']} violations"


def test_validator_catches_synthetic_violation():
    # Construct synthetic bad dataframe
    bad_df = pd.DataFrame({
        "user_id": ["INVALID_ID", "VLUSR000002"],
        "registration_datetime": [pd.Timestamp("2026-05-10"), pd.Timestamp("2026-05-10")],
        "last_login_datetime": [pd.Timestamp("2026-05-01"), pd.Timestamp("2026-05-15")], # Row 0 has login before reg
        "age": [10, 25], # Row 0 has age < 13
        "xp_balance": [-50, 100], # Row 0 has negative balance
    })
    results = DataValidator.validate_users(bad_df)
    failed_rules = [r["rule"] for r in results if not r["passed"]]
    assert "user_id_format_check" in failed_rules
    assert "user_registration_before_last_login" in failed_rules
    assert "user_age_reasonable_bounds" in failed_rules
    assert "user_xp_balance_non_negative" in failed_rules

