"""
Prepare Processed Star-Schema Tables for Power BI Dashboard Suite:
- dim_users.csv
- dim_dates.csv
- fct_sessions.csv
- fct_feature_events.csv
- fct_daily_activity.csv
- fct_tasks.csv
- fct_milestones.csv
- fct_wallet_ledger.csv
- fct_withdrawals.csv
- fct_referrals.csv
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT_DIR = Path(r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics")
SRC_DIR = ROOT_DIR / "src"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data_loader import DataLoader

def prepare_tables():
    print("Loading raw source datasets...")
    dl = DataLoader()
    
    # 1. Dim Users
    df_users = dl.load_users_clean()
    df_users["registration_datetime"] = pd.to_datetime(df_users["registration_datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_users["last_login_datetime"] = pd.to_datetime(df_users["last_login_datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    users_csv = PROCESSED_DIR / "dim_users.csv"
    df_users.to_csv(users_csv, index=False)
    print(f"Saved: {users_csv} ({len(df_users)} records)")

    # 2. Dim Dates
    min_date = pd.Timestamp("2026-01-01")
    max_date = pd.Timestamp("2026-12-31")
    date_range = pd.date_range(min_date, max_date, freq="D")
    df_dates = pd.DataFrame({"date_key": date_range.strftime("%Y%m%d").astype(int), "calendar_date": date_range.strftime("%Y-%m-%d")})
    df_dates["year"] = date_range.year
    df_dates["quarter"] = "Q" + date_range.quarter.astype(str)
    df_dates["month_num"] = date_range.month
    df_dates["month_name"] = date_range.strftime("%B")
    df_dates["month_year"] = date_range.strftime("%b %Y")
    df_dates["day_of_month"] = date_range.day
    df_dates["day_of_week"] = date_range.day_name()
    df_dates["day_of_week_num"] = date_range.dayofweek + 1
    df_dates["is_weekend"] = df_dates["day_of_week_num"].isin([6, 7])
    dates_csv = PROCESSED_DIR / "dim_dates.csv"
    df_dates.to_csv(dates_csv, index=False)
    print(f"Saved: {dates_csv} ({len(df_dates)} records)")

    # 3. Fact Sessions
    df_sessions = dl.load_sessions()
    df_sessions["session_start"] = pd.to_datetime(df_sessions["session_start"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_sessions["session_end"] = pd.to_datetime(df_sessions["session_end"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_sessions["session_date"] = pd.to_datetime(df_sessions["session_start"]).dt.strftime("%Y-%m-%d")
    sessions_csv = PROCESSED_DIR / "fct_sessions.csv"
    df_sessions.to_csv(sessions_csv, index=False)
    print(f"Saved: {sessions_csv} ({len(df_sessions)} records)")

    # 4. Fact Feature Events
    df_events = dl.load_feature_events()
    df_events["event_datetime"] = pd.to_datetime(df_events["event_datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_events["event_date"] = pd.to_datetime(df_events["event_datetime"]).dt.strftime("%Y-%m-%d")
    events_csv = PROCESSED_DIR / "fct_feature_events.csv"
    df_events.to_csv(events_csv, index=False)
    print(f"Saved: {events_csv} ({len(df_events)} records)")

    # 5. Fact Daily Activity
    df_daily = dl.load_daily_activity()
    df_daily["activity_date"] = pd.to_datetime(df_daily["activity_date"]).dt.strftime("%Y-%m-%d")
    daily_csv = PROCESSED_DIR / "fct_daily_activity.csv"
    df_daily.to_csv(daily_csv, index=False)
    print(f"Saved: {daily_csv} ({len(df_daily)} records)")

    # 6. Fact Tasks
    df_tasks = dl.load_task_activity()
    df_tasks["task_viewed_at"] = pd.to_datetime(df_tasks["task_viewed_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_tasks["task_started_at"] = pd.to_datetime(df_tasks["task_started_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_tasks["task_completed_at"] = pd.to_datetime(df_tasks["task_completed_at"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_tasks["task_date"] = pd.to_datetime(df_tasks["task_started_at"]).dt.strftime("%Y-%m-%d")
    tasks_csv = PROCESSED_DIR / "fct_tasks.csv"
    df_tasks.to_csv(tasks_csv, index=False)
    print(f"Saved: {tasks_csv} ({len(df_tasks)} records)")

    # 7. Fact Milestones
    df_milestones = dl.load_milestones()
    df_milestones["milestone_datetime"] = pd.to_datetime(df_milestones["milestone_datetime"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_milestones["milestone_date"] = pd.to_datetime(df_milestones["milestone_datetime"]).dt.strftime("%Y-%m-%d")
    milestones_csv = PROCESSED_DIR / "fct_milestones.csv"
    df_milestones.to_csv(milestones_csv, index=False)
    print(f"Saved: {milestones_csv} ({len(df_milestones)} records)")

    # 8. Fact Wallet Ledger (Derived / Modeled Benchmark)
    ledger_records = []
    tx_counter = 1
    # Completed tasks earn points (50 pts per completed task standard)
    for idx, row in df_tasks[df_tasks["task_status"] == "Completed"].iterrows():
        ledger_records.append({
            "transaction_id": f"WLTX{tx_counter:08d}",
            "wallet_id": f"WLT_{row['user_id']}",
            "user_id": row["user_id"],
            "transaction_type": "TASK_REWARD",
            "points_amount": 50,
            "direction": "CREDIT",
            "transaction_timestamp": row["task_completed_at"],
            "transaction_date": row["task_date"],
            "source_reference_id": row["task_id"],
            "status": "SETTLED"
        })
        tx_counter += 1
        
    for idx, row in df_milestones.iterrows():
        # Points from milestone value
        pts = int(row["milestone_value"]) if str(row["milestone_value"]).isdigit() else 25
        ledger_records.append({
            "transaction_id": f"WLTX{tx_counter:08d}",
            "wallet_id": f"WLT_{row['user_id']}",
            "user_id": row["user_id"],
            "transaction_type": "MILESTONE_BONUS",
            "points_amount": pts,
            "direction": "CREDIT",
            "transaction_timestamp": row["milestone_datetime"],
            "transaction_date": row["milestone_date"],
            "source_reference_id": f"MLS_{idx}",
            "status": "SETTLED"
        })
        tx_counter += 1
    
    df_ledger = pd.DataFrame(ledger_records)
    ledger_csv = PROCESSED_DIR / "fct_wallet_ledger.csv"
    df_ledger.to_csv(ledger_csv, index=False)
    print(f"Saved: {ledger_csv} ({len(df_ledger)} records)")

    # 9. Fact Withdrawals (Modeled Benchmark for Withdrawal Analytics Dashboard)
    np.random.seed(42)
    eligible_users = df_users[df_users["xp_balance"] >= 200].copy()
    withdrawal_records = []
    w_counter = 1
    methods = ["UPI", "PayPal", "Bank Transfer", "Amazon Gift Card"]
    method_weights = [0.55, 0.20, 0.15, 0.10]
    
    for idx, user in eligible_users.iterrows():
        num_w = np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])
        user_reg = pd.to_datetime(user["registration_datetime"])
        for i in range(num_w):
            req_time = user_reg + pd.Timedelta(days=int(np.random.randint(15, 90)), hours=int(np.random.randint(8, 20)))
            amount_pts = int(np.random.choice([200, 500, 1000, 2000], p=[0.4, 0.35, 0.2, 0.05]))
            method = np.random.choice(methods, p=method_weights)
            
            # Status: 85% Completed, 10% Rejected, 5% Pending
            status = np.random.choice(["Completed", "Rejected", "Pending"], p=[0.85, 0.10, 0.05])
            tat_hours = round(float(np.random.exponential(scale=6.5) + 0.5), 1) if status == "Completed" else None
            rej_reason = np.random.choice(["Invalid KYC / UPI ID", "Suspicious Multi-Account", "Daily Payout Limit Exceeded"], p=[0.5, 0.3, 0.2]) if status == "Rejected" else None
            
            withdrawal_records.append({
                "withdrawal_id": f"WTH{w_counter:07d}",
                "user_id": user["user_id"],
                "points_redeemed": amount_pts,
                "cash_equivalent_inr": amount_pts * 0.10, # 10 pts = 1 INR
                "payout_method": method,
                "status": status,
                "requested_at": req_time.strftime("%Y-%m-%d %H:%M:%S"),
                "withdrawal_date": req_time.strftime("%Y-%m-%d"),
                "turnaround_time_hours": tat_hours,
                "rejection_reason": rej_reason
            })
            w_counter += 1
            
    df_withdrawals = pd.DataFrame(withdrawal_records)
    withdrawals_csv = PROCESSED_DIR / "fct_withdrawals.csv"
    df_withdrawals.to_csv(withdrawals_csv, index=False)
    print(f"Saved: {withdrawals_csv} ({len(df_withdrawals)} records)")

    # 10. Fact Referrals (Modeled Graph Edge Network)
    ref_records = []
    r_counter = 1
    referral_users = df_users[df_users["referral_source_detail"].notnull()]
    available_referrers = df_users[df_users["account_status"] == "Active"]["user_id"].tolist()
    
    for idx, invitee in referral_users.iterrows():
        referrer_id = np.random.choice(available_referrers)
        while referrer_id == invitee["user_id"]:
            referrer_id = np.random.choice(available_referrers)
            
        share_channel = np.random.choice(["WhatsApp", "Telegram", "Instagram", "Direct Link", "SMS"], p=[0.45, 0.25, 0.15, 0.10, 0.05])
        is_activated = invitee["is_active_7d"]
        bounty_pts = 100 if is_activated else 0
        
        ref_records.append({
            "referral_id": f"REF{r_counter:07d}",
            "referrer_id": referrer_id,
            "invitee_id": invitee["user_id"],
            "referral_code_used": invitee["referral_source_detail"],
            "share_channel": share_channel,
            "referral_date": pd.to_datetime(invitee["registration_datetime"]).strftime("%Y-%m-%d"),
            "status": "Activated" if is_activated else "Registered",
            "reward_points_awarded": bounty_pts
        })
        r_counter += 1
        
    df_referrals = pd.DataFrame(ref_records)
    referrals_csv = PROCESSED_DIR / "fct_referrals.csv"
    df_referrals.to_csv(referrals_csv, index=False)
    print(f"Saved: {referrals_csv} ({len(df_referrals)} records)")
    print("All 10 star-schema tables successfully prepared in data/processed/!")

if __name__ == "__main__":
    prepare_tables()
