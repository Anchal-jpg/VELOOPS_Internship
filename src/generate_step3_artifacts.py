"""
Script to generate Step 3 Excel Workbooks:
1. Product_Data_Readiness_Audit.xlsx
2. Data_Coverage_Matrix.xlsx
3. Analytics_Gap_Assessment.xlsx
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
# 1. Product_Data_Readiness_Audit.xlsx
# ==============================================================================
def create_product_data_readiness_audit():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Readiness_Audit"
    
    headers = [
        "Audit_ID", "Product_Area", "Feature_Name", "User_Action",
        "System_Outcome", "Business_Question", "Current_Data_Status",
        "Source_Component", "Audit_Finding", "Readiness_Score", "Priority"
    ]
    ws.append(headers)
    
    audit_rows = [
        ("AUD-001", "Identity & Auth", "User Registration", "Submits signup form with email, demographic data", "Creates user record, hashes password, generates referral code", "What is our signup completion rate and CAC by marketing channel?", "Partially Ready (Profile in Users; Funnel events missing)", "Backend API / Client", "Only static profile stored in Users_1000_Clean; drop-off funnel unmeasurable", "50% - Partial", "Critical"),
        ("AUD-002", "Identity & Auth", "User Login", "Submits credentials or OAuth token", "Authenticates session, issues JWT, updates last_login_datetime", "What is user login frequency, churn propensity, and DAU/MAU ratio?", "Partially Ready (last_login only; Auth stream missing)", "Backend Auth Service", "last_login_datetime updated in-place; historical login timestamps lost", "40% - Low", "Critical"),
        ("AUD-003", "Identity & Auth", "Onboarding Tutorial", "Steps through screens explaining VEs, XP, and cashout mechanics", "Records onboarding completion flag in user record", "Which onboarding step causes the highest initial drop-off?", "Partially Ready (onboarding_status flag only)", "Mobile Client", "No step-by-step progress tracking; cannot optimize activation funnel", "40% - Low", "High"),
        ("AUD-004", "Advertising Core", "Watch Rewarded Ads", "Clicks 'Watch Ad', streams 30s video, closes player", "Ad network SDK verifies view via s2s callback; credits reward", "What is ad completion rate, eCPM yield, and ad fatigue per user?", "Ready (Events tracked; SDK callback unverified)", "Client SDK & Ad Network", "3,126 events in 03_Feature_Events (ad_started, ad_completed, ad_skipped)", "85% - High", "High"),
        ("AUD-005", "Tasks & Surveys", "Third-Party App Tasks", "Selects offer, downloads partner app, reaches level requirement", "Offerwall postback triggers reward allocation", "What is our partner offer conversion rate and chargeback rate?", "Ready (9,846 tasks in 05_Task_Activity)", "Offerwall Postback API", "Task status & failure reasons tracked; third-party transaction ID missing", "80% - High", "High"),
        ("AUD-006", "Tasks & Surveys", "Surveys & Questionnaires", "Answers screening questions and completes survey", "Survey provider postback validates completion; issues reward", "Why do users fail surveys (screening vs quota full vs timeout)?", "Ready (1,259 survey tasks logged)", "Survey Partner API", "Failure reasons tracked (Validation failed, Timeout, etc.)", "85% - High", "High"),
        ("AUD-007", "Security & Integrity", "CAPTCHA Challenge", "Solves interactive challenge", "Scoring algorithm evaluates bot likelihood; grants session pass", "What proportion of traffic represents automated bot farm attacks?", "Ready (2,733 events in 03_Feature_Events)", "Backend Security Engine", "captcha_started, captcha_completed, captcha_failed well tracked", "90% - High", "Critical"),
        ("AUD-008", "Gamification Core", "Daily Reward", "Opens reward calendar and taps 'Claim'", "Verifies 24h eligibility window; credits reward; updates streak", "What is the day-over-day claim retention among new cohorts?", "Ready (2,499 events in 03_Feature_Events)", "Backend Gamification", "daily_reward_viewed and daily_reward_claimed tracked", "90% - High", "High"),
        ("AUD-009", "Gamification Core", "Streak System", "Maintains consecutive daily app engagement", "Calculates streak count; applies multiplier; resets on broken streak", "At what streak milestone (Day 3, 7, 14) is long-term retention cemented?", "Ready (2,734 events in 03_Feature_Events)", "Backend Gamification", "streak_viewed, streak_claimed, streak_broken tracked", "90% - High", "High"),
        ("AUD-010", "Gamification Core", "Missions System", "Selects mission, tracks progress, completes daily quest", "Validates completion criteria; marks mission complete; credits prize", "Which missions drive the highest engagement versus abandonment?", "Ready (2,780 events in 03_Feature_Events)", "Backend Gamification", "mission_viewed, started, completed, abandoned tracked", "90% - High", "High"),
        ("AUD-011", "Engagement Core", "Tap & Earn", "Taps interactive widget repeatedly to accumulate micro-earnings", "Enforces tap rate limiter; batches micro-units; credits balance", "What is the average tap velocity and how many users hit bot limiters?", "Ready (2,654 events in 03_Feature_Events)", "Mobile Client & API", "tap_started and tap_completed tracked", "85% - High", "Medium"),
        ("AUD-012", "Engagement Core", "Mining Rewards", "Starts mining session; collects passive yield upon timer expiration", "Runs background timer; accumulates claimable balance", "What is optimal mining session duration to maximize daily app returns?", "Ready (2,616 events in 03_Feature_Events)", "Backend Timer Service", "mining_started, mining_activity, mining_stopped tracked", "85% - High", "Medium"),
        ("AUD-013", "Social & Growth", "Referral Program", "Generates and shares invite link; referee installs and registers", "Binds referee to referrer; checks qualification criteria; pays bonus", "What is VELOOP's K-factor and which channels generate high-LTV users?", "Partially Ready (UI events logged; Relational edge table missing)", "Backend Referral Engine", "referral_page_viewed, shared, created logged; no referee mapping table", "50% - Partial", "Critical"),
        ("AUD-014", "Status & Progression", "Level Progression", "Earns XP across platform activities to rank up", "Evaluates level thresholds; unlocks perks; fires level_up event", "How does user level correlate with 30-day retention and task completion?", "Ready (2,427 events in 03_Feature_Events)", "Backend XP Engine", "level_viewed and level_up tracked", "90% - High", "High"),
        ("AUD-015", "Chance & Entertainment", "Spin the Wheel", "Consumes spin credit to spin chance wheel", "Server-side RNG calculates prize tier; awards asset to user", "What is spin engagement frequency and how does it impact currency sinks?", "Ready (2,425 events in 03_Feature_Events)", "Backend RNG Engine", "spin_opened, spin_started, spin_completed tracked", "85% - High", "Medium"),
        ("AUD-016", "Social & Growth", "Follow & Earn", "Taps link to follow VELOOP or partner social account", "Verifies social auth / redirect; awards one-time completion bonus", "Which partner social channels generate the highest completion rate?", "Ready (1,659 events in 03_Feature_Events)", "Client & Redirect API", "follow_task_viewed and follow_task_completed tracked", "85% - High", "Medium"),
        ("AUD-017", "Gamification Core", "Leaderboards", "Views daily, weekly, or lifetime top earner rankings", "Aggregates rankings; renders cached leaderboard view", "Does viewing the leaderboard increase user daily earning activity?", "Ready (1,836 events in 03_Feature_Events)", "Cache / API Service", "leaderboard_viewed tracked", "80% - High", "Medium"),
        ("AUD-018", "Gamification Core", "Badges & Achievements", "Views achievements and claims unlocked milestone badges", "Checks achievement criteria; unlocks badge; assigns profile flair", "Which badges drive the strongest user completionist behavior?", "Ready (1,832 events in 03_Feature_Events)", "Backend Gamification", "badge_viewed and badge_earned tracked", "85% - High", "Medium"),
        ("AUD-019", "Financial Core", "Wallet & Balance", "Views balance snapshot and historical transaction statements", "Fetches multi-currency balances and pending transaction ledger", "What is VELOOP's outstanding virtual currency liability across users?", "NOT READY (wallet_viewed event only; Ledger missing)", "Financial Ledger Service", "Only 2,172 wallet_viewed events exist; zero transaction rows exist", "20% - Unready", "Critical"),
        ("AUD-020", "Economy & Liquidity", "Exchange Center", "Converts virtual currency pair (e.g. Gems to Tokens)", "Calculates exchange rate; debits source asset; credits target asset", "What is the net currency velocity and conversion volume across pairs?", "NOT READY (exchange_viewed event only; Ledger missing)", "Exchange Engine", "Only 1,690 exchange_viewed events exist; zero conversion rows exist", "20% - Unready", "Critical"),
        ("AUD-021", "Financial Core", "Withdrawal Pipeline", "Submits payout request to PayPal, UPI, Bank, or Crypto", "Validates balance; locks funds; checks fraud; triggers gateway payout", "What is payout success rate, processing latency, and gateway fee cost?", "NOT READY (Completely absent from provided data pack)", "Payout Gateway Engine", "Expected 1,200 records completely missing; no schema exists in raw data", "0% - Unready", "Critical"),
        ("AUD-022", "Customer Support", "Help Center & FAQs", "Navigates help center, browses FAQs, files support ticket", "Renders support articles; routes ticket to support desk", "What product issues generate the highest customer support contact rate?", "Partially Ready (Entry point in Sessions; Ticket data missing)", "Helpdesk API / Client", "Only entry_point=='Help/Support' in sessions; ticket logs absent", "30% - Low", "Medium"),
    ]
    
    for row in audit_rows:
        ws.append(row)
        
    file_path = base_dir / "documentation" / "Product_Data_Readiness_Audit.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "Product_Data_Readiness_Audit.xlsx")

# ==============================================================================
# 2. Data_Coverage_Matrix.xlsx
# ==============================================================================
def create_data_coverage_matrix():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data_Coverage_Matrix"
    
    headers = [
        "Product_Area", "Feature", "User_Action", "System_Action",
        "Business_Outcome", "Data_Required", "Proposed_Event",
        "Source", "Business_Question", "Status", "Priority"
    ]
    ws.append(headers)
    
    matrix_rows = [
        ("Identity", "Registration", "Submits email and password", "Validates credentials, creates user profile", "New registered user account", "user_id, email, acquisition_channel, device_id, timestamp", "user_registered", "Backend Auth", "What is total signup volume and CAC by channel?", "Proposed", "Critical"),
        ("Identity", "Email Verification", "Clicks verification link in email", "Marks email_verification_status as verified", "Verified email address reducing bot risk", "user_id, token, verified_timestamp, client_ip", "email_verified", "Backend Auth", "What percentage of users verify email within 24h?", "Proposed", "High"),
        ("Identity", "Authentication", "Enters credentials to log in", "Verifies hash, issues session token, updates login date", "Active authenticated session", "user_id, session_id, platform, auth_method, timestamp", "user_logged_in", "Backend Auth", "What is the return login frequency of active cohorts?", "Proposed", "Critical"),
        ("Identity", "Onboarding", "Views welcome screens and tips", "Advances step index, sets onboarding_status='Completed'", "User educated on earning mechanics", "user_id, session_id, step_index, total_steps, timestamp", "onboarding_step_completed", "Frontend App", "Where do new users abandon the initial walkthrough?", "Proposed", "High"),
        ("Advertising", "Watch Ads", "Taps 'Watch Ad' button", "Initializes ad SDK, requests ad unit", "User intent to watch advertisement", "user_id, session_id, ad_unit_id, network_provider, timestamp", "ad_started", "Client SDK", "How many ad requests are initiated daily?", "Confirmed", "High"),
        ("Advertising", "Watch Ads", "Watches full 30s rewarded video", "Verifies view completion via callback, queues reward", "Ad impression successfully monetized", "user_id, session_id, ad_unit_id, duration_seconds, eCPM_est", "ad_completed", "Ad Callback API", "What is our ad completion rate and revenue yield?", "Confirmed", "High"),
        ("Advertising", "Watch Ads", "Closes video player before 30s", "Cancels reward allocation, logs drop-off", "Incomplete ad view; no ad network payout", "user_id, session_id, ad_unit_id, seconds_watched, timestamp", "ad_skipped", "Client SDK", "What proportion of users skip ads and at what second?", "Confirmed", "Medium"),
        ("Tasks", "Task Discovery", "Browses task board or offerwall", "Queries active offers filtered by country/device", "User exposure to available monetizable tasks", "user_id, session_id, category, offer_count_rendered", "task_board_viewed", "Backend API", "How many available tasks does an active user view?", "Proposed", "High"),
        ("Tasks", "Task Execution", "Clicks 'Start Task' on selected offer", "Generates activity_id, redirects to offer URL", "Task attempt initialized", "activity_id, user_id, task_id, category, timestamp", "task_started", "Backend API", "Which task categories attract the highest start rate?", "Confirmed", "High"),
        ("Tasks", "Task Completion", "Finishes required action in third-party app", "Third-party postback received and validated", "Completed task awaiting credit approval", "activity_id, user_id, task_id, completion_timestamp", "task_completed", "Postback API", "What is the end-to-end task conversion rate?", "Confirmed", "High"),
        ("Tasks", "Task Failure", "Abandons task or fails validation criteria", "Logs failure_reason, closes task attempt", "Failed task attempt; user dissatisfaction", "activity_id, user_id, task_id, failure_reason, duration", "task_failed", "Backend API", "What are the primary failure reasons causing drop-off?", "Confirmed", "High"),
        ("Gamification", "Daily Reward", "Opens calendar and taps 'Claim'", "Verifies 24h cooldown, credits reward to balance", "Daily reward claimed, user retained", "user_id, session_id, day_number, reward_type, reward_amount", "daily_reward_claimed", "Backend Game", "What is the retention elasticity of daily reward streaks?", "Confirmed", "High"),
        ("Gamification", "Streak Rewards", "Logs in consecutive days and claims streak", "Increments streak counter, applies multiplier bonus", "Reinforced daily habit formation", "user_id, session_id, streak_days, multiplier, timestamp", "streak_claimed", "Backend Game", "What percentage of users maintain 7-day and 30-day streaks?", "Confirmed", "High"),
        ("Gamification", "Streak Rewards", "Fails to log in within 36 hours", "Resets streak counter to 0, sends recovery push", "Broken streak, churn risk elevated", "user_id, last_active_date, previous_streak_length, timestamp", "streak_broken", "Backend Cron", "How many users churn permanently after a broken streak?", "Confirmed", "Medium"),
        ("Gamification", "Missions", "Checks daily mission criteria", "Renders available quests and progress bars", "User awareness of structured daily goals", "user_id, session_id, mission_id, target_goal, timestamp", "mission_viewed", "Frontend App", "Do active mission viewers complete more tasks?", "Confirmed", "Medium"),
        ("Gamification", "Missions", "Achieves required quest milestones", "Marks mission complete, credits bonus tokens", "Completed daily mission loop", "user_id, session_id, mission_id, xp_awarded, timestamp", "mission_completed", "Backend Game", "What is the mission completion rate across user tiers?", "Confirmed", "High"),
        ("Security", "CAPTCHA Challenge", "Initiates sensitive action (cashout/tap)", "Triggers bot verification prompt", "Protected platform action", "user_id, session_id, challenge_type, trigger_feature", "captcha_started", "Security Engine", "How frequently do legitimate users encounter CAPTCHAs?", "Confirmed", "Critical"),
        ("Security", "CAPTCHA Challenge", "Solves challenge correctly", "Validates solution, unblocks user action", "Verified human user", "user_id, session_id, solve_duration_seconds, attempts", "captcha_completed", "Security Engine", "What is the CAPTCHA pass rate across device platforms?", "Confirmed", "Critical"),
        ("Security", "CAPTCHA Challenge", "Fails challenge or times out", "Flags session, restricts reward allocation", "Blocked automated script or suspicious user", "user_id, session_id, failure_type, ip_address, timestamp", "captcha_failed", "Security Engine", "What percentage of CAPTCHA challenges fail due to bots?", "Confirmed", "Critical"),
        ("Virality", "Referral", "Copies unique referral code or link", "Renders share modal, generates tracking link", "User intent to invite peers", "user_id, session_id, referral_code, share_channel", "referral_shared", "Frontend App", "What social channels are most popular for referral shares?", "Confirmed", "High"),
        ("Virality", "Referral", "New referee completes qualifying signup", "Links referee to referrer, triggers reward credit", "Viral acquisition completed; K-factor positive", "referrer_id, referee_id, referral_code, reward_payout", "referral_activated", "Backend Referral", "What is VELOOP's actual referral conversion velocity?", "Proposed", "Critical"),
        ("Financial", "Wallet View", "Opens wallet dashboard screen", "Queries multi-currency balance ledger", "User inspecting earnings and cashout readiness", "user_id, session_id, ve_balance, xp_balance, token_balance", "wallet_viewed", "Frontend App", "How often do users check balances before attempting cashout?", "Confirmed", "High"),
        ("Financial", "Balance Ledger", "System credits earnings from task or streak", "Appends immutable credit row to double-entry ledger", "Financially accurate ledger balance", "transaction_id, user_id, currency, amount, source_event_id", "wallet_credited", "Ledger Engine", "What is our daily net liability growth by currency?", "Proposed", "Critical"),
        ("Financial", "Currency Exchange", "Converts Gems to Tokens or Tokens to Cash", "Executes atomic debit/credit at active exchange rate", "Virtual asset converted for withdrawal liquidity", "exchange_id, user_id, from_curr, to_curr, from_amt, to_amt", "currency_exchanged", "Exchange Engine", "What is the daily exchange volume and treasury spread margin?", "Proposed", "Critical"),
        ("Financial", "Withdrawal Request", "Selects payout method (UPI/PayPal) and amount", "Validates balance, freezes funds, logs request", "Pending payout request submitted", "withdrawal_id, user_id, amount_fiat, payout_method, address", "withdrawal_requested", "Payout Engine", "What is total daily withdrawal demand across payout methods?", "Proposed", "Critical"),
        ("Financial", "Withdrawal Processing", "Sends batch payout instruction to gateway API", "Sets status to 'Processing', awaits webhook callback", "Payout instruction transmitted to payment rail", "withdrawal_id, gateway_ref_id, processing_started_at", "withdrawal_processing", "Gateway API", "What is our average payment gateway settlement latency?", "Proposed", "Critical"),
        ("Financial", "Withdrawal Completed", "Receives successful settlement webhook", "Marks status 'Completed', unlocks settled balance", "Successful user payout; realized reward value", "withdrawal_id, gateway_fee, settled_amount, completed_at", "withdrawal_completed", "Gateway Webhook", "What is our final payout success rate and gateway fee drag?", "Proposed", "Critical"),
        ("Financial", "Withdrawal Rejected", "KYC or fraud check fails, or gateway rejects", "Rejects payout, unfreezes balance or bans account", "Prevented fraudulent cashout or bounced account", "withdrawal_id, rejection_code, failure_reason, rejected_at", "withdrawal_rejected", "Risk Engine", "What are the primary rejection reasons (invalid UPI/KYC/fraud)?", "Proposed", "Critical"),
        ("Financial", "Withdrawal Reversal", "Settlement reverses post-success (chargeback)", "Debits user balance, logs financial recovery", "Bounced bank wire or reversed payment", "withdrawal_id, reversal_ref, reason_code, reversed_at", "withdrawal_reversed", "Gateway Webhook", "What is our post-settlement reversal rate?", "Proposed", "High"),
    ]
    
    for row in matrix_rows:
        ws.append(row)
        
    file_path = base_dir / "documentation" / "Data_Coverage_Matrix.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "Data_Coverage_Matrix.xlsx")

# ==============================================================================
# 3. Analytics_Gap_Assessment.xlsx
# ==============================================================================
def create_analytics_gap_assessment():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Gap_Assessment"
    
    headers = [
        "Gap_ID", "Product_Area", "Gap_Title", "Current_Data_State",
        "Root_Cause", "Business_Analytical_Impact", "Financial_Fraud_Risk",
        "Technical_Remediation_Plan", "Priority", "Effort_Estimate", "Owner"
    ]
    ws.append(headers)
    
    gaps = [
        ("GAP-001", "Financial Core", "Complete Absence of Wallet Transaction Ledger", "Zero transaction records exist; only wallet_viewed event in 03_Feature_Events", "Financial ledger microservice not yet integrated with telemetry pipeline", "Cannot measure balance growth, currency liability, inflation, or transaction history", "Critical: Inability to audit user balances or detect double-spending", "Deploy immutable double-entry ledger table (wallet_transactions) in PostgreSQL/DW", "Critical", "5 Days", "Data Eng / Backend"),
        ("GAP-002", "Financial Core", "Complete Absence of Withdrawal Dataset", "Expected 1,200 withdrawal records in PDF Sec 28 are missing from data pack", "Payout gateway integration not reflected in current simulated data export", "Cannot calculate payout success rate, settlement latency, gateway fees, or cashout demand", "Critical: Financial blindspot; cashout is the primary user retention value proposition", "Implement withdrawal_requests table with 5-stage state machine and gateway webhooks", "Critical", "4 Days", "Data Eng / Backend"),
        ("GAP-003", "Earning & Rewards", "Coupled Task-Reward Logging Without Dedicated Reward Ledger", "reward_status logged directly in 05_Task_Activity without currency type or amounts", "Relational shortcut in initial simulated data generator", "Cannot determine which currency was credited (VE vs XP vs Gems) or audit reversals", "High: Fraudulent tasks cannot be reversed without mutating operational task records", "Create dedicated rewards_ledger table with transaction_id, currency, amount, and status", "Critical", "3 Days", "Data Eng"),
        ("GAP-004", "Virality & Growth", "Missing Relational Referral Edge Table", "Only referral_code and referral_source_detail exist in Users; no edge graph", "Referral attribution table omitted from raw simulated dataset pack", "Cannot calculate viral K-factor, multi-tier referral trees, or identify referral fraud rings", "Critical: Sybil attack vulnerability; users self-referring without validation", "Create referral_relationships table linking referrer_id, referee_id, and qualification_time", "Critical", "3 Days", "Backend / Analytics"),
        ("GAP-005", "Identity & Auth", "Absence of Granular Registration & Auth Event Stream", "Only final profile attributes stored in Users; no registration funnel events", "Frontend auth screens do not emit client-side telemetry events", "Cannot determine signup drop-off rate by screen, password validation failure, or OAuth drop", "Medium: High marketing spend wasted on unoptimized signup funnels", "Instrument client events: registration_started, step_completed, auth_failed, auth_success", "High", "2 Days", "Frontend Mobile"),
        ("GAP-006", "Economy & Liquidity", "Exchange Center Tracking Limited to Page View", "Only exchange_viewed (1,690 times) in 03_Feature_Events; zero conversion records", "Exchange transaction logging not routed to analytics event stream", "Cannot track currency conversion volumes, exchange spread margins, or token sinks", "High: Currency arbitrage and token inflation run unmonitored", "Instrument currency_exchanged event and create exchange_transactions ledger table", "High", "3 Days", "Backend / Data Eng"),
        ("GAP-007", "Advertising Core", "Ad Network Partner Callback Telemetry Missing", "ad_started and ad_completed logged client-side; no server-to-server callback data", "Ad network SDK callbacks not captured in data warehouse", "Discrepancy between client-reported ad views and partner payable impressions unmeasurable", "High: Ad network clawbacks and client-side ad spoofing undetected", "Route ad network postback webhooks to data pipeline; reconcile client vs server impressions", "High", "3 Days", "Data Eng / AdOps"),
        ("GAP-008", "Session Management", "High Proportion of Missing Exit Feature in Sessions (5.89%)", "466 out of 7,913 sessions have null exit_feature in 02_Sessions", "Abrupt app backgrounding, OS termination, or crashes bypass exit logging", "Distorts session exit funnel and journey analysis", "Medium: App instability and crashes masked as normal session terminations", "Implement client lifecycle heartbeat and background state persistence handler", "Medium", "2 Days", "Mobile Eng"),
        ("GAP-009", "Data Integrity", "Orphan Milestone Records Without Session Context (0.83%)", "40 milestone records in 06_Milestones have null session_id", "Milestones triggered by asynchronous cron jobs do not capture triggering session context", "Breaks session-level milestone velocity analysis and multi-touch attribution", "Low: Session-level funnel reporting breaks on inner joins", "Allow null session_id for system-triggered milestones and add trigger_source column", "Medium", "1 Day", "Data Eng"),
        ("GAP-010", "Economy & Balances", "Absence of Multi-Currency Balance Snapshot History", "Only xp_balance stored in Users_1000_Clean; VE, Gem, and Token balances absent", "Balance state not captured in periodic daily snapshots", "Cannot compute company-wide daily virtual currency reserve liabilities or inflation rates", "Critical: Inability to forecast cashout liquidity requirements", "Implement daily user_balance_snapshots table across all 5 virtual currency types", "Critical", "3 Days", "Data Eng"),
        ("GAP-011", "Security & Fraud", "No Device Fingerprinting or IP Geolocation History", "Only static 'primary_device' and 'platform' strings in Users; no IP or device hash", "Security attributes omitted from initial simulated user profiles", "Cannot detect device-farm farming, proxy/VPN abuse, or multi-accounting from single device", "Critical: High exposure to automated bot syndicates draining reward pools", "Log device_fingerprint_hash, ip_address, and vpn_flag on all session starts", "Critical", "3 Days", "Security Eng"),
        ("GAP-012", "Tasks & Surveys", "Third-Party Offerwall Transaction ID Not Linked to Task Activity", "activity_id and task_id exist, but partner_transaction_id is absent", "Third-party partner identifiers not propagated through client SDK", "Cannot reconcile advertiser chargebacks with specific internal task records", "High: Unable to dispute chargebacks or deduct rewards from fraudulent users", "Add partner_transaction_id and partner_name to task_activity schema", "High", "2 Days", "Backend / Offerwall"),
        ("GAP-013", "Gamification Core", "Streak Freeze and Recovery Mechanics Not Tracked", "streak_viewed, claimed, and broken exist, but streak_freeze used is absent", "Streak freeze feature not yet modeled in telemetry events", "Cannot evaluate monetization impact of selling streak freeze power-ups", "Medium: Missed revenue opportunity in micro-transaction economy", "Add streak_freeze_purchased and streak_freeze_consumed events to tracking plan", "Medium", "2 Days", "Product / Mobile"),
        ("GAP-014", "Customer Experience", "Customer Support Ticket Resolution & CSAT Missing", "Only entry_point=='Help/Support' in sessions; ticket status and CSAT absent", "Helpdesk ticketing platform (Zendesk/Freshdesk) not connected to data pipeline", "Cannot correlate product bugs, task failures, or withdrawal delays with user churn", "Medium: Customer friction points in earning and cashout remain unquantified", "Ingest customer support ticket webhook stream into data warehouse", "Medium", "2 Days", "Support / Data Eng"),
        ("GAP-015", "Lifecycle & Marketing", "Push Notification & Engagement Campaign Attribution Missing", "entry_point=='Push Notification' exists, but campaign_id and message_id absent", "Marketing automation platform (Braze/OneSignal) telemetry disconnected from app events", "Cannot determine push open rate, campaign ROI, or optimal re-engagement send times", "High: Marketing push budget spent without attribution or conversion tracking", "Enrich session entry metadata with campaign_id, creative_id, and deep_link_slug", "High", "2 Days", "Growth / Data Eng"),
    ]
    
    for row in gaps:
        ws.append(row)
        
    file_path = base_dir / "documentation" / "Analytics_Gap_Assessment.xlsx"
    save_styled_workbook(wb, file_path)
    wb.save(base_dir / "Analytics_Gap_Assessment.xlsx")

if __name__ == "__main__":
    print("Generating Step 3 Excel Workbooks...")
    create_product_data_readiness_audit()
    create_data_coverage_matrix()
    create_analytics_gap_assessment()
    print("Step 3 Excel Workbooks generated successfully!")

