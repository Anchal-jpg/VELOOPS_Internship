"""
Script to generate Step 5 Excel Workbook:
Earning_Reward_Analytics_Specification.xlsx
"""

import sys
from pathlib import Path
import openpyxl

base_dir = Path(r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics")
sys.path.append(str(base_dir / "src"))
from report_utils import ReportUtils

def save_styled_workbook(wb: openpyxl.Workbook, file_path: Path):
    for sheet_name in wb.sheetnames:
        ReportUtils.apply_excel_styling(wb, sheet_name)
    wb.save(file_path)
    print(f"Saved: {file_path}")

def create_earning_reward_specification():
    wb = openpyxl.Workbook()
    
    # Sheet 1: Task Lifecycle Model
    ws1 = wb.active
    ws1.title = "Task_Lifecycle_Model"
    headers1 = [
        "Stage_Index", "Lifecycle_Stage", "Event_Trigger", "Actor",
        "System_Action", "Prerequisites", "Next_Allowed_Stages", "Telemetry_Status"
    ]
    ws1.append(headers1)
    stages = [
        (1, "Task Discovery", "task_board_viewed", "User", "Fetches active offers matching user demographic & country", "User in Active_Onboarded state", "Task Opened, Task Abandoned", "Proposed Event"),
        (2, "Task Opened", "task_detail_viewed", "User", "Renders offer instructions, reward amount, requirements", "Task active in catalog", "Task Started, Task Closed", "Proposed Event"),
        (3, "Task Started", "task_started", "User", "Generates activity_id; redirects to offer/ad URL", "Cooldown timer clear; daily cap unreached", "Task Completed, Task Failed, Task Abandoned", "Available (05_Task_Activity)"),
        (4, "Task Execution", "task_in_progress", "User / SDK", "Runs timer / tracks progress / plays video", "Active session connection", "Task Completed, Task Timeout, User Exited", "Available in ad/spin events"),
        (5, "Task Completion", "task_completed", "User / Partner", "Receives user completion trigger or partner postback", "Proof of action submitted", "Validation Pending", "Available (05_Task_Activity)"),
        (6, "Validation Processing", "task_validation_executed", "Backend Rules", "Verifies completion rules (duration, anti-fraud, postback signature)", "Completion proof present", "Validation Passed, Validation Failed", "Proposed Event"),
        (7, "Reward Pending", "reward_pending_queued", "Ledger Engine", "Places credit into escrow pending final verification", "Validation Passed", "Reward Credited, Reward Cancelled", "Available (reward_status)"),
        (8, "Reward Credited", "reward_credited", "Ledger Engine", "Appends credit row to rewards_ledger; increments wallet balance", "Escrow verification cleared", "Reward Reversed, Reward Corrected", "Available (reward_status)"),
        (9, "Reward Reversed", "reward_reversed", "Admin / Anti-Fraud", "Debits user balance due to chargeback or detected spoofing", "Post-credit fraud flag raised", "None (Final State)", "Proposed Event (Critical)"),
        (10, "Reward Corrected", "reward_corrected", "Ledger Engine", "Adjusts credit amount due to rate recalculation or tier bonus", "Accounting discrepancy resolved", "None (Final State)", "Proposed Event"),
    ]
    for row in stages:
        ws1.append(row)
        
    # Sheet 2: Decoupled Rewards Ledger Schema
    ws2 = wb.create_sheet(title="Decoupled_Rewards_Ledger")
    headers2 = [
        "Field_Name", "Data_Type", "Requirement", "Default_Value",
        "Validation_Rule", "Source_Component", "Analytical_Use_Case"
    ]
    ws2.append(headers2)
    ledger_fields = [
        ("reward_transaction_id", "VARCHAR(20)", "Required", "None", "Primary Key; Regex ^RWD\d{10}$", "Ledger Engine", "Unique financial identifier for every reward distribution"),
        ("activity_id", "VARCHAR(15)", "Optional", "NULL", "Foreign Key -> task_activity.activity_id", "Task Service", "Binds reward directly to operational task attempt"),
        ("user_id", "VARCHAR(11)", "Required", "None", "Foreign Key -> users.user_id", "User Service", "User balance recipient join key"),
        ("source_feature", "VARCHAR(50)", "Required", "None", "Enum: Watch_Ads, App_Task, Survey, Streak, Mission, Tap, Spin", "Event Engine", "Financial revenue and cost attribution by feature"),
        ("currency_type", "VARCHAR(10)", "Required", "VE", "Enum: VE, XP, Gem, Token, Spin", "Ledger Engine", "Separates non-monetary XP from redeemable tokens/VEs"),
        ("reward_amount", "DECIMAL(12,4)", "Required", "None", "Strictly positive number (> 0.0000)", "Ledger Engine", "Exact currency quantum credited to wallet"),
        ("transaction_type", "VARCHAR(20)", "Required", "Credit", "Enum: Credit, Debit_Reversal, Adjustment_Add, Adjustment_Sub", "Ledger Engine", "Accounting nature of ledger entry"),
        ("reward_status", "VARCHAR(20)", "Required", "Pending", "Enum: Pending, Credited, Reversed, Corrected, Cancelled", "Ledger Engine", "Escrow and fulfillment lifecycle status"),
        ("created_at", "TIMESTAMP", "Required", "CURRENT_TIMESTAMP", "Valid past/current timestamp", "Database Server", "Transaction initiation timestamp for daily ledger closing"),
        ("credited_at", "TIMESTAMP", "Optional", "NULL", ">= created_at; populated when Credited", "Ledger Engine", "Measures reward credit fulfillment latency"),
        ("reversal_reason", "VARCHAR(100)", "Optional", "NULL", "Non-null if status in ('Reversed', 'Cancelled')", "Risk Engine", "Categorizes chargeback or fraud origin"),
        ("idempotency_hash", "VARCHAR(64)", "Required", "None", "SHA-256 hash of (user_id, activity_id, currency, amount)", "Client / Ingestion", "Prevents duplicate reward credits on network retries"),
        ("balance_after", "DECIMAL(12,4)", "Required", "None", "User running currency balance post-transaction", "Ledger Engine", "Audit trail for balance verification and reconciliation"),
    ]
    for row in ledger_fields:
        ws2.append(row)
        
    # Sheet 3: Failure Reason Taxonomy
    ws3 = wb.create_sheet(title="Failure_Reason_Taxonomy")
    headers3 = [
        "Failure_Code", "Observed_Reason", "Frequency_in_Dataset", "Percentage_of_Failed",
        "Primary_Category", "Technical_Root_Cause", "Third_Party_Dependency", "Remediation_Strategy"
    ]
    ws3.append(headers3)
    failures = [
        ("FAIL-001", "Validation failed", 732, "20.78%", "Quality / Fraud", "Completion criteria not satisfied (e.g. gameplay level unmet, proxy detected)", "Internal Rules / Offerwall", "Display clear rejection guidelines to user to set expectations"),
        ("FAIL-002", "Task unavailable", 722, "20.50%", "Availability", "Ad inventory depleted, survey quota filled, or campaign paused by advertiser", "Ad Network / Survey API", "Real-time offer inventory caching to remove dead links from task board"),
        ("FAIL-003", "Timeout", 710, "20.16%", "Infrastructure", "User exceeded max time limit or network connectivity lost during execution", "Client Network / SDK", "Grace period buffer and offline state caching with reconnect retry"),
        ("FAIL-004", "Incomplete action", 706, "20.05%", "User Behavior", "User closed partner app before reaching event checkpoint or skipped survey section", "User Attention", "Progress milestone bar indicating percent of task completed"),
        ("FAIL-005", "User exited", 701, "19.90%", "User Behavior", "User explicitly tapped back/cancel button to abandon task attempt", "UX Friction", "Analyze task onboarding friction; reduce intrusive permission demands"),
        ("FAIL-006", "S2S Postback Signature Invalid", 0, "0.00% (Proposed)", "Security", "HMAC SHA-256 signature mismatch on advertiser server-to-server callback", "Offerwall Partner", "Rotate partner API secrets and reject spoofed credit calls"),
        ("FAIL-007", "Ad Player Stream Interrupted", 0, "0.00% (Proposed)", "SDK / Media", "Video buffering stall exceeding 15 seconds causing player crash", "Google AdMob / Unity Ads", "Preload rewarded video assets during earlier session screens"),
    ]
    for row in failures:
        ws3.append(row)
        
    # Sheet 4: Reward KPI Catalogue
    ws4 = wb.create_sheet(title="Reward_KPI_Catalogue")
    headers4 = [
        "KPI_ID", "Metric_Name", "Formula / Calculation",
        "Target_Benchmark", "Data_Source_Tables", "Business_Significance"
    ]
    ws4.append(headers4)
    kpis = [
        ("KPI-RWD-01", "Task Completion Rate", "COUNT(Completed Tasks) / COUNT(Started Tasks)", "55.0% - 65.0%", "task_activity", "Core measure of user task execution efficiency"),
        ("KPI-RWD-02", "Task Failure Rate", "COUNT(Failed Tasks) / COUNT(Started Tasks)", "< 15.0%", "task_activity", "Health indicator of offer inventory and partner SDK stability"),
        ("KPI-RWD-03", "Task Abandonment Rate", "COUNT(Abandoned Tasks) / COUNT(Started Tasks)", "< 20.0%", "task_activity", "UX friction metric indicating unengaging or confusing tasks"),
        ("KPI-RWD-04", "Reward Credit Velocity", "AVG(credited_at - task_completed_at)", "< 5 Seconds", "task_activity, rewards_ledger", "Instant reward feedback driving dopamine and D1 retention"),
        ("KPI-RWD-05", "Reward Reversal Rate", "COUNT(Reversed Rewards) / COUNT(Total Credited Rewards)", "< 1.5%", "rewards_ledger", "Direct measure of advertiser chargebacks and bot fraud"),
        ("KPI-RWD-06", "Revenue to Reward Ratio (RRR)", "Partner Revenue ($) / Virtual Currency Cost ($)", ">= 2.5x", "financial_marts, rewards_ledger", "Monetization margin ensuring platform unit economics remain positive"),
        ("KPI-RWD-07", "Average Daily Earning Per Active User", "SUM(Virtual Units Credited) / DAU", "Stable Growth", "rewards_ledger, daily_activity", "Tracks user earning power and prevents virtual inflation runaway"),
    ]
    for row in kpis:
        ws4.append(row)
        
    file_path = base_dir / "documentation" / "Earning_Reward_Analytics_Specification.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "Earning_Reward_Analytics_Specification.xlsx")

if __name__ == "__main__":
    print("Generating Step 5 Excel Workbook...")
    create_earning_reward_specification()
    print("Step 5 Excel Workbook generated successfully!")

