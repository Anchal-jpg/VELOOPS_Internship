"""
VELOOP Product Analytics - Data Loader Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

import os
from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd


class DataLoader:
    """
    Robust data loader for VELOOP raw and simulated datasets.
    Preserves original files and reads sheets safely into pandas DataFrames.
    """

    DEFAULT_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

    def __init__(self, raw_data_dir: Optional[Union[str, Path]] = None):
        if raw_data_dir is None:
            self.raw_data_dir = self.DEFAULT_RAW_DIR
        else:
            self.raw_data_dir = Path(raw_data_dir)

        self.users_file = self.raw_data_dir / "VELoop_Rewards_Data_01.xlsx"
        self.behavior_file = self.raw_data_dir / "VELOOP_Simulated_User_Behavior_1000.xlsx"

        self._validate_files_exist()

    def _validate_files_exist(self) -> None:
        """Verify that source files exist before attempting to load."""
        if not self.users_file.exists():
            raise FileNotFoundError(f"Users dataset not found at: {self.users_file}")
        if not self.behavior_file.exists():
            raise FileNotFoundError(f"Behavior dataset not found at: {self.behavior_file}")

    def load_users_clean(self) -> pd.DataFrame:
        """Load clean 1000 users dataset."""
        df = pd.read_excel(self.users_file, sheet_name="Users_1000_Clean")
        # Drop accidental trailing unnamed empty columns if present
        df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
        return df

    def load_users_messy(self) -> pd.DataFrame:
        """Load messy users dataset used for data quality auditing."""
        df = pd.read_excel(self.users_file, sheet_name="Users_Messy_Audit")
        df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
        return df

    def load_sessions(self) -> pd.DataFrame:
        """Load simulated user sessions dataset."""
        return pd.read_excel(self.behavior_file, sheet_name="02_Sessions")

    def load_feature_events(self) -> pd.DataFrame:
        """Load simulated granular feature events dataset."""
        return pd.read_excel(self.behavior_file, sheet_name="03_Feature_Events")

    def load_daily_activity(self) -> pd.DataFrame:
        """Load user daily aggregated activity dataset."""
        return pd.read_excel(self.behavior_file, sheet_name="04_Daily_Activity")

    def load_task_activity(self) -> pd.DataFrame:
        """Load task activity and reward status dataset."""
        return pd.read_excel(self.behavior_file, sheet_name="05_Task_Activity")

    def load_milestones(self) -> pd.DataFrame:
        """Load milestone completions dataset."""
        return pd.read_excel(self.behavior_file, sheet_name="06_Milestones")

    def load_feature_usage_summary(self) -> pd.DataFrame:
        """Load pre-aggregated feature usage benchmark summary."""
        return pd.read_excel(self.behavior_file, sheet_name="07_Feature_Usage")

    def load_event_messy_audit(self) -> pd.DataFrame:
        """Load messy feature events dataset used for event data quality auditing."""
        return pd.read_excel(self.behavior_file, sheet_name="10_Event_Data_Quality_Audit")

    def load_all_clean_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load all core analytical tables into a single dictionary."""
        return {
            "users": self.load_users_clean(),
            "sessions": self.load_sessions(),
            "feature_events": self.load_feature_events(),
            "daily_activity": self.load_daily_activity(),
            "task_activity": self.load_task_activity(),
            "milestones": self.load_milestones(),
            "feature_usage": self.load_feature_usage_summary(),
        }


if __name__ == "__main__":
    loader = DataLoader()
    print("Testing DataLoader...")
    users = loader.load_users_clean()
    print(f"Loaded users_clean: {users.shape}")
    sessions = loader.load_sessions()
    print(f"Loaded sessions: {sessions.shape}")
    print("DataLoader test passed successfully.")

