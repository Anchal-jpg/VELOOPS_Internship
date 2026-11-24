"""
Script to generate Step 6 Excel Workbooks:
1. Wallet_Analytics_Specification.xlsx
2. Withdrawal_Analytics_Specification.xlsx
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

# ==============================================================================
# 1. Wallet_Analytics_Specification.xlsx
# ==============================================================================
def create_wallet_specification():
    wb = openpyxl.Workbook()
    
    # Sheet 1: Wallet Transaction Schema
    ws1 = wb.active
    ws1.title = "Wallet_Transaction_Schema"
    headers1 = [
        "Field_Name", "Data_Type", "Requirement", "Default_Value",
        "Validation_Rule", "Source_Component", "Analytical_Use_Case"
    ]
    ws1.append(headers1)
    fields = [
        ("transaction_id", "VARCHAR(24)", "Required", "None", "Primary Key; Regex ^WLT\d{12}$", "Wallet Microservice", "Unique identifier for every balance mutation"),
        ("wallet_id", "VARCHAR(20)", "Required", "None", "Foreign Key -> user_wallets.wallet_id", "Wallet Microservice", "Groups multiple currency accounts for a user"),
        ("user_id", "VARCHAR(11)", "Required", "None", "Foreign Key -> users.user_id", "User Service", "Direct join key to user demographic profile"),
        ("transaction_type", "VARCHAR(30)", "Required", "None", "Enum: CREDIT_REWARD, DEBIT_WITHDRAWAL, etc.", "Ledger Engine", "Classifies economic nature of fund movement"),
        ("currency", "VARCHAR(10)", "Required", "VE", "Enum: VE, XP, GEM, TOKEN, SPIN", "Ledger Engine", "Identifies specific virtual or liquid asset"),
        ("amount", "DECIMAL(14,4)", "Required", "None", "Strictly positive number (> 0.0000)", "Ledger Engine", "Quantum of funds moved in this transaction"),
        ("direction", "VARCHAR(6)", "Required", "None", "Enum: CREDIT, DEBIT", "Ledger Engine", "Double-entry sign indicator (inflow vs outflow)"),
        ("balance_before", "DECIMAL(14,4)", "Required", "None", "Non-negative decimal (>= 0.0000)", "Ledger Engine", "User balance immediately prior to posting"),
        ("balance_after", "DECIMAL(14,4)", "Required", "None", "Non-negative decimal; balance_before +/- amount", "Ledger Engine", "Reconciliation check ensuring zero balance drift"),
        ("transaction_status", "VARCHAR(20)", "Required", "SETTLED", "Enum: PENDING, SETTLED, LOCKED, REVERSED, FAILED", "Ledger Engine", "Lifecycle state of the ledger record"),
        ("source_event_id", "VARCHAR(20)", "Optional", "NULL", "Foreign Key -> feature_events.event_id", "Telemetry Pipeline", "Traces financial credit directly to triggering user event"),
        ("reference_id", "VARCHAR(36)", "Optional", "NULL", "Foreign Key to external activity or withdrawal ID", "Task / Withdrawal API", "Bi-directional linkage to external operational ID"),
        ("idempotency_key", "VARCHAR(64)", "Required", "None", "SHA-256 hash of unique business payload", "Client / Ingestion Gateway", "Strictly enforces exactly-once transaction processing"),
        ("created_at", "TIMESTAMP", "Required", "CURRENT_TIMESTAMP", "Immutable UTC creation timestamp", "Database Server", "Temporal ledger sequencing and daily closing balances"),
    ]
    for row in fields:
        ws1.append(row)
        
    # Sheet 2: Transaction Types Taxonomy
    ws2 = wb.create_sheet(title="Transaction_Types_Taxonomy")
    headers2 = [
        "Transaction_Type", "Direction", "Currency_Applicability",
        "Economic_Classification", "Description", "Triggering_Source", "Reversibility"
    ]
    ws2.append(headers2)
    types = [
        ("CREDIT_TASK_REWARD", "CREDIT", "VE, XP, GEM, TOKEN", "Faucet (Inflow)", "Reward issued for completing ad, survey, or offerwall task", "Task Completion Engine", "Reversible upon advertiser chargeback"),
        ("CREDIT_STREAK_BONUS", "CREDIT", "VE, XP, GEM, SPIN", "Faucet (Inflow)", "Bonus awarded for maintaining multi-day consecutive logins", "Streak Engine", "Non-reversible"),
        ("CREDIT_DAILY_REWARD", "CREDIT", "GEM, SPIN, XP", "Faucet (Inflow)", "Standard 24-hour reward calendar claim", "Daily Reward Engine", "Non-reversible"),
        ("CREDIT_REFERRAL_COMMISSION", "CREDIT", "TOKEN, XP", "Faucet (Inflow)", "Commission paid to referrer upon referee qualified action", "Referral Engine", "Reversible upon referee fraud detection"),
        ("DEBIT_EXCHANGE_OUT", "DEBIT", "GEM, VE", "Internal Conversion", "Debited from source balance during currency conversion", "Exchange Center", "Non-reversible (Atomic transaction)"),
        ("CREDIT_EXCHANGE_IN", "CREDIT", "TOKEN, GEM", "Internal Conversion", "Credited to target balance during currency conversion", "Exchange Center", "Non-reversible (Atomic transaction)"),
        ("DEBIT_WITHDRAWAL_HOLD", "DEBIT", "TOKEN", "Lock / Escrow", "Funds locked in escrow pending payout review", "Withdrawal Pipeline", "Refundable if withdrawal rejected"),
        ("DEBIT_WITHDRAWAL_SETTLED", "DEBIT", "TOKEN", "Sink (Outflow)", "Permanent debit following successful gateway payout", "Payment Gateway Webhook", "Irreversible post-gateway settlement"),
        ("CREDIT_WITHDRAWAL_REFUND", "CREDIT", "TOKEN", "Internal Refund", "Restores locked funds to user upon payout rejection", "Risk / Gateway Callback", "Non-reversible"),
        ("DEBIT_REVERSAL_CHARGEBACK", "DEBIT", "VE, TOKEN", "Penalty / Recovery", "Clawback debited from balance due to verified partner fraud", "Risk Review Engine", "Administrative only"),
        ("CREDIT_ADMIN_ADJUSTMENT", "CREDIT", "ALL", "Adjustment", "Manual compensation credited by customer support", "Support Dashboard", "Administrative only"),
    ]
    for row in types:
        ws2.append(row)
        
    # Sheet 3: Multi-Currency Registry
    ws3 = wb.create_sheet(title="Multi_Currency_Registry")
    headers3 = [
        "Currency_Code", "Currency_Name", "Decimals", "Redeemable_for_Cash",
        "Primary_Faucet", "Primary_Sink", "Exchange_Rules", "Inflation_Risk"
    ]
    ws3.append(headers3)
    currencies = [
        ("VE", "Virtual Earnings", 2, "Yes (Via Exchange to Token)", "Watch Ads, Tap & Earn, CAPTCHA", "Exchange Center to Tokens", "Convertible to Tokens at fixed dynamic exchange rate", "High (High velocity micro-earnings)"),
        ("XP", "Experience Points", 0, "No (Status Only)", "All platform completed actions", "Non-consumable progression", "Non-convertible; strictly determines Level & Perks", "Zero (Closed status system)"),
        ("GEM", "Gems", 0, "No (Utility Currency)", "Daily Rewards, Streak Milestones", "Spin the Wheel, VIP Missions", "Convertible to Spins or Entry Tickets", "Medium (Controlled issuance)"),
        ("TOKEN", "VELOOP Tokens", 4, "Yes (Direct Cashout)", "Exchange Center, High-tier Tasks", "Withdrawal Pipeline (Fiat/Crypto)", "Directly pegged to withdrawal payout options ($/INR)", "Critical (Direct platform cash liability)"),
        ("SPIN", "Wheel Spin Credits", 0, "No (Chance Tickets)", "Level-ups, Daily Claims", "Spin the Wheel RNG Mechanic", "Burned immediately upon spin execution", "Low (Pure game loop sink)"),
    ]
    for row in currencies:
        ws3.append(row)
        
    # Sheet 4: Balance Reconciliation Rules
    ws4 = wb.create_sheet(title="Balance_Reconciliation_Rules")
    headers4 = [
        "Rule_ID", "Rule_Name", "Mathematical_Invariant",
        "Enforcement_Mechanism", "Severity", "Failure_Action"
    ]
    ws4.append(headers4)
    rules = [
        ("RULE-BAL-01", "Non-Negative Balance Constraint", "balance_after >= 0.0000 across all currencies", "Database CHECK constraint & API pre-flight check", "CRITICAL", "Transaction rejected with HTTP 422 OverdraftBlocked"),
        ("RULE-BAL-02", "Delta Accuracy Invariant", "balance_after == balance_before + (direction=='CREDIT' ? amount : -amount)", "Database Trigger & Ledger Ingestion Assertion", "CRITICAL", "Database rollback and alert flagged to On-Call Data Eng"),
        ("RULE-BAL-03", "Sum of Ledger Matches Wallet", "wallet.current_balance == SUM(Credits) - SUM(Debits)", "Daily automated reconciliation cron job (02:00 UTC)", "CRITICAL", "Discrepancy quarantined in ledger_discrepancies table"),
        ("RULE-BAL-04", "Idempotent Transaction Dedup", "COUNT(transactions WHERE idempotency_key = key) == 1", "Unique Index on idempotency_key in database", "HIGH", "Second attempt returns existing transaction record (HTTP 200)"),
        ("RULE-BAL-05", "Atomic Exchange Double-Entry", "SUM(Debit_Exchange_Out.usd_value) == SUM(Credit_Exchange_In.usd_value) + Fee", "Single DB Transaction with SERIALIZABLE isolation", "CRITICAL", "Both legs rolled back if either side fails"),
    ]
    for row in rules:
        ws4.append(row)
        
    file_path = base_dir / "documentation" / "Wallet_Analytics_Specification.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "Wallet_Analytics_Specification.xlsx")

# ==============================================================================
# 2. Withdrawal_Analytics_Specification.xlsx
# ==============================================================================
def create_withdrawal_specification():
    wb = openpyxl.Workbook()
    
    # Sheet 1: Withdrawal Lifecycle Model
    ws1 = wb.active
    ws1.title = "Withdrawal_Lifecycle_Model"
    headers1 = [
        "Stage_Index", "Lifecycle_Stage", "Triggering_Actor",
        "System_Action", "Prerequisites", "Next_Allowed_Stages", "Telemetry_Event"
    ]
    ws1.append(headers1)
    stages = [
        (1, "Withdrawal Requested", "User", "Validates balance, freezes requested tokens, writes pending row", "User Active; Balance >= Min Threshold; 0 active freezes", "Under Review, Auto-Approved", "withdrawal_requested"),
        (2, "Risk & KYC Processing", "Risk Engine", "Executes automated velocity check, proxy scan, and KYC tier validation", "Pending request in queue", "Approved for Gateway, Rejected_Fraud, Rejected_KYC", "withdrawal_processing"),
        (3, "Gateway Transmitted", "Payment Dispatcher", "Dispatches batch API call to PayPal, Cashfree (UPI), or Crypto Rail", "Approved risk score; gateway available", "Gateway_Success, Gateway_Failure, Gateway_Timeout", "withdrawal_transmitted"),
        (4, "Withdrawal Completed", "Payment Gateway", "Webhook receives confirmation of successful settlement; settles fee", "Gateway confirmation callback", "None (Final Settled State)", "withdrawal_completed"),
        (5, "Withdrawal Rejected", "Risk / Gateway", "Rejects payout; unlocks escrow tokens back to user wallet", "Risk rule trip or bad banking VPA/email", "None (Final Rejected State)", "withdrawal_rejected"),
        (6, "Withdrawal Reversed", "Payment Gateway", "Settlement reverses post-payout due to bank bounce or chargeback", "Post-completion bank dispute callback", "None (Final Reversed State)", "withdrawal_reversed"),
    ]
    for row in stages:
        ws1.append(row)
        
    # Sheet 2: Withdrawal Schema Specification
    ws2 = wb.create_sheet(title="Withdrawal_Schema_Spec")
    headers2 = [
        "Field_Name", "Data_Type", "Requirement", "Default_Value",
        "Validation_Rule", "Source_Component", "Analytical_Use_Case"
    ]
    ws2.append(headers2)
    w_fields = [
        ("withdrawal_id", "VARCHAR(24)", "Required", "None", "Primary Key; Regex ^WDR\d{12}$", "Withdrawal Service", "Unique business key for all payout operations"),
        ("user_id", "VARCHAR(11)", "Required", "None", "Foreign Key -> users.user_id", "User Service", "User demographic & tenure join key"),
        ("amount_tokens", "DECIMAL(12,4)", "Required", "None", ">= min_withdrawal_tokens; <= max_daily_tokens", "Withdrawal Service", "Token balance burned in exchange for cashout"),
        ("amount_fiat", "DECIMAL(10,2)", "Required", "None", "Calculated based on active token-fiat peg", "Withdrawal Service", "Real-world cash disbursement amount"),
        ("currency_code", "VARCHAR(3)", "Required", "INR", "Enum: INR, USD, EUR, USDT", "Withdrawal Service", "Disbursement currency classification"),
        ("payout_method", "VARCHAR(20)", "Required", "None", "Enum: UPI, PAYPAL, BANK_TRANSFER, CRYPTO_USDT", "Withdrawal Service", "Payment channel share and channel preference analysis"),
        ("payout_destination_masked", "VARCHAR(100)", "Required", "None", "Masked identifier (e.g. ***42@okhdfcbank)", "Client Input", "Audit identification while preserving PII privacy"),
        ("withdrawal_status", "VARCHAR(20)", "Required", "REQUESTED", "Enum: REQUESTED, PROCESSING, COMPLETED, REJECTED, REVERSED", "Withdrawal Service", "Fulfillment funnel status tracking"),
        ("gateway_provider", "VARCHAR(30)", "Optional", "NULL", "Enum: Cashfree, Razorpay, PayPal_Payouts, Binance_Pay", "Dispatcher", "Payment partner SLA and fee comparison"),
        ("gateway_transaction_ref", "VARCHAR(100)", "Optional", "NULL", "Unique string returned by partner gateway", "Gateway Callback", "Bank settlement reconciliation and tracing"),
        ("gateway_fee_amount", "DECIMAL(8,2)", "Required", "0.00", ">= 0.00; fee charged by payment rail", "Gateway Callback", "Cost-of-goods-sold (COGS) drag analysis"),
        ("rejection_code", "VARCHAR(50)", "Optional", "NULL", "Non-null if status in ('REJECTED', 'REVERSED')", "Risk / Gateway", "Categorizes cashout friction and failure points"),
        ("requested_at", "TIMESTAMP", "Required", "CURRENT_TIMESTAMP", "Valid past/current timestamp", "Database Server", "Queue entry timestamp for SLA measurement"),
        ("completed_at", "TIMESTAMP", "Optional", "NULL", ">= requested_at; non-null if COMPLETED", "Database Server", "Measures end-to-end turnaround latency"),
    ]
    for row in w_fields:
        ws2.append(row)
        
    # Sheet 3: Payout Rails Specification
    ws3 = wb.create_sheet(title="Payout_Rails_Spec")
    headers3 = [
        "Payout_Rail", "Target_Geography", "Settlement_Type", "Min_Threshold",
        "Max_Daily_Limit", "Estimated_SLA", "Gateway_Fee_Structure", "Fraud_Risk_Profile"
    ]
    ws3.append(headers3)
    rails = [
        ("UPI (Unified Payments Interface)", "India (Domestic)", "Instant (IMPS Rail)", "₹50 ($0.60)", "₹5,000 ($60.00)", "< 5 Minutes", "₹2.50 flat per transfer", "Medium (VPA typos, stolen accounts)"),
        ("PayPal Payouts", "Global (180+ countries)", "Batch API (1-2 Hours)", "$5.00", "$100.00", "1 - 24 Hours", "2.0% + $0.25 per transaction", "High (Unverified PayPal emails, chargebacks)"),
        ("Direct Bank Wire (NEFT/IMPS)", "India / Regional", "Batch Transfer", "₹500 ($6.00)", "₹25,000 ($300.00)", "12 - 48 Hours", "₹5.00 flat per transfer", "Low (Bank account names cross-checked with KYC)"),
        ("Crypto (USDT - Polygon/TRON)", "International / Web3", "Blockchain Transfer", "$10.00", "$500.00", "< 15 Minutes", "$1.00 flat network gas fee", "Critical (Irreversible blockchain transactions)"),
    ]
    for row in rails:
        ws3.append(row)
        
    # Sheet 4: Rejection & Failure Codes
    ws4 = wb.create_sheet(title="Rejection_Failure_Codes")
    headers4 = [
        "Rejection_Code", "Failure_Category", "Trigger_Origin",
        "Root_Cause_Description", "User_Facing_Message", "Recovery_Action"
    ]
    ws4.append(headers4)
    codes = [
        ("REJ_INVALID_DESTINATION", "User Input", "Gateway Validation", "UPI VPA does not exist or PayPal account email invalid", "Invalid payment destination address. Please verify details.", "User edits payment address and resubmits"),
        ("REJ_KYC_UNVERIFIED", "Compliance", "Internal Policy", "User attempting cashout exceeding Tier-0 threshold without ID verification", "Identity verification required to withdraw this amount.", "User routes to KYC upload flow"),
        ("REJ_SUSPECTED_PROXY_BOT", "Fraud Risk", "Security Engine", "Request originated from known datacenter IP or emulator fingerprint", "Account flagged for security review. Payout placed on hold.", "Escalates to manual fraud analyst review queue"),
        ("REJ_VELOCITY_LIMIT_EXCEEDED", "Fraud Risk", "Risk Engine", "User exceeded max allowed withdrawals per 24 hours (Limit: 2)", "Daily withdrawal limit reached. Please try again tomorrow.", "User waits for rolling 24h window reset"),
        ("REJ_TASK_CHARGEBACK_DEFICIT", "Financial", "Risk Review", "Underlying offerwall tasks disputed by advertiser post-request", "Payout cancelled due to invalid task verification.", "Tokens forfeited; deficit ledger entry posted"),
        ("FAIL_GATEWAY_INSUFFICIENT_FUNDS", "Operational", "Payment Partner", "VELOOP corporate disbursement treasury wallet depleted", "Payout experiencing processing delays. Retry in progress.", "Automated Treasury alert; rebalances disbursement wallet"),
    ]
    for row in codes:
        ws4.append(row)
        
    # Sheet 5: Withdrawal KPI Catalogue
    ws5 = wb.create_sheet(title="Withdrawal_KPI_Catalogue")
    headers5 = [
        "KPI_ID", "Metric_Name", "Formula / Calculation",
        "Target_Benchmark", "Data_Source_Tables", "Business_Significance"
    ]
    ws5.append(headers5)
    w_kpis = [
        ("KPI-WDR-01", "Withdrawal Fulfillment Rate", "COUNT(Completed Withdrawals) / COUNT(Total Requested)", ">= 92.0%", "withdrawal_requests", "Core operational success metric for user value delivery"),
        ("KPI-WDR-02", "End-to-End Processing Latency", "AVG(completed_at - requested_at)", "< 2 Hours (Instant for UPI)", "withdrawal_requests", "Primary driver of user trust and retention post-cashout"),
        ("KPI-WDR-03", "Withdrawal Rejection Rate", "COUNT(Rejected Withdrawals) / COUNT(Total Requested)", "< 6.0%", "withdrawal_requests", "Measures payment friction, invalid destination errors, and bot blocks"),
        ("KPI-WDR-04", "Gateway Fee Drag %", "SUM(gateway_fee_amount) / SUM(amount_fiat)", "< 2.5%", "withdrawal_requests", "Disbursement transaction cost impacting net corporate margins"),
        ("KPI-WDR-05", "Post-Cashout 30D Retention", "COUNT(Active users 30d post-cashout) / COUNT(Cashout users)", ">= 65.0%", "withdrawal_requests, daily_activity", "Measures whether cashing out creates a repeat earner or platform exit"),
        ("KPI-WDR-06", "Fraud Hold Rate", "COUNT(Withdrawals flagged by Risk) / COUNT(Total Requested)", "3.0% - 5.0%", "withdrawal_requests", "Ensures anti-fraud screening catches bad actors without choking queue"),
    ]
    for row in w_kpis:
        ws5.append(row)
        
    file_path = base_dir / "documentation" / "Withdrawal_Analytics_Specification.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "Withdrawal_Analytics_Specification.xlsx")

if __name__ == "__main__":
    print("Generating Step 6 Excel Workbooks...")
    create_wallet_specification()
    create_withdrawal_specification()
    print("Step 6 Excel Workbooks generated successfully!")

