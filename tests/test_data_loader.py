"""
Unit tests for DataLoader module.
"""

import sys
from pathlib import Path
import pytest

base_dir = Path(__file__).resolve().parent.parent
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from data_loader import DataLoader


@pytest.fixture(scope="module")
def loader():
    raw_dir = base_dir / "data" / "raw"
    return DataLoader(raw_data_dir=raw_dir)


def test_users_clean_shape(loader):
    df = loader.load_users_clean()
    assert len(df) == 1000, f"Expected 1000 users, got {len(df)}"
    assert "user_id" in df.columns
    assert "email" in df.columns
    assert "xp_balance" in df.columns


def test_users_messy_shape(loader):
    df = loader.load_users_messy()
    assert len(df) == 1008, f"Expected 1008 messy users, got {len(df)}"
    assert "data_environment" in df.columns


def test_sessions_shape(loader):
    df = loader.load_sessions()
    assert len(df) == 7913, f"Expected 7913 sessions, got {len(df)}"
    assert "session_id" in df.columns
    assert "session_duration_seconds" in df.columns


def test_feature_events_shape(loader):
    df = loader.load_feature_events()
    assert len(df) == 35704, f"Expected 35704 events, got {len(df)}"
    assert "event_id" in df.columns
    assert "feature_name" in df.columns


def test_task_activity_shape(loader):
    df = loader.load_task_activity()
    assert len(df) == 9846, f"Expected 9846 tasks, got {len(df)}"
    assert "activity_id" in df.columns
    assert "task_status" in df.columns
    assert "reward_status" in df.columns


def test_milestones_shape(loader):
    df = loader.load_milestones()
    assert len(df) == 4799, f"Expected 4799 milestones, got {len(df)}"
    assert "milestone_type" in df.columns

