"""
Script to generate Phase 3 Deliverables:
1. Data_Dictionary.xlsx (85+ fields across 11 entities)
2. Entity_Relationship_Diagram.mmd & Entity_Relationship_Diagram.png
3. Data_Model_Documentation.md
4. Proposed_Database_Schema.sql
"""

import sys
from pathlib import Path
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.patches as patches

base_dir = Path(r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics")
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from report_utils import ReportUtils

def save_styled_workbook(wb: openpyxl.Workbook, file_path: Path):
    for sheet_name in wb.sheetnames:
        ReportUtils.apply_excel_styling(wb, sheet_name)
    wb.save(file_path)
    print(f"Saved: {file_path}")

# ==============================================================================
# 1. Data_Dictionary.xlsx
# ==============================================================================
def create_data_dictionary():
    wb = openpyxl.Workbook()
    
    # Sheet 1: Master_Data_Dictionary
    ws1 = wb.active
    ws1.title = "Master_Data_Dictionary"
    
    headers1 = [
        "Entity", "Field_Name", "Data_Type", "Definition", "Example_Value",
        "Requirement", "Allowed_Values", "Validation_Rule", "Source_Component",
        "Sensitivity_Classification", "Analytical_Use", "Implementation_Status"
    ]
    ws1.append(headers1)
    
    fields = [
        # Entity 1: Users (15 fields)
        ("Users", "user_id", "VARCHAR(11)", "Unique stable user account identifier", "VLUSR000001", "Required", "Format ^VLUSR\\d{6}$", "Non-null, unique primary key", "Backend User Service", "Internal Identifier", "Primary dimensional join key across all marts", "Verified (Users_1000_Clean)"),
        ("Users", "full_name", "VARCHAR(100)", "Legal or display name of the user", "Sanjay Singh", "Required", "Text string 2-100 chars", "Trim whitespace; non-empty", "User Signup Input", "Confidential PII", "Personalization and KYC banking match", "Verified (Users_1000_Clean)"),
        ("Users", "email", "VARCHAR(150)", "Primary contact email address", "sanjay.singh1@gmail.com", "Required", "Valid email regex", "RFC 5322 regex; unique constraint", "User Signup Input", "Confidential PII", "Identity authentication and re-engagement", "Verified (Users_1000_Clean)"),
        ("Users", "age", "INTEGER", "Chronological age of the user in years", "35", "Required", "13 to 100", "Must be integer between 13 and 100", "User Signup Input", "Internal Demographic", "Demographic segmentation & legal compliance", "Verified (Users_1000_Clean)"),
        ("Users", "gender", "VARCHAR(20)", "Self-identified gender of the user", "Male", "Required", "Enum: Male, Female, Other, Prefer not to say", "Restricted to allowed enum set", "User Signup Input", "Internal Demographic", "Ad targeting and demographic cohort analysis", "Verified (Users_1000_Clean)"),
        ("Users", "state", "VARCHAR(50)", "Geographic state or territory of residence", "Odisha", "Required", "Standardized Indian States / Regions", "Valid state dictionary match", "User Signup / IP Geo", "Internal Geographic", "Regional task allocation and localized eCPMs", "Verified (Users_1000_Clean)"),
        ("Users", "city", "VARCHAR(50)", "City of residence", "Bhubaneswar", "Optional", "Standard city names", "Trim whitespace; null allowed", "User Signup / IP Geo", "Internal Geographic", "Urban vs rural earning index analysis", "Verified (Users_1000_Clean)"),
        ("Users", "registration_datetime", "TIMESTAMP", "Exact timestamp when user committed registration", "2026-06-10 07:14:00", "Required", "Valid past/current UTC timestamp", "Must be <= last_login_datetime", "Database Server", "Operational Metadata", "Cohort grouping (acquisition date), tenure", "Verified (Users_1000_Clean)"),
        ("Users", "acquisition_source", "VARCHAR(50)", "Marketing channel attributed to the user signup", "Facebook Ads", "Required", "Organic, Facebook Ads, Google Ads, Referral, Influencer", "Restricted to allowed acquisition channels", "Attribution Engine", "Internal Marketing", "CAC calculation and channel quality ranking", "Verified (Users_1000_Clean)"),
        ("Users", "referral_source_detail", "VARCHAR(50)", "Referral code used during registration", "REF12345", "Optional", "Alphanumeric code or NULL", "Null for organic; matches referral_code", "Referral Service", "Internal Marketing", "Viral loop attribution and referee tracking", "Verified (Users_1000_Clean)"),
        ("Users", "primary_device", "VARCHAR(50)", "Primary hardware form factor used", "Mobile", "Required", "Mobile, Desktop, Tablet", "Restricted to allowed devices", "Client User-Agent", "Technical Metadata", "Device optimization and screen layout tuning", "Verified (Users_1000_Clean)"),
        ("Users", "platform", "VARCHAR(20)", "Primary operating system platform", "Android", "Required", "Android, iOS, Web", "Restricted to allowed OS platforms", "Client App SDK", "Technical Metadata", "Cross-platform performance and feature parity", "Verified (Users_1000_Clean)"),
        ("Users", "xp_balance", "INTEGER", "Current accumulated Experience Points balance", "1250", "Required", "Non-negative integer >= 0", "CHECK (xp_balance >= 0)", "Gamification Service", "Internal Economic", "Determines user level and perk unlocking", "Verified (Users_1000_Clean)"),
        ("Users", "referral_code", "VARCHAR(20)", "Unique referral code assigned to user to invite peers", "VLREF000001", "Required", "Unique alphanumeric string", "Unique constraint across all users", "Referral Service", "Public Identifier", "Viral sharing and invite tracking", "Verified (Users_1000_Clean)"),
        ("Users", "days_since_registration", "INTEGER", "Number of days elapsed since user registration date", "45", "Required", "Integer >= 0", "Computed: CURRENT_DATE - registration_date", "Data Warehouse Mart", "Derived Metric", "Tenure bracket classification (D0, D1-7, D8-30)", "Verified (Users_1000_Clean)"),

        # Entity 2: Accounts & Security (8 fields)
        ("Accounts", "account_status", "VARCHAR(20)", "Operational state of the user account", "Active", "Required", "Active, Suspended, Pending, Deactivated", "Restricted to allowed lifecycle states", "User Auth Service", "Security Critical", "Active user filtering and churn analysis", "Verified (Users_1000_Clean)"),
        ("Accounts", "email_verification_status", "VARCHAR(20)", "Verification state of the user email address", "Verified", "Required", "Verified, Unverified", "Restricted to allowed verification enums", "Auth Service", "Security Critical", "Security readiness and bot farm risk filtering", "Verified (Users_1000_Clean)"),
        ("Accounts", "onboarding_status", "VARCHAR(20)", "Completion state of the introductory tutorial", "Completed", "Required", "Completed, Incomplete", "Restricted to allowed onboarding enums", "Client App SDK", "Product Engagement", "D0 activation funnel conversion rate", "Verified (Users_1000_Clean)"),
        ("Accounts", "last_login_datetime", "TIMESTAMP", "Timestamp of most recent authenticated app session", "2026-09-17 10:08:00", "Optional", "Valid UTC timestamp or NULL", "Must be >= registration_datetime", "Auth Gateway", "Operational Metadata", "Recency calculation and dormancy classification", "Verified (Users_1000_Clean)"),
        ("Accounts", "consent_status", "VARCHAR(20)", "Data processing consent status under privacy law", "Granted", "Required", "Granted, Denied, Pending", "Restricted to consent enums", "Consent Management", "Legal / Compliance", "Regulatory compliance (DPDP Act / GDPR)", "Verified (Users_1000_Clean)"),
        ("Accounts", "marketing_opt_in", "BOOLEAN", "Consent flag for marketing push and email notifications", "TRUE", "Required", "Boolean True/False", "Default FALSE", "User Profile Settings", "Internal Marketing", "Addressable audience sizing for push campaigns", "Verified (Users_1000_Clean)"),
        ("Accounts", "account_created_via", "VARCHAR(30)", "Registration authentication mechanism", "Direct", "Required", "Direct, Google_OAuth, Apple_ID", "Restricted to auth mechanisms", "Auth Gateway", "Technical Metadata", "Social auth adoption and signup friction analysis", "Verified (Users_1000_Clean)"),
        ("Accounts", "country", "VARCHAR(10)", "ISO 3166-1 alpha-2 country code of residency", "IN", "Required", "Standard ISO Alpha-2 (IN, US, etc.)", "Two-character uppercase string", "User Profile / GeoIP", "Internal Geographic", "Geographic localization and legal terms", "Verified (Users_1000_Clean)"),

        # Entity 3: Sessions (8 fields)
        ("Sessions", "session_id", "VARCHAR(11)", "Unique identifier for an application visit session", "SESS0000001", "Required", "Format ^SESS\\d{7}$", "Unique primary key; non-null", "Client Telemetry SDK", "Internal Identifier", "Session-level analytics and visit grouping", "Verified (02_Sessions)"),
        ("Sessions", "session_start", "TIMESTAMP", "Timestamp when app session was initialized", "2026-08-11 10:30:01", "Required", "Valid UTC timestamp", "Must be <= session_end", "Client Telemetry SDK", "Operational Metadata", "Session pacing and hourly engagement curves", "Verified (02_Sessions)"),
        ("Sessions", "session_end", "TIMESTAMP", "Timestamp when app session terminated", "2026-08-11 10:30:46", "Required", "Valid UTC timestamp", "Must be >= session_start", "Client Telemetry SDK", "Operational Metadata", "Session duration calculation", "Verified (02_Sessions)"),
        ("Sessions", "session_duration_seconds", "INTEGER", "Elapsed session length in seconds", "45", "Required", "Integer >= 0 and <= 86400", "Matches session_end - session_start", "Client Telemetry SDK", "Product Engagement", "Average time spent in app per visit", "Verified (02_Sessions)"),
        ("Sessions", "entry_point", "VARCHAR(50)", "UI origin or navigation trigger initiating session", "Dashboard", "Required", "Dashboard, Push Notification, Deep Link, Direct", "Valid entry point dictionary", "Client Telemetry SDK", "Product Engagement", "Push campaign attribution and return traffic origin", "Verified (02_Sessions)"),
        ("Sessions", "exit_feature", "VARCHAR(50)", "Last feature screen viewed before session ended", "Help/Support", "Optional", "Valid feature name or NULL", "Null indicates abrupt backgrounding/crash", "Client Telemetry SDK", "Product Engagement", "Session drop-off screen analysis (5.89% nulls)", "Verified (02_Sessions)"),
        ("Sessions", "events_in_session", "INTEGER", "Count of granular telemetry events fired in session", "17", "Required", "Integer >= 0", "Non-negative integer", "Event Ingestion Engine", "Product Engagement", "Session activity depth and interaction density", "Verified (02_Sessions)"),
        ("Sessions", "features_used_count", "INTEGER", "Number of distinct features interacted with in session", "4", "Required", "Integer >= 0 and <= 15", "Non-negative integer", "Event Ingestion Engine", "Product Engagement", "Feature exploration breadth per visit", "Verified (02_Sessions)"),

        # Entity 4: Tasks (Catalog Entity) (6 fields)
        ("Tasks", "task_id", "VARCHAR(20)", "Unique identifier for a catalog offer or task template", "TASK0071", "Required", "Format ^TASK\\d{4}$", "Unique catalog primary key", "Task Management CMS", "Public Identifier", "Task performance and partner campaign grouping", "Verified (05_Task_Activity)"),
        ("Tasks", "task_category", "VARCHAR(50)", "Functional category of the earning task", "Game", "Required", "Ad, App Task, Survey, CAPTCHA, Game, Social, Promo", "Restricted to 8 valid task categories", "Task Management CMS", "Internal Product", "Category completion rate and revenue mix", "Verified (05_Task_Activity)"),
        ("Tasks", "task_title", "VARCHAR(150)", "User-facing title of the earning offer", "Reach Level 10 in Castle Quest", "Required", "Non-empty string", "Length 5-150 characters", "Task Management CMS", "Internal Product", "UI task catalog rendering and marketing copy", "Proposed Specification"),
        ("Tasks", "reward_currency_offered", "VARCHAR(10)", "Virtual currency awarded upon successful completion", "VE", "Required", "VE, XP, GEM, TOKEN, SPIN", "Restricted to 5 platform currencies", "Task Management CMS", "Internal Economic", "Currency faucet distribution modeling", "Proposed Specification"),
        ("Tasks", "reward_amount_offered", "DECIMAL(10,2)", "Base currency amount awarded upon completion", "150.00", "Required", "Decimal > 0.00", "Strictly positive number", "Task Management CMS", "Internal Economic", "Expected value per task and payout economics", "Proposed Specification"),
        ("Tasks", "advertiser_partner_name", "VARCHAR(100)", "Name of third-party network sponsoring offer", "Tapjoy", "Required", "AdMob, Unity, Tapjoy, Pollfish, Direct", "Non-empty partner string", "AdOps Management", "Partner Commercial", "Partner revenue yield and chargeback analysis", "Proposed Specification"),

        # Entity 5: Task Activity (Operational Execution) (7 fields)
        ("Task Activity", "activity_id", "VARCHAR(15)", "Unique operational identifier for a task execution attempt", "ACT0000001", "Required", "Format ^ACT\\d{7}$", "Unique primary key; non-null", "Task Execution Service", "Internal Identifier", "End-to-end task conversion tracking", "Verified (05_Task_Activity)"),
        ("Task Activity", "task_viewed_at", "TIMESTAMP", "Timestamp when task instructions were displayed", "2026-08-05 19:36:29", "Required", "Valid past/current UTC timestamp", "Must be <= task_started_at", "Task Execution Service", "Operational Metadata", "Discovery-to-start conversion velocity", "Verified (05_Task_Activity)"),
        ("Task Activity", "task_started_at", "TIMESTAMP", "Timestamp when user clicked start to initiate offer", "2026-08-05 19:38:50", "Required", "Valid UTC timestamp", "task_viewed_at <= task_started_at", "Task Execution Service", "Operational Metadata", "Denominator for task completion calculations", "Verified (05_Task_Activity)"),
        ("Task Activity", "task_completed_at", "TIMESTAMP", "Timestamp when user or partner submitted completion", "2026-08-05 19:42:15", "Optional", "Valid UTC timestamp or NULL", "Null when Failed, Abandoned, or Pending", "Task Execution Service", "Operational Metadata", "Task completion duration and latency SLA", "Verified (05_Task_Activity)"),
        ("Task Activity", "task_status", "VARCHAR(20)", "Operational status of the task execution attempt", "Completed", "Required", "Completed, Abandoned, Failed, Pending", "Restricted to 4 valid task statuses", "Task Execution Service", "Product Engagement", "Task Completion Rate (TCR) calculation", "Verified (05_Task_Activity)"),
        ("Task Activity", "failure_reason", "VARCHAR(100)", "Specific failure code explaining uncredited task", "Validation failed", "Optional", "Validation failed, Task unavailable, Timeout, etc.", "Must be non-null if status == 'Failed'", "Task Validation Service", "Quality & Stability", "Diagnosing partner SDK drops and UX friction", "Verified (05_Task_Activity)"),
        ("Task Activity", "reward_status", "VARCHAR(20)", "Reward fulfillment state recorded on task row", "Credited", "Required", "Credited, Not Credited, Pending", "Restricted to 3 valid reward statuses", "Task Execution Service", "Financial Coupling", "Operational task credit audit (GAP-003)", "Verified (05_Task_Activity)"),

        # Entity 6: Rewards (Financial Ledger) (7 fields)
        ("Rewards", "reward_transaction_id", "VARCHAR(24)", "Unique financial ledger transaction identifier for reward", "RWD202611010001", "Required", "Format ^RWD\\d{12}$", "Unique primary key; non-null", "Rewards Ledger Engine", "Financial Sensitive", "Audit trail for all platform reward distributions", "Proposed Target (GAP-003)"),
        ("Rewards", "source_feature", "VARCHAR(50)", "Originating feature rewarding the user", "Watch Ads", "Required", "Watch Ads, Missions, Streaks, Daily Reward, Tap", "Restricted to 15 platform features", "Rewards Ledger Engine", "Internal Economic", "Cost attribution and feature profitability", "Proposed Target (GAP-003)"),
        ("Rewards", "currency_type", "VARCHAR(10)", "Virtual currency credited in this transaction", "VE", "Required", "VE, XP, GEM, TOKEN, SPIN", "Restricted to 5 platform currencies", "Rewards Ledger Engine", "Internal Economic", "Multi-currency balance reconciliation", "Proposed Target (GAP-003)"),
        ("Rewards", "reward_amount", "DECIMAL(14,4)", "Quantum of currency awarded", "150.0000", "Required", "Strictly positive number > 0.0000", "CHECK (reward_amount > 0)", "Rewards Ledger Engine", "Financial Sensitive", "Gross currency issuance volume ($)", "Proposed Target (GAP-003)"),
        ("Rewards", "reward_lifecycle_status", "VARCHAR(20)", "Escrow and fulfillment state of reward", "CREDITED", "Required", "PENDING, CREDITED, REVERSED, CORRECTED", "Restricted to 4 reward states", "Rewards Ledger Engine", "Financial Sensitive", "Escrow tracking and chargeback reversal audit", "Proposed Target (GAP-003)"),
        ("Rewards", "idempotency_hash", "VARCHAR(64)", "SHA-256 cryptographic hash of transaction payload", "a1b2c3d4e5...", "Required", "64-character hexadecimal hash", "Unique constraint across all rewards", "Ingestion Gateway", "Security Critical", "Prevents duplicate reward credits on network retries", "Proposed Target (GAP-003)"),
        ("Rewards", "credited_at", "TIMESTAMP", "Timestamp when funds cleared escrow into spendable balance", "2026-11-01 14:32:00", "Optional", "Valid UTC timestamp or NULL", "Populated when status == 'CREDITED'", "Rewards Ledger Engine", "Operational Metadata", "Reward delivery latency measurement", "Proposed Target (GAP-003)"),

        # Entity 7: Wallet Transactions (8 fields)
        ("Wallet Transactions", "wallet_transaction_id", "VARCHAR(24)", "Unique double-entry balance mutation identifier", "WLT202611010001", "Required", "Format ^WLT\\d{12}$", "Unique primary key; non-null", "Wallet Ledger Service", "Financial Sensitive", "Immutable financial ledger record", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "transaction_type", "VARCHAR(30)", "Economic classification of the balance movement", "CREDIT_TASK_REWARD", "Required", "11 defined transaction types", "Restricted to transaction taxonomy", "Wallet Ledger Service", "Financial Sensitive", "Classifies faucet vs sink vs conversion", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "direction", "VARCHAR(6)", "Accounting direction of entry", "CREDIT", "Required", "CREDIT, DEBIT", "Restricted to CREDIT or DEBIT", "Wallet Ledger Service", "Financial Sensitive", "Double-entry accounting balance delta", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "amount", "DECIMAL(14,4)", "Currency amount debited or credited", "200.0000", "Required", "Decimal > 0.0000", "CHECK (amount > 0)", "Wallet Ledger Service", "Financial Sensitive", "Monetary quantum moved in transaction", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "balance_before", "DECIMAL(14,4)", "Account balance immediately prior to posting", "500.0000", "Required", "Decimal >= 0.0000", "Non-negative balance", "Wallet Ledger Service", "Financial Sensitive", "Audit trail baseline for delta check", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "balance_after", "DECIMAL(14,4)", "Account balance immediately following posting", "700.0000", "Required", "Decimal >= 0.0000", "balance_before +/- amount == balance_after", "Wallet Ledger Service", "Financial Sensitive", "Instantaneous balance integrity assertion", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "reference_id", "VARCHAR(36)", "External operational identifier linking the entry", "ACT0000001", "Optional", "Foreign key to task or withdrawal", "Valid foreign ID string or NULL", "Wallet Ledger Service", "Operational Metadata", "Bi-directional linkage to operational source", "Proposed Target (GAP-001)"),
        ("Wallet Transactions", "idempotency_key", "VARCHAR(64)", "Unique transaction deduplication hash", "e7f8a9...", "Required", "Unique 64-char string", "Unique constraint in database", "Wallet Ingestion Gateway", "Security Critical", "Prevents double-spend and double-credit bugs", "Proposed Target (GAP-001)"),

        # Entity 8: Withdrawals (Cashout Pipeline) (8 fields)
        ("Withdrawals", "withdrawal_id", "VARCHAR(24)", "Unique identifier for a cashout payout operation", "WDR202611010001", "Required", "Format ^WDR\\d{12}$", "Unique primary key; non-null", "Withdrawal Microservice", "Financial Sensitive", "Tracks cashout request through gateway", "Proposed Target (GAP-002)"),
        ("Withdrawals", "amount_tokens", "DECIMAL(12,4)", "Tokens debited from user wallet for cashout", "1000.0000", "Required", "Decimal >= min_tokens_threshold", "CHECK (amount_tokens > 0)", "Withdrawal Microservice", "Financial Sensitive", "Token burn volume in cashout operations", "Proposed Target (GAP-002)"),
        ("Withdrawals", "amount_fiat", "DECIMAL(10,2)", "Disbursed fiat currency equivalent", "500.00", "Required", "Decimal > 0.00", "Calculated based on active peg", "Withdrawal Microservice", "Financial Sensitive", "Real-world cash disbursement amount", "Proposed Target (GAP-002)"),
        ("Withdrawals", "currency_code", "VARCHAR(3)", "ISO 4217 fiat currency code", "INR", "Required", "INR, USD, EUR, USDT", "Standard currency code", "Withdrawal Microservice", "Financial Sensitive", "Treasury currency exposure and bank rails", "Proposed Target (GAP-002)"),
        ("Withdrawals", "payout_method", "VARCHAR(20)", "Payment rail selected for fund disbursement", "UPI", "Required", "UPI, PAYPAL, BANK_TRANSFER, CRYPTO_USDT", "Restricted to 4 supported rails", "Withdrawal Microservice", "Financial Sensitive", "Disbursement rail volume and fee share", "Proposed Target (GAP-002)"),
        ("Withdrawals", "payout_destination_masked", "VARCHAR(100)", "Masked account identifier for privacy preservation", "***42@okhdfcbank", "Required", "Masked VPA, email, or bank number", "PII sanitized string", "Client Payout Form", "Confidential PII", "Operational auditing without exposing full PII", "Proposed Target (GAP-002)"),
        ("Withdrawals", "withdrawal_status", "VARCHAR(20)", "Current state in the 5-stage payout pipeline", "COMPLETED", "Required", "REQUESTED, PROCESSING, COMPLETED, REJECTED, REVERSED", "Restricted to 5 lifecycle states", "Withdrawal Microservice", "Financial Sensitive", "Fulfillment funnel and SLA latency monitoring", "Proposed Target (GAP-002)"),
        ("Withdrawals", "gateway_fee_amount", "DECIMAL(8,2)", "Transaction fee charged by payment gateway partner", "2.50", "Required", "Decimal >= 0.00", "Non-negative fee amount", "Gateway Webhook Callback", "Commercial Financial", "Gateway fee drag on net corporate margins", "Proposed Target (GAP-002)"),

        # Entity 9: Referrals (Virality & Relationships) (7 fields)
        ("Referrals", "referral_id", "BIGINT", "Unique auto-incrementing referral connection identifier", "1001", "Required", "Integer > 0", "Unique primary key; non-null", "Referral Engine", "Internal Identifier", "Referral tree modeling and viral loops", "Proposed Target (GAP-004)"),
        ("Referrals", "referrer_user_id", "VARCHAR(11)", "User ID of the inviter generating the referral", "VLUSR000001", "Required", "Format ^VLUSR\\d{6}$", "Foreign key -> users.user_id", "Referral Engine", "Internal Identifier", "Referrer commission attribution", "Proposed Target (GAP-004)"),
        ("Referrals", "referee_user_id", "VARCHAR(11)", "User ID of the invited new user", "VLUSR000105", "Required", "Format ^VLUSR\\d{6}$", "Foreign key UNIQUE -> users.user_id", "Referral Engine", "Internal Identifier", "Ensures referee can only be referred once", "Proposed Target (GAP-004)"),
        ("Referrals", "referral_code_used", "VARCHAR(20)", "Referral code inputted during referee signup", "VLREF000001", "Required", "Alphanumeric code", "Matches referrer referral_code", "Signup Attribution", "Internal Marketing", "Code-level campaign tracking and attribution", "Proposed Target (GAP-004)"),
        ("Referrals", "conversion_status", "VARCHAR(20)", "Current stage of referee conversion progression", "QUALIFIED", "Required", "REGISTERED, ONBOARDED, ACTIVATED, QUALIFIED, REJECTED", "Restricted to 5 conversion states", "Referral Engine", "Growth & Virality", "Referral conversion funnel analysis", "Proposed Target (GAP-004)"),
        ("Referrals", "is_qualified", "BOOLEAN", "Indicates referee has achieved earning threshold", "TRUE", "Required", "Boolean True/False", "Default FALSE; set upon task completion", "Referral Rules Engine", "Growth & Virality", "Determines referral reward payout eligibility", "Proposed Target (GAP-004)"),
        ("Referrals", "referrer_reward_credited", "BOOLEAN", "Indicates bonus tokens have cleared to referrer", "TRUE", "Required", "Boolean True/False", "Set TRUE upon reward_credited event", "Ledger Engine", "Financial Sensitive", "Ensures bonus is awarded exactly once", "Proposed Target (GAP-004)"),

        # Entity 10: Feature Events (Telemetry) (7 fields)
        ("Feature Events", "event_id", "VARCHAR(11)", "Unique telemetry event identifier", "EVT00000001", "Required", "Format ^EVT\\d{8}$", "Unique primary key; non-null", "Client Telemetry SDK", "Internal Identifier", "Atomic event join key across clickstream", "Verified (03_Feature_Events)"),
        ("Feature Events", "event_datetime", "TIMESTAMP", "Exact timestamp when user interaction occurred", "2026-08-11 10:30:03", "Required", "Valid UTC timestamp", "Must fall within session_start and session_end", "Client Telemetry SDK", "Operational Metadata", "Event sequencing and engagement frequency", "Verified (03_Feature_Events)"),
        ("Feature Events", "feature_name", "VARCHAR(50)", "Functional feature domain where interaction happened", "Watch Ads", "Required", "15 distinct feature names", "Restricted to 15 supported features", "Client Telemetry SDK", "Product Engagement", "Feature adoption and engagement distribution", "Verified (03_Feature_Events)"),
        ("Feature Events", "event_name", "VARCHAR(50)", "Specific action or transition emitted", "ad_completed", "Required", "Standardized lower_snake_case string", "Valid event taxonomy name", "Client Telemetry SDK", "Product Engagement", "Granular user action conversion funnels", "Verified (03_Feature_Events)"),
        ("Feature Events", "event_status", "VARCHAR(20)", "Outcome state of the atomic interaction", "Success", "Required", "Started, Success, Abandoned, Failed", "Restricted to 4 event statuses", "Client Telemetry SDK", "Product Engagement", "Feature success and failure rate benchmarking", "Verified (03_Feature_Events)"),
        ("Feature Events", "sequence_number", "INTEGER", "Sequential event index within the session", "1", "Required", "Integer >= 1", "Monotonically increasing per session", "Client Telemetry SDK", "Technical Metadata", "Path analysis and user journey reconstruction", "Verified (03_Feature_Events)"),
        ("Feature Events", "reward_related_flag", "BOOLEAN", "Flag indicating event directly impacts currency balance", "TRUE", "Required", "Boolean True/False", "Boolean constraint", "Client Telemetry SDK", "Financial Oversight", "Filters monetization events from navigational pings", "Verified (03_Feature_Events)"),

        # Entity 11: Daily Engagement (Rollup Mart) (7 fields)
        ("Daily Engagement", "activity_date", "DATE", "Calendar date of engagement (UTC)", "2026-08-11", "Required", "Valid ISO 8601 Date YYYY-MM-DD", "Composite primary key with user_id", "Rollup ETL Pipeline", "Operational Metadata", "Temporal aggregation grain for daily reporting", "Verified (04_Daily_Activity)"),
        ("Daily Engagement", "session_count", "INTEGER", "Total distinct sessions initiated by user on date", "2", "Required", "Integer >= 0", "Non-negative integer", "Rollup ETL Pipeline", "Product Engagement", "Visits per DAU stickiness metric", "Verified (04_Daily_Activity)"),
        ("Daily Engagement", "session_duration_minutes", "DECIMAL(8,2)", "Total cumulative minutes spent in app on date", "18.20", "Required", "Decimal >= 0.00", "Non-negative decimal", "Rollup ETL Pipeline", "Product Engagement", "Time-in-app engagement intensity", "Verified (04_Daily_Activity)"),
        ("Daily Engagement", "event_count", "INTEGER", "Total granular telemetry events fired on date", "17", "Required", "Integer >= 0", "Non-negative integer", "Rollup ETL Pipeline", "Product Engagement", "Daily interaction density per active user", "Verified (04_Daily_Activity)"),
        ("Daily Engagement", "completed_task_count", "INTEGER", "Total monetizable tasks successfully finished on date", "2", "Required", "Integer >= 0", "Non-negative integer", "Rollup ETL Pipeline", "Monetization Yield", "Daily task completion power per earner", "Verified (04_Daily_Activity)"),
        ("Daily Engagement", "daily_reward_claimed", "BOOLEAN", "Indicates calendar reward claimed on date", "TRUE", "Required", "Boolean True/False", "Boolean constraint", "Rollup ETL Pipeline", "Gamification Retention", "Daily habit reinforcement indicator", "Verified (04_Daily_Activity)"),
        ("Daily Engagement", "active_flag", "BOOLEAN", "Classifies user as an active DAU for the calendar day", "TRUE", "Required", "Boolean True/False", "Boolean constraint", "Rollup ETL Pipeline", "Core Active Metric", "Primary filter for DAU calculations", "Verified (04_Daily_Activity)"),
    ]
    
    for row in fields:
        ws1.append(row)
        
    doc_path = base_dir / "documentation" / "Data_Dictionary.xlsx"
    rep_path = base_dir / "reports" / "Data_Dictionary.xlsx"
    root_path = base_dir / "Data_Dictionary.xlsx"
    save_styled_workbook(wb, doc_path)
    wb.save(rep_path)
    wb.save(root_path)
    print(f"Saved: {root_path} (Total fields: {len(fields)})")

# ==============================================================================
# 2. Entity_Relationship_Diagram.mmd
# ==============================================================================
def create_er_diagram_mmd():
    mmd_content = """erDiagram
    USERS ||--o{ SESSIONS : "1:N (initiates)"
    USERS ||--o{ FEATURE_EVENTS : "1:N (emits)"
    USERS ||--o{ DAILY_ACTIVITY : "1:N (accumulates)"
    USERS ||--o{ TASK_ACTIVITY : "1:N (executes)"
    USERS ||--o{ MILESTONES : "1:N (unlocks)"
    USERS ||--o{ REWARDS_LEDGER : "1:N (earns)"
    USERS ||--o{ WALLET_TRANSACTIONS : "1:N (transacts)"
    USERS ||--o{ WITHDRAWAL_REQUESTS : "1:N (requests)"
    USERS ||--o{ REFERRAL_RELATIONSHIPS : "1:N (refers/referee)"

    SESSIONS ||--o{ FEATURE_EVENTS : "1:N (contains)"
    SESSIONS ||--o{ TASK_ACTIVITY : "1:N (hosts)"
    SESSIONS ||--o{ MILESTONES : "1:N (triggers)"

    TASKS ||--o{ TASK_ACTIVITY : "1:N (catalog template)"

    TASK_ACTIVITY ||--o| REWARDS_LEDGER : "1:1 (decoupled credit)"
    REWARDS_LEDGER ||--o| WALLET_TRANSACTIONS : "1:1 (posts credit)"
    WITHDRAWAL_REQUESTS ||--o{ WALLET_TRANSACTIONS : "1:N (hold/settle/refund)"

    USERS {
        VARCHAR(11) user_id PK
        VARCHAR(100) full_name
        VARCHAR(150) email
        INTEGER age
        VARCHAR(20) gender
        VARCHAR(50) state
        VARCHAR(50) city
        TIMESTAMP registration_datetime
        VARCHAR(50) acquisition_source
        VARCHAR(50) referral_source_detail
        VARCHAR(50) primary_device
        VARCHAR(20) platform
        VARCHAR(20) account_status
        VARCHAR(20) email_verification_status
        VARCHAR(20) onboarding_status
        TIMESTAMP last_login_datetime
        INTEGER xp_balance
        VARCHAR(20) referral_code
        BOOLEAN is_active_7d
        BOOLEAN is_active_30d
    }

    SESSIONS {
        VARCHAR(11) session_id PK
        VARCHAR(11) user_id FK
        TIMESTAMP session_start
        TIMESTAMP session_end
        INTEGER session_duration_seconds
        VARCHAR(50) device
        VARCHAR(20) platform
        VARCHAR(50) entry_point
        VARCHAR(50) exit_feature
        INTEGER events_in_session
        INTEGER features_used_count
    }

    FEATURE_EVENTS {
        VARCHAR(11) event_id PK
        VARCHAR(11) user_id FK
        VARCHAR(11) session_id FK
        TIMESTAMP event_datetime
        VARCHAR(50) feature_name
        VARCHAR(50) event_name
        VARCHAR(20) event_status
        VARCHAR(50) device
        VARCHAR(20) platform
        INTEGER sequence_number
        BOOLEAN reward_related_flag
    }

    TASKS {
        VARCHAR(20) task_id PK
        VARCHAR(50) task_category
        VARCHAR(150) task_title
        VARCHAR(10) reward_currency_offered
        DECIMAL reward_amount_offered
        VARCHAR(100) advertiser_partner_name
    }

    TASK_ACTIVITY {
        VARCHAR(15) activity_id PK
        VARCHAR(11) user_id FK
        VARCHAR(20) task_id FK
        VARCHAR(11) session_id FK
        VARCHAR(50) task_category
        TIMESTAMP task_viewed_at
        TIMESTAMP task_started_at
        TIMESTAMP task_completed_at
        VARCHAR(20) task_status
        VARCHAR(100) failure_reason
        VARCHAR(20) reward_status
    }

    REWARDS_LEDGER {
        VARCHAR(24) reward_transaction_id PK
        VARCHAR(15) activity_id FK
        VARCHAR(11) user_id FK
        VARCHAR(50) source_feature
        VARCHAR(10) currency_type
        DECIMAL reward_amount
        VARCHAR(20) reward_lifecycle_status
        VARCHAR(64) idempotency_hash
        DECIMAL balance_after
        TIMESTAMP created_at
        TIMESTAMP credited_at
    }

    WALLET_TRANSACTIONS {
        VARCHAR(24) wallet_transaction_id PK
        VARCHAR(11) user_id FK
        VARCHAR(10) currency
        VARCHAR(30) transaction_type
        VARCHAR(6) direction
        DECIMAL amount
        DECIMAL balance_before
        DECIMAL balance_after
        VARCHAR(36) reference_id
        VARCHAR(64) idempotency_key
        TIMESTAMP created_at
    }

    WITHDRAWAL_REQUESTS {
        VARCHAR(24) withdrawal_id PK
        VARCHAR(11) user_id FK
        DECIMAL amount_tokens
        DECIMAL amount_fiat
        VARCHAR(3) currency_code
        VARCHAR(20) payout_method
        VARCHAR(100) payout_destination_masked
        VARCHAR(20) withdrawal_status
        VARCHAR(30) gateway_provider
        VARCHAR(100) gateway_transaction_ref
        DECIMAL gateway_fee_amount
        TIMESTAMP requested_at
        TIMESTAMP completed_at
    }

    REFERRAL_RELATIONSHIPS {
        BIGINT referral_id PK
        VARCHAR(11) referrer_user_id FK
        VARCHAR(11) referee_user_id FK
        VARCHAR(20) referral_code_used
        VARCHAR(20) conversion_status
        BOOLEAN is_qualified
        BOOLEAN referrer_reward_credited
        TIMESTAMP created_at
    }

    DAILY_ACTIVITY {
        VARCHAR(11) user_id PK
        DATE activity_date PK
        INTEGER session_count
        DECIMAL session_duration_minutes
        INTEGER event_count
        INTEGER completed_task_count
        BOOLEAN daily_reward_claimed
        BOOLEAN active_flag
    }

    MILESTONES {
        BIGSERIAL milestone_id PK
        VARCHAR(11) user_id FK
        VARCHAR(11) session_id FK
        VARCHAR(50) milestone_type
        TIMESTAMP milestone_datetime
        VARCHAR(50) milestone_value
    }
"""
    output_path = base_dir / "documentation" / "Entity_Relationship_Diagram.mmd"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(mmd_content)
    print(f"Saved: {output_path}")

# ==============================================================================
# 3. Entity_Relationship_Diagram.png
# ==============================================================================
def create_er_diagram_png():
    fig, ax = plt.subplots(figsize=(16, 12), dpi=300)
    ax.set_facecolor("#0F172A")  # Deep slate dark
    fig.patch.set_facecolor("#0F172A")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Header Title
    ax.text(8, 11.4, "VELOP REWARDS — LOGICAL DATA MODEL (ER DIAGRAM)", 
            color="#FFFFFF", fontsize=18, fontweight="bold", ha="center")
    ax.text(8, 11.0, "Relational Core Architecture: Verified Source Tables vs Proposed Financial Ledgers", 
            color="#94A3B8", fontsize=11, ha="center")

    def draw_entity_box(x, y, w, h, title, fields, border_color="#38BDF8", fill_color="#1E293B"):
        # Box container
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", 
                                      linewidth=2, edgecolor=border_color, facecolor=fill_color)
        ax.add_patch(rect)
        # Header bar
        header_rect = patches.FancyBboxPatch((x, y + h - 0.5), w, 0.5, boxstyle="round,pad=0.05", 
                                             linewidth=0, facecolor=border_color)
        ax.add_patch(header_rect)
        ax.text(x + w/2, y + h - 0.28, title, color="#0F172A", fontsize=9.5, fontweight="bold", ha="center")
        
        # Fields text
        y_text = y + h - 0.8
        for f in fields:
            ax.text(x + 0.15, y_text, f, color="#E2E8F0", fontsize=7.5, family="monospace")
            y_text -= 0.32

    # Draw Core Entities
    # 1. Users (Center Hub)
    draw_entity_box(6.2, 5.2, 3.6, 4.4, "USERS (Core Dimension)", [
        "PK user_id (VLUSR######)",
        "   full_name, email",
        "   age, gender, state, city",
        "   registration_datetime",
        "   acquisition_source",
        "   account_status, platform",
        "   email_verification_status",
        "   onboarding_status",
        "   xp_balance, referral_code",
        "   is_active_7d, is_active_30d"
    ], border_color="#38BDF8")

    # 2. Sessions (Top Left)
    draw_entity_box(0.8, 7.2, 3.6, 3.2, "SESSIONS (1:N from Users)", [
        "PK session_id (SESS#######)",
        "FK user_id",
        "   session_start, session_end",
        "   session_duration_seconds",
        "   device, platform, entry_point",
        "   exit_feature (5.89% null)",
        "   events_in_session"
    ], border_color="#38BDF8")

    # 3. Feature Events (Bottom Left)
    draw_entity_box(0.8, 1.8, 3.6, 3.8, "FEATURE_EVENTS (1:N)", [
        "PK event_id (EVT########)",
        "FK user_id",
        "FK session_id",
        "   event_datetime",
        "   feature_name (15 features)",
        "   event_name (40+ types)",
        "   event_status (Started/Success)",
        "   sequence_number",
        "   reward_related_flag"
    ], border_color="#38BDF8")

    # 4. Task Activity (Top Center-Right)
    draw_entity_box(11.6, 7.2, 3.6, 3.4, "TASK_ACTIVITY (1:N)", [
        "PK activity_id (ACT#######)",
        "FK user_id",
        "FK task_id (Catalog)",
        "FK session_id",
        "   task_category (8 types)",
        "   task_viewed_at, started_at",
        "   task_completed_at",
        "   task_status, failure_reason"
    ], border_color="#38BDF8")

    # 5. Proposed Rewards Ledger (Center Right)
    draw_entity_box(11.6, 3.6, 3.6, 3.2, "REWARDS_LEDGER (Proposed)", [
        "PK reward_transaction_id",
        "FK activity_id (1:1 Decoupled)",
        "FK user_id",
        "   source_feature, currency",
        "   reward_amount, balance_after",
        "   reward_lifecycle_status",
        "   idempotency_hash"
    ], border_color="#34D399")

    # 6. Proposed Wallet Transactions (Bottom Center)
    draw_entity_box(6.2, 0.8, 3.6, 3.6, "WALLET_TRANSACTIONS (Proposed)", [
        "PK wallet_transaction_id",
        "FK user_id",
        "   currency (VE/XP/Gem/Token)",
        "   transaction_type (11 types)",
        "   direction (CREDIT / DEBIT)",
        "   amount, balance_before",
        "   balance_after (Delta Check)",
        "   idempotency_key"
    ], border_color="#34D399")

    # 7. Proposed Withdrawals (Bottom Right)
    draw_entity_box(11.6, 0.4, 3.6, 3.0, "WITHDRAWAL_REQUESTS (Proposed)", [
        "PK withdrawal_id (WDR######)",
        "FK user_id",
        "   amount_tokens, amount_fiat",
        "   payout_method (UPI/PayPal)",
        "   withdrawal_status (5 stages)",
        "   gateway_provider, fee_amount"
    ], border_color="#F472B6")

    # Relationship Connector Arrows
    arrow_props = dict(arrowstyle="->", color="#94A3B8", lw=1.5)
    ax.annotate("", xy=(4.4, 8.8), xytext=(6.2, 8.8), arrowprops=arrow_props) # Users -> Sessions
    ax.annotate("", xy=(4.4, 4.2), xytext=(6.2, 6.2), arrowprops=arrow_props) # Users -> Events
    ax.annotate("", xy=(2.6, 5.0), xytext=(2.6, 7.2), arrowprops=arrow_props) # Sessions -> Events
    ax.annotate("", xy=(11.6, 8.8), xytext=(9.8, 8.8), arrowprops=arrow_props) # Users -> Task Activity
    ax.annotate("", xy=(13.4, 6.8), xytext=(13.4, 7.2), arrowprops=arrow_props) # Tasks -> Rewards Ledger
    ax.annotate("", xy=(9.8, 2.6), xytext=(11.6, 4.6), arrowprops=arrow_props) # Rewards -> Wallet
    ax.annotate("", xy=(8.0, 4.4), xytext=(8.0, 5.2), arrowprops=arrow_props) # Users -> Wallet
    ax.annotate("", xy=(11.6, 1.8), xytext=(9.8, 2.0), arrowprops=arrow_props) # Wallet -> Withdrawals

    # Legend
    legend_elements = [
        patches.Patch(facecolor="#38BDF8", label="Verified Source Entity (Simulated Pack)"),
        patches.Patch(facecolor="#34D399", label="Proposed Decoupled Financial Ledger"),
        patches.Patch(facecolor="#F472B6", label="Proposed 5-Stage Withdrawal Pipeline"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", facecolor="#1E293B", edgecolor="#334155", 
              fontsize=8.5, labelcolor="#E2E8F0")

    png_path = base_dir / "documentation" / "Entity_Relationship_Diagram.png"
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, facecolor="#0F172A")
    plt.close()
    print(f"Saved: {png_path}")

# ==============================================================================
# 4. Data_Model_Documentation.md
# ==============================================================================
def create_data_model_documentation():
    md_content = """# VELOOP REWARDS — LOGICAL DATA MODEL DOCUMENTATION

**Author:** Senior Data Analyst & Database Architect  
**Project:** VELOOP Rewards Data Analyst Internship (Task 01)  
**Execution Scope:** Days 16–18 (Data Architecture & Logical Modeling)  
**Document Generation Date:** 24 November 2026  
**Document Status:** Complete & Audited  
**Repository Location:** `documentation/Data_Model_Documentation.md`  

---

## 1. Executive Summary & Architecture Paradigm

The VELOOP Rewards data architecture is structured around a hybrid relational model optimized for:
1. **Third Normal Form (3NF) Ingestion & Ledgering:** Ensuring zero update anomalies, atomic financial consistency, and strict referential integrity across transactional tables.
2. **Dimensional Star Schema Presentation:** Supporting high-performance Power BI reporting and analytical queries without slow multi-table snowflaking.

### Critical Decoupling Milestone
The central architectural innovation in this model is the **complete decoupling of operational task telemetry from the financial ledger**:
- In the original raw pack, `reward_status` was conflated directly onto `05_Task_Activity`.
- In our target logical model, `task_activity` logs operational attempts, while `rewards_ledger` and `wallet_transactions` manage atomic double-entry balance credits, debit reversals, and multi-currency mutations.

---

## 2. Visual Entity-Relationship Architecture

The visual diagram is rendered and available at [Entity_Relationship_Diagram.png](file:///d:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Entity_Relationship_Diagram.png). The editable Mermaid definition is stored in [Entity_Relationship_Diagram.mmd](file:///d:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Entity_Relationship_Diagram.mmd).

```mermaid
erDiagram
    USERS ||--o{ SESSIONS : "1:N (initiates)"
    USERS ||--o{ FEATURE_EVENTS : "1:N (emits)"
    USERS ||--o{ DAILY_ACTIVITY : "1:N (accumulates)"
    USERS ||--o{ TASK_ACTIVITY : "1:N (executes)"
    USERS ||--o{ MILESTONES : "1:N (unlocks)"
    USERS ||--o{ REWARDS_LEDGER : "1:N (earns)"
    USERS ||--o{ WALLET_TRANSACTIONS : "1:N (transacts)"
    USERS ||--o{ WITHDRAWAL_REQUESTS : "1:N (requests)"
    USERS ||--o{ REFERRAL_RELATIONSHIPS : "1:N (refers/referee)"

    SESSIONS ||--o{ FEATURE_EVENTS : "1:N (contains)"
    SESSIONS ||--o{ TASK_ACTIVITY : "1:N (hosts)"
    SESSIONS ||--o{ MILESTONES : "1:N (triggers)"

    TASKS ||--o{ TASK_ACTIVITY : "1:N (catalog template)"

    TASK_ACTIVITY ||--o| REWARDS_LEDGER : "1:1 (decoupled credit)"
    REWARDS_LEDGER ||--o| WALLET_TRANSACTIONS : "1:1 (posts credit)"
    WITHDRAWAL_REQUESTS ||--o{ WALLET_TRANSACTIONS : "1:N (hold/settle/refund)"
```

---

## 3. Entity Classification & Cardinality Rules

### Core Dimension Entities

#### 1. `users` (Central Conformed Dimension)
- **Primary Key:** `user_id` (Regex `^VLUSR\\d{6}$`).
- **Cardinality:** 1:N with `sessions`, `feature_events`, `task_activity`, `wallet_transactions`, `withdrawal_requests`.
- **Integrity Rule:** Deleting a user is prohibited if child ledger transactions exist (`ON DELETE RESTRICT`).

#### 2. `tasks` (Offerwall & Earning Catalog Dimension)
- **Primary Key:** `task_id` (Regex `^TASK\\d{4}$`).
- **Cardinality:** 1:N with `task_activity`. Defines the template properties (category, offered reward, advertiser partner).

### Operational Fact Entities

#### 3. `sessions` (User Visit Telemetry Fact)
- **Primary Key:** `session_id` (Regex `^SESS\\d{7}$`).
- **Foreign Key:** `user_id` -> `users.user_id` (`ON DELETE RESTRICT`).
- **Cardinality:** 1:N with `feature_events` and `task_activity`.
- **Constraint:** `session_start <= session_end`; duration non-negative.

#### 4. `feature_events` (Granular Clickstream Fact)
- **Primary Key:** `event_id` (Regex `^EVT\\d{8}$`).
- **Foreign Keys:** `user_id`, `session_id`.
- **Grain:** One row per atomic user action across the 15 supported features.

#### 5. `task_activity` (Operational Earning Fact)
- **Primary Key:** `activity_id` (Regex `^ACT\\d{7}$`).
- **Foreign Keys:** `user_id`, `task_id`, `session_id`.
- **Grain:** One row per task execution attempt. Captures 8 categories and 5 failure reasons.

### Proposed Financial & Relational Ledger Entities

#### 6. `rewards_ledger` (Decoupled Reward Distribution Fact)
- **Primary Key:** `reward_transaction_id` (Regex `^RWD\\d{12}$`).
- **Foreign Keys:** `activity_id` (`ON DELETE RESTRICT`), `user_id`.
- **Unique Constraint:** `idempotency_hash` (`SHA256(user_id, activity_id, currency, amount)`).

#### 7. `wallet_transactions` (Double-Entry Balance Ledger Fact)
- **Primary Key:** `wallet_transaction_id` (Regex `^WLT\\d{12}$`).
- **Foreign Key:** `user_id`.
- **Mathematical Invariant:** `balance_after = balance_before +/- amount`.

#### 8. `withdrawal_requests` (Payout Pipeline Fact)
- **Primary Key:** `withdrawal_id` (Regex `^WDR\\d{12}$`).
- **Foreign Key:** `user_id`.
- **Fulfillment States:** `REQUESTED` -> `PROCESSING` -> `COMPLETED` / `REJECTED` / `REVERSED`.

#### 9. `referral_relationships` (Directed Viral Graph Fact)
- **Primary Key:** `referral_id` (BigSerial).
- **Foreign Keys:** `referrer_user_id` -> `users.user_id`, `referee_user_id` -> `users.user_id` (UNIQUE).
- **Self-Referral Constraint:** `CHECK (referrer_user_id <> referee_user_id)`.

---

## 4. Referential Integrity & Relational Verification

In our Phase 0 automated audit, `DatasetInspector.check_referential_integrity` verified:
- `user_id` foreign key validation across all 5 child tables against `Users_1000_Clean` achieved **100.0% integrity (0 orphan records)**.
- `session_id` foreign key validation across `Feature_Events` and `Task_Activity` achieved **100.0% integrity (0 orphan records)**.
- In `06_Milestones`, 40 records exhibit null `session_id`, correctly isolated as asynchronous background cron executions.

---

## 5. Deliverable References

- Master Data Dictionary: [Data_Dictionary.xlsx](file:///d:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Data_Dictionary.xlsx)
- Editable Mermaid Model: [Entity_Relationship_Diagram.mmd](file:///d:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Entity_Relationship_Diagram.mmd)
- Visual PNG Render: [Entity_Relationship_Diagram.png](file:///d:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Entity_Relationship_Diagram.png)
- Production DDL: [sql/Proposed_Database_Schema.sql](file:///d:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/sql/Proposed_Database_Schema.sql)
"""
    doc_path = base_dir / "documentation" / "Data_Model_Documentation.md"
    root_path = base_dir / "Data_Model_Documentation.md"
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    with open(root_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved: {doc_path}")

# ==============================================================================
# 5. Proposed_Database_Schema.sql synchronization
# ==============================================================================
def sync_proposed_database_schema():
    source_sql = base_dir / "sql" / "proposed_schema.sql"
    target_sql = base_dir / "sql" / "Proposed_Database_Schema.sql"
    if source_sql.exists():
        with open(source_sql, "r", encoding="utf-8") as f:
            content = f.read()
        with open(target_sql, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved: {target_sql}")

if __name__ == "__main__":
    print("Generating Phase 3 Deliverables...")
    create_data_dictionary()
    create_er_diagram_mmd()
    create_er_diagram_png()
    create_data_model_documentation()
    sync_proposed_database_schema()
    print("Phase 3 Deliverables generated successfully!")

