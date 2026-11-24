"""
Unit tests for profiling modules (DatasetInspector, DuplicateAnalyzer, MissingValueAnalyzer).
"""

import sys
from pathlib import Path
import pytest

base_dir = Path(__file__).resolve().parent.parent
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from data_loader import DataLoader
from dataset_inspector import DatasetInspector
from duplicate_analysis import DuplicateAnalyzer
from missing_value_analysis import MissingValueAnalyzer
from column_summary import ColumnSummaryAnalyzer


@pytest.fixture(scope="module")
def loader():
    raw_dir = base_dir / "data" / "raw"
    return DataLoader(raw_data_dir=raw_dir)


def test_primary_key_identification(loader):
    users = loader.load_users_clean()
    inspector = DatasetInspector(users, dataset_name="users")
    pk_candidates = inspector.identify_potential_primary_keys()
    assert "user_id" in pk_candidates


def test_clean_vs_messy_duplicates(loader):
    clean = loader.load_users_clean()
    messy = loader.load_users_messy()
    analyzer = DuplicateAnalyzer(clean, dataset_name="users")
    comp = analyzer.compare_clean_vs_messy(clean, messy, id_col="user_id")
    assert comp["clean_id_duplicates"] == 0
    assert comp["messy_id_duplicates"] == 8
    assert comp["injected_duplicates"] == 8


def test_referential_integrity_sessions_to_users(loader):
    users = loader.load_users_clean()
    sessions = loader.load_sessions()
    res = DatasetInspector.check_referential_integrity(
        child_df=sessions,
        child_col="user_id",
        parent_df=users,
        parent_col="user_id"
    )
    assert res["is_valid_fk"] is True
    assert res["orphan_distinct_count"] == 0


def test_missing_value_summary(loader):
    tasks = loader.load_task_activity()
    analyzer = MissingValueAnalyzer(tasks, dataset_name="tasks")
    missing_df = analyzer.summarize_missing()
    cols_missing = list(missing_df["column_name"])
    assert "failure_reason" in cols_missing
    assert "task_completed_at" in cols_missing


def test_column_summary_numeric(loader):
    users = loader.load_users_clean()
    analyzer = ColumnSummaryAnalyzer(users, dataset_name="users")
    num_summary = analyzer.summarize_numeric_columns()
    assert "xp_balance" in list(num_summary["column_name"])
    assert "age" in list(num_summary["column_name"])

