"""
Script to generate Step 4 Excel Workbook:
User_Analytics_Specification.xlsx
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

def create_user_analytics_specification():
    wb = openpyxl.Workbook()
    
    # Sheet 1: Identifier Standards
    ws1 = wb.active
    ws1.title = "Identifier_Standards"
    headers1 = [
        "Identifier_Name", "Format_Pattern", "Regex_Validator",
        "Scope", "Generation_Source", "Persistence_Rule",
        "Current_Status", "Domain_Rules"
    ]
    ws1.append(headers1)
    
    id_rows = [
        ("user_id", "VLUSR followed by 6 digits (e.g. VLUSR000001)", r"^VLUSR\d{6}$", "Global User Profile", "Backend User Service on successful signup", "Permanent immutable primary key; never re-used or updated", "Available (Verified in Users_1000_Clean)", "Must strictly match regex; 0 nulls allowed; unique constraint"),
        ("session_id", "SESS followed by 7 digits (e.g. SESS0000001)", r"^SESS\d{7}$", "App Session", "Client SDK on app foreground / session init", "Persists until app backgrounded >30m or explicit logout", "Available (Verified in 02_Sessions)", "Unique per session; max duration 3,600s; binds all child events"),
        ("event_id", "EVT followed by 8 digits (e.g. EVT00000001)", r"^EVT\d{8}$", "Atomic Event", "Client SDK / Telemetry Gateway", "Ephemeral streaming event; deduplicated at ingestion", "Available (Verified in 03_Feature_Events)", "Globally unique event identifier; strict monotonically increasing format"),
        ("device_id", "UUID v4 or Secure Android/IDFA hash", r"^[a-f0-9\-]{36}$", "Physical Device", "Hardware / OS API (Widevine/Keymaster)", "Persists across app installs until OS factory reset", "Proposed (Only generic device string available)", "Critical for detecting multi-account device farms and bot networks"),
        ("install_id", "UUID v4 generated on first app launch", r"^[a-f0-9\-]{36}$", "App Installation", "Client Application Local Storage", "Regenerated on app re-installation or data wipe", "Proposed (Currently absent)", "Used to measure pre-registration install-to-signup drop-off"),
    ]
    for row in id_rows:
        ws1.append(row)
        
    # Sheet 2: User Profile Schema
    ws2 = wb.create_sheet(title="User_Profile_Schema")
    headers2 = [
        "Field_Name", "Data_Type", "Requirement", "Default_Value",
        "Validation_Rule", "Data_Classification", "Analytical_Use_Case"
    ]
    ws2.append(headers2)
    schema_rows = [
        ("user_id", "VARCHAR(11)", "Required", "None", "Primary Key; Regex ^VLUSR\d{6}$", "Available (Clean)", "Core relational join key across all analytical marts"),
        ("full_name", "VARCHAR(100)", "Required", "None", "Non-empty string; length 2-100", "Available (Clean)", "Personalization & KYC bank account name verification"),
        ("email", "VARCHAR(150)", "Required", "None", "Valid RFC 5322 email regex; Unique", "Available (Clean)", "Identity verification, communications & duplicate user detection"),
        ("age", "INT", "Required", "None", "Value between 13 and 100", "Available (Clean)", "Demographic segmentation & legal compliance (COPPA / GDPR-K)"),
        ("gender", "VARCHAR(20)", "Required", "Prefer not to say", "Enum: Male, Female, Other, Prefer not to say", "Available (Clean)", "Ad personalization & demographic cohort analysis"),
        ("state", "VARCHAR(50)", "Required", "None", "Valid Indian State / Territory", "Available (Clean)", "Regional task availability & location-based partner targeting"),
        ("city", "VARCHAR(50)", "Optional", "NULL", "Standardized city name", "Available (Clean)", "Urban vs rural earning and offerwall engagement profiling"),
        ("registration_datetime", "TIMESTAMP", "Required", "CURRENT_TIMESTAMP", "Valid past timestamp; <= last_login", "Available (Clean)", "Cohort grouping (acquisition date), tenure & lifecycle age"),
        ("acquisition_source", "VARCHAR(50)", "Required", "Organic", "Enum: Organic, Facebook Ads, Google Ads, Referral, Influencer", "Available (Clean)", "Marketing attribution, CAC calculation & channel quality"),
        ("referral_source_detail", "VARCHAR(50)", "Optional", "NULL", "Referrer code if acquired via referral", "Available (Clean)", "Referral link attribution & viral growth tracking"),
        ("primary_device", "VARCHAR(50)", "Required", "Mobile", "Enum: Mobile, Desktop, Tablet", "Available (Clean)", "Device breakdown & responsive feature optimization"),
        ("platform", "VARCHAR(20)", "Required", "Android", "Enum: Android, iOS, Web", "Available (Clean)", "Cross-platform performance, crash rates & app store attribution"),
        ("account_status", "VARCHAR(20)", "Required", "Pending", "Enum: Active, Suspended, Pending, Deactivated", "Available (Clean)", "Churn tracking, fraud suspension & active user base modeling"),
        ("email_verification_status", "VARCHAR(20)", "Required", "Unverified", "Enum: Verified, Unverified", "Available (Clean)", "Security readiness & bot farm risk filtering"),
        ("onboarding_status", "VARCHAR(20)", "Required", "Incomplete", "Enum: Completed, Incomplete", "Available (Clean)", "Activation rate & D1 user drop-off analysis"),
        ("last_login_datetime", "TIMESTAMP", "Optional", "NULL", ">= registration_datetime; <= current_time", "Available (Clean)", "Recency calculation, DAU/WAU/MAU activity flags"),
        ("lifetime_sessions", "INT", "Required", "0", "Non-negative integer (>= 0)", "Available (Clean)", "User engagement frequency & session frequency tiers"),
        ("active_days", "INT", "Required", "0", "Non-negative integer (<= days_since_reg)", "Available (Clean)", "L28 engagement intensity & stickiness index"),
        ("xp_balance", "INT", "Required", "0", "Non-negative integer (>= 0)", "Available (Clean)", "User status progression & level threshold calculation"),
        ("referral_code", "VARCHAR(20)", "Required", "None", "Unique alphanumeric string; length 6-12", "Available (Clean)", "Viral loop attribution & invite sharing"),
        ("days_since_registration", "INT", "Required", "0", "Computed: CURRENT_DATE - reg_date", "Available (Clean)", "Tenure bracket segmentation (D0, D1-7, D8-30, D30+)"),
        ("is_active_7d", "BOOLEAN", "Required", "False", "True if last_login >= NOW() - 7 days", "Available (Clean)", "Weekly active user (WAU) classification"),
        ("is_active_30d", "BOOLEAN", "Required", "False", "True if last_login >= NOW() - 30 days", "Available (Clean)", "Monthly active user (MAU) classification"),
        ("consent_status", "VARCHAR(20)", "Required", "Granted", "Enum: Granted, Denied, Pending", "Available (Clean)", "Data privacy compliance (DPDP Act / GDPR)"),
        ("marketing_opt_in", "BOOLEAN", "Required", "False", "Boolean True/False", "Available (Clean)", "Push & email marketing campaign addressability"),
        ("account_created_via", "VARCHAR(30)", "Required", "Direct", "Enum: Direct, Google_OAuth, Apple_ID, Facebook", "Available (Clean)", "Authentication channel friction and security analysis"),
        ("country", "VARCHAR(10)", "Required", "IN", "ISO 3166-1 alpha-2 country code", "Available (Clean)", "Geographic compliance & localized currency settlement"),
        ("phone_number_verified", "BOOLEAN", "Optional", "False", "Boolean True/False", "Proposed", "Two-factor auth and high-value withdrawal security"),
        ("kyc_tier", "VARCHAR(20)", "Required", "Tier_0", "Enum: Tier_0 (None), Tier_1 (ID), Tier_2 (Bank)", "Proposed", "AML / financial cashout threshold compliance"),
        ("fraud_risk_score", "DECIMAL(4,2)", "Optional", "0.00", "Score between 0.00 and 100.00", "Proposed", "Automated cashout hold and suspicious activity flagging"),
    ]
    for row in schema_rows:
        ws2.append(row)
        
    # Sheet 3: Account Lifecycle States
    ws3 = wb.create_sheet(title="Account_Lifecycle_States")
    headers3 = [
        "State_Name", "State_Type", "Entry_Condition",
        "Exit_Condition", "Allowed_Transitions", "Analytical_Definition"
    ]
    ws3.append(headers3)
    lifecycle_rows = [
        ("Registered_Unverified", "Initial", "User submits signup form", "Clicks email verification link or completes phone OTP", "Active_Onboarded, Suspended_Fraud, Abandoned", "Top-of-funnel registered user; restricted from cashout"),
        ("Active_Onboarded", "Core Active", "Completes walkthrough and email verification", "Inactivity > 30 days or Terms violation", "Dormant, Suspended_Fraud, Deactivated", "Fully active user eligible for all earning and payout features"),
        ("Dormant", "At Risk", "No session activity for > 30 consecutive days", "User initiates new authenticated login session", "Active_Onboarded, Churned_Permanent, Deactivated", "High-risk retention drop-off; target for push re-engagement"),
        ("Suspended_Fraud", "Restricted", "Triggered by multi-accounting, VPN, bot CAPTCHA failures", "Manual review approval or permanent deactivation", "Active_Onboarded, Deactivated", "Account locked; reward credits frozen; withdrawals blocked"),
        ("Deactivated", "Terminal", "User requests account deletion (GDPR) or confirmed bot", "None (Terminal state)", "None", "Permanently purged; PII anonymized; ledger retained for audit"),
        ("Churned_Permanent", "Analytical", "No session activity for > 90 consecutive days", "User returns via win-back campaign", "Active_Onboarded", "Statistically lost user; excluded from DAU/MAU reporting"),
    ]
    for row in lifecycle_rows:
        ws3.append(row)
        
    # Sheet 4: Funnel Events Specification
    ws4 = wb.create_sheet(title="Funnel_Events_Specification")
    headers4 = [
        "Event_Name", "Funnel_Phase", "Trigger_Action", "Payload_Properties",
        "Delivery_Channel", "Tracking_Status", "Priority"
    ]
    ws4.append(headers4)
    funnel_rows = [
        ("registration_started", "Registration", "User views initial signup screen", "acquisition_channel, device_id, platform, client_ip", "Client Telemetry", "Proposed (Critical Gap)", "Critical"),
        ("registration_step_completed", "Registration", "Completes step (credentials, profile, demographic)", "step_name, step_index, duration_seconds", "Client Telemetry", "Proposed (Critical Gap)", "High"),
        ("registration_completed", "Registration", "Successfully creates user account in database", "user_id, account_created_via, referral_code_used", "Server-Side API", "Proposed (Critical Gap)", "Critical"),
        ("email_verification_sent", "Verification", "System transmits verification email with token", "user_id, email_domain, dispatch_timestamp", "Server-Side Auth", "Proposed (Critical Gap)", "Medium"),
        ("email_verified", "Verification", "User clicks verification link; token validated", "user_id, latency_to_verify_seconds", "Server-Side Auth", "Proposed (Critical Gap)", "High"),
        ("user_login_attempt", "Authentication", "User submits credentials on login screen", "auth_method (Password/Google), client_ip", "Client Telemetry", "Proposed (Critical Gap)", "High"),
        ("user_login_success", "Authentication", "Credentials verified; session JWT issued", "user_id, session_id, platform, is_first_login_today", "Server-Side Auth", "Proposed (Critical Gap)", "Critical"),
        ("user_login_failed", "Authentication", "Authentication fails (bad password/rate limit)", "failure_reason, attempt_count, client_ip", "Server-Side Auth", "Proposed (Critical Gap)", "High"),
        ("onboarding_started", "Onboarding", "User enters welcome walkthrough carousel", "user_id, session_id, platform", "Client Telemetry", "Proposed (Critical Gap)", "High"),
        ("onboarding_step_viewed", "Onboarding", "Views specific onboarding explainer card", "user_id, step_index, card_topic (VEs/XP/Cashout)", "Client Telemetry", "Proposed (Critical Gap)", "Medium"),
        ("onboarding_completed", "Onboarding", "Completes final tutorial step and enters app", "user_id, total_onboarding_duration_seconds", "Client Telemetry", "Proposed (Critical Gap)", "High"),
        ("onboarding_skipped", "Onboarding", "User taps 'Skip Tutorial' button", "user_id, step_index_when_skipped", "Client Telemetry", "Proposed (Critical Gap)", "Medium"),
    ]
    for row in funnel_rows:
        ws4.append(row)
        
    # Sheet 5: Analytical Use Cases
    ws5 = wb.create_sheet(title="Analytical_Use_Cases")
    headers5 = [
        "Use_Case_ID", "Analytical_Domain", "Objective",
        "Key_Metrics_Generated", "SQL_Table_Dependencies", "Business_Impact"
    ]
    ws5.append(headers5)
    use_case_rows = [
        ("UC-USER-01", "Acquisition Attribution", "Measure marketing channel CAC and signup conversion velocity", "Signup Volume, CAC, Channel Conversion Rate, D7 Retention by Channel", "users, event_stream", "Reallocate ad spend to high-LTV acquisition sources"),
        ("UC-USER-02", "Activation Funnel", "Identify friction points in signup and onboarding walkthrough", "Step Drop-off %, Onboarding Completion %, Time-to-First-Task", "event_stream (funnel events)", "Streamline onboarding to boost D1 activation by 15-25%"),
        ("UC-USER-03", "Retention & Churn", "Track daily, weekly, and monthly user stickiness (DAU/WAU/MAU)", "DAU, WAU, MAU, L28 Engagement Ratio, Cohort Decay Curves", "daily_activity, sessions, users", "Identify early churn warning signals and trigger win-back automations"),
        ("UC-USER-04", "Identity & Bot Shield", "Detect multi-accounting and bot syndicates exploiting welcome bonuses", "Accounts-per-Device, IP-Collision Rate, CAPTCHA Failure Rate", "users, sessions, security_logs", "Block bot syndicates before virtual currencies are cashed out"),
        ("UC-USER-05", "Demographic Targeting", "Analyze earning behavior across age brackets, genders, and regions", "Task Completion by Age/Gender, Regional Earning Index", "users, task_activity", "Attract targeted demographic advertisers willing to pay premium eCPMs"),
    ]
    for row in use_case_rows:
        ws5.append(row)
        
    file_path = base_dir / "documentation" / "User_Analytics_Specification.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "User_Analytics_Specification.xlsx")

if __name__ == "__main__":
    print("Generating Step 4 Excel Workbook...")
    create_user_analytics_specification()
    print("Step 4 Excel Workbook generated successfully!")

