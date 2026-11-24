"""
Script to generate Phase 2 Deliverable: Event_Tracking_Plan.xlsx
Comprehensive enterprise event tracking plan covering 40+ events across 12 product areas.
"""

import sys
from pathlib import Path
import openpyxl

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

def create_event_tracking_plan():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Sheet 1: Production_Event_Tracking_Plan
    # ----------------------------------------------------
    ws1 = wb.active
    ws1.title = "Event_Tracking_Plan"
    
    headers1 = [
        "Event_ID", "Event_Name", "Product_Area", "Trigger",
        "Event_Definition", "User_ID", "Session_ID", "Transaction_ID",
        "Timestamp_Handling", "Required_Properties", "Optional_Properties",
        "Property_Data_Types", "Allowed_Values", "Validation_Rules",
        "Event_Source", "Business_Purpose", "KPI_Dependency",
        "Deduplication_Rule", "Implementation_Status", "Priority", "Acceptance_Criteria"
    ]
    ws1.append(headers1)
    
    events = [
        # 1. User and Account
        ("EVT-DEF-001", "user_registered", "User and Account", "User submits registration form and account is created",
         "Fires once when a new user account is committed to the database", "Required", "Optional", "N/A",
         "ISO 8601 UTC timestamp", "user_id, email, acquisition_source, platform", "referral_code_used, utm_campaign, utm_medium",
         "String, String, String, String", "platform IN ('Android', 'iOS', 'Web')", "email regex valid; user_id must be unique",
         "Backend User Service", "Measure top-of-funnel account creation velocity", "New Users (NU), Signup CAC",
         "Unique on user_id", "Proposed (Profile exists in Users)", "Critical", "Emits 201 Created; event payload lands in Kafka topic within 500ms"),
         
        ("EVT-DEF-002", "user_profile_updated", "User and Account", "User updates profile attributes (city, state, marketing preference)",
         "Fires when demographic or notification consent fields are modified", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, updated_fields_list", "state, city, marketing_opt_in",
         "String, String, Array[String]", "updated_fields not empty", "user_id exists; fields match schema",
         "Backend User Service", "Track profile completeness and consent changes", "Consent Compliance Rate",
         "Deduplicate by user_id + timestamp (1s window)", "Proposed", "Medium", "Logs previous and new values in audit log"),
         
        ("EVT-DEF-003", "user_account_deleted", "User and Account", "User requests account deletion under privacy rights (GDPR/DPDP)",
         "Fires when account termination is confirmed and PII purge initiates", "Required", "Optional", "N/A",
         "ISO 8601 UTC timestamp", "user_id, deletion_reason_category", "feedback_text",
         "String, String, String", "reason IN ('Privacy', 'Unused', 'Poor_Earnings', 'Bugs', 'Other')", "user_id must be Active or Dormant",
         "Backend Auth Service", "Measure terminal churn reasons and regulatory compliance", "Churn Velocity, Deactivation Rate",
         "Unique on user_id", "Proposed", "High", "PII scrubbed from operational tables; ledger anonymized"),

        # 2. Registration and Onboarding
        ("EVT-DEF-004", "registration_started", "Registration & Onboarding", "User arrives on initial registration screen",
         "Fires when registration screen renders for a prospective user", "Optional (anonymous_id)", "Required (install_session)", "N/A",
         "ISO 8601 UTC timestamp", "anonymous_id, platform, client_ip", "utm_source, utm_campaign, referrer_url",
         "String, String, String", "platform IN ('Android', 'iOS', 'Web')", "anonymous_id valid UUID v4",
         "Mobile Client SDK", "Determine install-to-registration conversion funnel drop-off", "Registration Funnel Conversion %",
         "Deduplicate by anonymous_id (5m window)", "Proposed", "High", "Fires on screen view before user interaction"),

        ("EVT-DEF-005", "onboarding_step_viewed", "Registration & Onboarding", "User advances to an onboarding tutorial screen",
         "Fires when a specific walkthrough slide or card is displayed", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, step_index, step_name", "time_on_previous_step_sec",
         "String, String, Integer, String", "step_index BETWEEN 1 AND 5", "step_index > 0; step_name valid enum",
         "Mobile Client SDK", "Identify specific tutorial slides where new users abandon", "Onboarding Step Drop-off %",
         "Deduplicate by session_id + step_index", "Proposed", "High", "Emitted immediately upon slide transition"),

        ("EVT-DEF-006", "onboarding_completed", "Registration & Onboarding", "User views final onboarding card and taps 'Get Started'",
         "Fires when onboarding walkthrough is fully finished", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, total_duration_seconds", "starter_bonus_awarded",
         "String, String, Float, Boolean", "total_duration_seconds >= 2.0", "user_id exists; status updated to Completed",
         "Mobile Client SDK", "Measure D0 activation rate and onboarding efficiency", "Onboarding Completion Rate",
         "Unique per user_id", "Proposed (Status exists in Users)", "Critical", "Sets onboarding_status = 'Completed' in database"),

        ("EVT-DEF-007", "onboarding_skipped", "Registration & Onboarding", "User taps 'Skip Tutorial' button",
         "Fires when user bypasses the onboarding walkthrough", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, step_index_when_skipped", "None",
         "String, String, Integer", "step_index BETWEEN 1 AND 4", "step_index matches current card",
         "Mobile Client SDK", "Evaluate whether tutorial is considered intrusive by users", "Onboarding Skip Rate",
         "Deduplicate by session_id", "Proposed", "Medium", "Sets onboarding_status = 'Incomplete'"),

        # 3. Login and Sessions
        ("EVT-DEF-008", "user_logged_in", "Login & Sessions", "User successfully authenticates and receives JWT token",
         "Fires upon every successful login authentication", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, auth_method, platform", "is_first_login_today, device_model",
         "String, String, String, String", "auth_method IN ('Password', 'Google_OAuth', 'Apple_ID', 'Biometric')", r"session_id must match regex ^SESS\d{7}$",
         "Backend Auth Gateway", "Track login frequency, DAU, and multi-factor adoption", "DAU, MAU, Retention D1/D7/D30",
         "Unique per session_id", "Proposed (last_login in Users)", "Critical", "Updates users.last_login_datetime immediately"),

        ("EVT-DEF-009", "user_login_failed", "Login & Sessions", "Authentication attempt fails due to invalid password or rate limit",
         "Fires when credentials validation returns an error", "Optional", "Optional", "N/A",
         "ISO 8601 UTC timestamp", "attempted_login_identifier, failure_reason, client_ip", "consecutive_failure_count",
         "String, String, String", "failure_reason IN ('Bad_Password', 'User_Not_Found', 'Locked', 'Rate_Limited')", "failure_reason must be populated",
         "Backend Auth Gateway", "Detect credential stuffing attacks and forgotten password friction", "Login Failure Rate, Account Lockout Rate",
         "Deduplicate by IP + timestamp (1s window)", "Proposed", "High", "Fires on HTTP 401/429 response"),

        ("EVT-DEF-010", "session_start", "Login & Sessions", "Application brought to foreground or launched",
         "Fires when a new app session lifecycle begins", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "session_id, user_id, entry_point, device, platform", "app_version, connection_type",
         "String, String, String, String, String", "entry_point IN ('Dashboard', 'Push Notification', 'Deep Link', 'Direct Launch')", "session_start <= session_end",
         "Client Telemetry SDK", "Denominator for engagement depth, visits per day", "Total Sessions, Average Visits/DAU",
         "Unique on session_id", "Confirmed & Verified (02_Sessions)", "Critical", "Must insert row into sessions table"),

        ("EVT-DEF-011", "session_end", "Login & Sessions", "Application backgrounded > 30m or user explicitly exits",
         "Fires when session terminates, recording final duration and exit point", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "session_id, user_id, session_duration_seconds, events_in_session", "exit_feature",
         "String, String, Integer, Integer", "session_duration_seconds >= 0", "duration == session_end - session_start",
         "Client Telemetry SDK", "Measure session length distribution and exit screens", "Avg Session Duration, Abrupt Exit %",
         "Unique on session_id", "Confirmed & Verified (02_Sessions)", "Critical", "Populates sessions.session_duration_seconds"),

        # 4. Task Discovery and Completion
        ("EVT-DEF-012", "task_board_viewed", "Task Lifecycle", "User navigates to tasks/earn tab and views available offers",
         "Fires when task list renders on client screen", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, available_task_count, category_filter", "promoted_task_ids",
         "String, String, Integer, String", "category_filter IN ('All', 'Ad', 'Survey', 'App', 'Game')", "available_task_count >= 0",
         "Backend Task Engine", "Measure task catalog impressions and discovery engagement", "Task Discovery Rate",
         "Deduplicate by session_id + category (1m window)", "Proposed", "High", "Renders offer list sorted by eCPM"),

        ("EVT-DEF-013", "task_started", "Task Lifecycle", "User selects a task and initiates execution",
         "Fires when task activity record is generated and user begins offer", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "activity_id, user_id, task_id, task_category, session_id", "expected_reward_ve",
         "String, String, String, String, String", "task_category IN ('Advertisement', 'App Task', 'Survey', 'CAPTCHA', 'Game')", r"activity_id must be unique ^ACT\d{7}$",
         "Backend Task Service", "Measure task start volume and category popularity", "Tasks Started, Start Velocity",
         "Unique on activity_id", "Confirmed & Verified (05_Task_Activity)", "Critical", "Writes pending row to task_activity"),

        ("EVT-DEF-014", "task_completed", "Task Lifecycle", "User finishes task actions and client/partner reports completion",
         "Fires when task actions are submitted for validation", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "activity_id, user_id, task_id, task_category, duration_seconds", "partner_postback_id",
         "String, String, String, String, Integer", "duration_seconds >= min_task_duration", "task_started_at <= task_completed_at",
         "Backend / Partner Postback", "Core measure of successful task execution", "Task Completion Rate (TCR)",
         "Unique on activity_id", "Confirmed & Verified (05_Task_Activity)", "Critical", "Sets task_status = 'Completed'"),

        ("EVT-DEF-015", "task_validation_failed", "Task Lifecycle", "Task verification fails due to unmet criteria or timeout",
         "Fires when automated validation rules reject task completion proof", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "activity_id, user_id, task_id, failure_reason", "error_code, partner_message",
         "String, String, String, String", "failure_reason IN ('Validation failed', 'Task unavailable', 'Timeout', 'Incomplete action', 'User exited')", "failure_reason must be non-null",
         "Backend Validation Engine", "Diagnose partner SDK errors and user friction", "Task Failure Rate (TFR)",
         "Unique on activity_id", "Confirmed & Verified (05_Task_Activity)", "Critical", "Sets task_status = 'Failed' and logs reason"),

        # 5. Reward Lifecycle
        ("EVT-DEF-016", "reward_pending", "Reward Lifecycle", "Completed task validated; reward placed into escrow holding",
         "Fires when reward transaction enters pending verification queue", "Required", "Required", "Required (reward_tx_id)",
         "ISO 8601 UTC timestamp", "reward_transaction_id, activity_id, user_id, currency_type, reward_amount", "escrow_hold_hours",
         "String, String, String, String, Decimal", "currency_type IN ('VE', 'XP', 'GEM', 'TOKEN', 'SPIN')", "reward_amount > 0.0000",
         "Ledger Engine", "Track unvested reward liabilities and escrow velocity", "Pending Reward Volume ($)",
         "Unique on reward_transaction_id", "Confirmed (reward_status in Tasks)", "Critical", "Appends row to rewards_ledger with status PENDING"),

        ("EVT-DEF-017", "reward_credited", "Reward Lifecycle", "Escrow cleared; reward balance added to spendable user wallet",
         "Fires when currency balance is credited to user account", "Required", "Required", "Required (reward_tx_id)",
         "ISO 8601 UTC timestamp", "reward_transaction_id, user_id, currency_type, reward_amount, balance_after", "idempotency_hash",
         "String, String, String, Decimal, Decimal", "balance_after >= reward_amount", "idempotency_hash must be unique",
         "Ledger Engine", "Recognize realized user earnings and financial liabilities", "Reward Credited Rate, Net Currency Inflow",
         "Unique on reward_transaction_id", "Confirmed (reward_status in Tasks)", "Critical", "Increments wallet balance and logs WLT credit"),

        ("EVT-DEF-018", "reward_reversed", "Reward Lifecycle", "Advertiser chargeback or fraud reverses previously credited reward",
         "Fires when an accounting clawback debits user balance", "Required", "Optional", "Required (reward_tx_id)",
         "ISO 8601 UTC timestamp", "reward_transaction_id, user_id, currency_type, amount_debited, reversal_reason", "original_credit_date",
         "String, String, String, Decimal, String", "reversal_reason IN ('Chargeback', 'Proxy_Fraud', 'Emulator', 'Duplicate_Credit')", "amount_debited > 0",
         "Risk Review / Admin", "Track partner revenue clawbacks and fraud losses", "Reward Reversal Rate (RRR_rev)",
         "Unique on reversal event", "Proposed (GAP-003)", "Critical", "Posts DEBIT_REVERSAL to wallet_transactions"),

        # 6. Daily Rewards and Streaks
        ("EVT-DEF-019", "daily_reward_viewed", "Daily Rewards & Streaks", "User opens daily reward calendar screen",
         "Fires when daily calendar modal is displayed", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, current_calendar_day, is_claimable", "streak_bonus_multiplier",
         "String, String, Integer, Boolean", "current_calendar_day BETWEEN 1 AND 30", "calendar_day valid integer",
         "Client Telemetry SDK", "Evaluate daily reward visibility and calendar discovery", "Daily Reward Discovery Rate",
         "Deduplicate by session_id (1m window)", "Confirmed & Verified (03_Feature_Events)", "High", "Renders active day prize slot"),

        ("EVT-DEF-020", "daily_reward_claimed", "Daily Rewards & Streaks", "User taps 'Claim' button and collects daily calendar prize",
         "Fires when daily reward is validated and awarded", "Required", "Required", "Required (WLT tx)",
         "ISO 8601 UTC timestamp", "user_id, session_id, day_number, prize_currency, prize_amount", "next_claim_available_at",
         "String, String, Integer, String, Decimal", "prize_currency IN ('GEM', 'SPIN', 'XP', 'VE')", "Enforces 24-hour cooldown lock",
         "Backend Gamification", "Core daily retention habit metric", "Daily Reward Claim Rate (DRCR)",
         "Unique per user_id + calendar date", "Confirmed & Verified (03_Feature_Events)", "Critical", "Locks claim button for 24 hours"),

        ("EVT-DEF-021", "streak_claimed", "Daily Rewards & Streaks", "User maintains consecutive login streak and claims milestone bonus",
         "Fires when consecutive day streak milestone is recognized", "Required", "Required", "Required (WLT tx)",
         "ISO 8601 UTC timestamp", "user_id, session_id, streak_day_count, multiplier_applied", "reward_tokens",
         "String, String, Integer, Float", "streak_day_count >= 2", "streak count increments by 1",
         "Backend Gamification", "Measure habit loop strength and retention multipliers", "Streak Continuation Rate",
         "Unique per user_id + streak_count", "Confirmed & Verified (03_Feature_Events)", "High", "Calculates streak bonus payout"),

        ("EVT-DEF-022", "streak_broken", "Daily Rewards & Streaks", "User fails to log in within 36 hours; streak resets to 0",
         "Fires when streak expiration timer evaluates and resets counter", "Required", "Optional (Cron)", "N/A",
         "ISO 8601 UTC timestamp", "user_id, previous_streak_count, days_inactive", "was_recovery_offered",
         "String, Integer, Integer", "previous_streak_count >= 2", "resets active streak to 0",
         "Backend Cron Worker", "Measure churn risk and evaluate demand for streak freeze", "Streak Broken to Churn %",
         "Unique per broken streak instance", "Confirmed & Verified (03_Feature_Events)", "High", "Dispatches win-back push notification"),

        # 7. Missions and Badges
        ("EVT-DEF-023", "mission_completed", "Missions & Badges", "User completes all required quest criteria for a daily mission",
         "Fires when mission objectives evaluate to 100% complete", "Required", "Required", "Required (WLT tx)",
         "ISO 8601 UTC timestamp", "user_id, session_id, mission_id, xp_awarded, bonus_tokens", "completion_duration_minutes",
         "String, String, String, Integer, Decimal", "xp_awarded > 0", "all sub-task criteria verified",
         "Backend Gamification", "Measure quest completion velocity and engagement depth", "Mission Completion Rate",
         "Unique per user_id + mission_id + date", "Confirmed & Verified (03_Feature_Events)", "High", "Marks quest complete in UI"),

        ("EVT-DEF-024", "badge_earned", "Missions & Badges", "User achieves a permanent milestone achievement badge",
         "Fires when an achievement criterion is satisfied for the first time", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, badge_id, badge_category", "xp_bonus_awarded",
         "String, String, String, String", "badge_category IN ('EARNING', 'STREAK', 'REFERRAL', 'COMMUNITY')", "unique per user per badge",
         "Backend Gamification", "Recognize user status progression and completionist drive", "Badge Acquisition Depth",
         "Unique per user_id + badge_id", "Confirmed & Verified (03_Feature_Events)", "Medium", "Assigns badge flair to user profile"),

        ("EVT-DEF-025", "level_up", "Missions & Badges", "Accumulated XP crosses new level progression threshold",
         "Fires when user advances to next platform status tier", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, previous_level, new_level, total_xp", "multiplier_unlocked",
         "String, String, Integer, Integer, Integer", "new_level == previous_level + 1", "total_xp >= level_threshold(new_level)",
         "Backend XP Engine", "Track user tenure progression and long-term stickiness", "Level Progression Velocity",
         "Unique per user_id + new_level", "Confirmed & Verified (03_Feature_Events)", "High", "Unlocks higher reward multipliers"),

        # 8. Wallet Transactions
        ("EVT-DEF-026", "wallet_viewed", "Wallet & Ledger", "User navigates to wallet screen to inspect balances and history",
         "Fires when wallet dashboard renders balance snapshots", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, ve_balance, xp_balance, token_balance", "pending_escrow_tokens",
         "String, String, Decimal, Integer, Decimal", "all balance numbers >= 0", "session_id active",
         "Mobile Client SDK", "Evaluate balance checking frequency prior to cashout", "Wallet Check Frequency",
         "Deduplicate by session_id (1m window)", "Confirmed & Verified (03_Feature_Events)", "High", "Queries real-time balance cache"),

        ("EVT-DEF-027", "wallet_transaction_created", "Wallet & Ledger", "System posts an immutable debit or credit ledger entry",
         "Fires when double-entry transaction commits to wallet_transactions", "Required", "Optional", "Required (tx_id)",
         "ISO 8601 UTC timestamp", "transaction_id, user_id, currency, transaction_type, amount, direction, balance_after", "reference_id, idempotency_key",
         "String, String, String, String, Decimal, String, Decimal", "direction IN ('CREDIT', 'DEBIT')", "balance_after == balance_before +/- amount",
         "Ledger Microservice", "Immutable audit trail of all platform currency mutations", "Total Currency Liability, Velocity of Money",
         "Unique on transaction_id", "Proposed (GAP-001)", "Critical", "Enforces non-negative balance constraint"),

        ("EVT-DEF-028", "currency_exchanged", "Wallet & Ledger", "User converts VEs or Gems into redeemable Tokens",
         "Fires when atomic currency exchange conversion settles", "Required", "Required", "Required (tx_id)",
         "ISO 8601 UTC timestamp", "exchange_id, user_id, from_currency, to_currency, from_amount, to_amount", "exchange_rate_applied, fee_amount",
         "String, String, String, String, Decimal, Decimal", "from_currency != to_currency", "atomic debit and credit commit together",
         "Exchange Engine", "Measure currency conversion volume and platform spread margins", "Exchange Conversion Volume ($)",
         "Unique on exchange_id", "Proposed (GAP-006)", "Critical", "Burns source units and mints target tokens"),

        # 9. Withdrawals
        ("EVT-DEF-029", "withdrawal_requested", "Withdrawal Pipeline", "User submits cashout request specifying payout destination",
         "Fires when withdrawal request passes initial balance and minimum checks", "Required", "Required", "Required (wdr_id)",
         "ISO 8601 UTC timestamp", "withdrawal_id, user_id, amount_tokens, amount_fiat, payout_method", "payout_destination_masked",
         "String, String, Decimal, Decimal, String", "amount_tokens >= min_threshold", "user status == Active_Onboarded",
         "Withdrawal Service", "Track gross withdrawal demand and cash outflow pipeline", "Withdrawal Request Volume, Cashout Demand",
         "Unique on withdrawal_id", "Proposed (GAP-002)", "Critical", "Locks tokens in escrow and writes REQUESTED row"),

        ("EVT-DEF-030", "withdrawal_processing", "Withdrawal Pipeline", "Payout request passes automated risk checks and queues for gateway",
         "Fires when payout batch instruction is transmitted to payment rail", "Required", "Optional", "Required (wdr_id)",
         "ISO 8601 UTC timestamp", "withdrawal_id, user_id, gateway_provider, fraud_risk_score", "batch_id",
         "String, String, String, Float", "gateway IN ('Cashfree', 'Razorpay', 'PayPal', 'Binance')", "risk_score < 75.0",
         "Payout Dispatcher", "Measure risk screening velocity and gateway queue latency", "Gateway Transmit Latency",
         "Unique on withdrawal_id", "Proposed (GAP-002)", "High", "Sets withdrawal_status = 'PROCESSING'"),

        ("EVT-DEF-031", "withdrawal_completed", "Withdrawal Pipeline", "Payment gateway callback confirms successful settlement into bank/wallet",
         "Fires when funds are successfully delivered to user", "Required", "Optional", "Required (wdr_id)",
         "ISO 8601 UTC timestamp", "withdrawal_id, user_id, gateway_ref_id, gateway_fee_amount, settled_amount_fiat", "latency_seconds",
         "String, String, String, Decimal, Decimal", "settled_amount > 0", "gateway_ref_id non-null",
         "Payment Gateway Webhook", "Ultimate user value delivery metric; platform fulfillment health", "Withdrawal Fulfillment Rate (WFR), Avg Processing SLA",
         "Unique on withdrawal_id", "Proposed (GAP-002)", "Critical", "Sets status = 'COMPLETED'; permanently burns tokens"),

        ("EVT-DEF-032", "withdrawal_rejected", "Withdrawal Pipeline", "Payout rejected due to invalid destination, KYC failure, or bot risk",
         "Fires when payout is blocked and escrow funds refund to user", "Required", "Optional", "Required (wdr_id)",
         "ISO 8601 UTC timestamp", "withdrawal_id, user_id, rejection_code, failure_reason", "refund_tx_id",
         "String, String, String, String", "rejection_code IN ('REJ_INVALID_DESTINATION', 'REJ_KYC', 'REJ_FRAUD')", "rejection_code non-null",
         "Risk / Gateway Webhook", "Diagnose cashout friction, bank bounce rates, and fraud blocks", "Withdrawal Rejection Rate (WRR)",
         "Unique on withdrawal_id", "Proposed (GAP-002)", "Critical", "Refunds locked tokens via CREDIT_WITHDRAWAL_REFUND"),

        # 10. Referrals
        ("EVT-DEF-033", "referral_created", "Referrals & Virality", "User generates or views their unique invite code",
         "Fires when referral dashboard initializes unique invite assets", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, referral_code, session_id", "None",
         "String, String, String", "referral_code alphanumeric", "user account active",
         "Referral Service", "Track referral program awareness and invite code generation", "Referral Creation Rate",
         "Deduplicate by session_id", "Confirmed & Verified (03_Feature_Events)", "High", "Returns user unique referral URL"),

        ("EVT-DEF-034", "referral_shared", "Referrals & Virality", "User taps share button to distribute invite via external app",
         "Fires when share sheet or copy-link action is triggered", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, referral_code, share_channel, session_id", "None",
         "String, String, String, String", "share_channel IN ('WhatsApp', 'Telegram', 'Social', 'Copy_Link')", "share_channel valid enum",
         "Mobile Client SDK", "Identify most popular social distribution channels", "Invites Sent per User (i)",
         "Rate limit: max 50 shares/day", "Confirmed & Verified (03_Feature_Events)", "High", "Launches OS native share modal"),

        ("EVT-DEF-035", "referral_registered", "Referrals & Virality", "New referee signs up using an attributed referral code",
         "Fires when referral link between referrer and referee is created", "Required", "Optional", "N/A",
         "ISO 8601 UTC timestamp", "referee_user_id, referrer_user_id, referral_code, device_hash", "utm_source",
         "String, String, String, String", "referee_user_id != referrer_user_id", "asserts device not previously registered",
         "Backend User Service", "Measure viral invite conversion and top referrer acquisition", "Referral Conversion Rate, Viral K-Factor",
         "Unique per referee_user_id", "Proposed (GAP-004)", "Critical", "Inserts row into referral_relationships"),

        ("EVT-DEF-036", "referral_reward_credited", "Referrals & Virality", "Referee qualifies; bonus tokens credited to referrer and referee",
         "Fires when referral commission successfully posts to ledger", "Required", "Optional", "Required (reward_tx_id)",
         "ISO 8601 UTC timestamp", "referral_id, reward_transaction_id, referrer_user_id, referee_user_id, token_amount", "qualification_task_id",
         "String, String, String, String, Decimal", "token_amount > 0", "both accounts active; anti-fraud score < 75.0",
         "Ledger Engine", "Track viral acquisition payout cost and program ROI", "Effective Cost Per Referral (eCPR)",
         "Unique on referral_id + 'PAYOUT'", "Proposed (GAP-004)", "Critical", "Credits +200 Tokens to Referrer, +50 to Referee"),

        # 11. Feature Engagement
        ("EVT-DEF-037", "ad_started", "Feature Engagement", "Rewarded video ad playback begins on client",
         "Fires when video stream starts playing", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, ad_unit_id, network_provider", "ad_format",
         "String, String, String, String", "network IN ('AdMob', 'Unity', 'AppLovin')", "ad_unit_id valid string",
         "Ad Network SDK", "Track ad request volume and initial video impressions", "Ad Requests Started",
         "Unique per ad view attempt", "Confirmed & Verified (03_Feature_Events)", "High", "Initializes 30s playback countdown"),

        ("EVT-DEF-038", "ad_completed", "Feature Engagement", "User watches full 30s rewarded video without skipping",
         "Fires upon successful playback completion callback", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, ad_unit_id, duration_seconds", "estimated_ecpm",
         "String, String, String, Integer", "duration_seconds >= 30", "must have matching ad_started event",
         "Ad Network SDK", "Primary monetizable ad impression event", "Ad Completion Rate (33.7% in data)",
         "Unique per completed view", "Confirmed & Verified (03_Feature_Events)", "Critical", "Triggers reward allocation of VEs/Gems"),

        ("EVT-DEF-039", "tap_completed", "Feature Engagement", "User finishes active tap session in Tap & Earn feature",
         "Fires when micro-earning tapping session closes and credits points", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, tap_count, duration_seconds, earned_ve", "max_taps_per_second",
         "String, String, Integer, Integer, Decimal", "max_taps_per_second < 15.0", "earned_ve == tap_count * multiplier",
         "Mobile Client & API", "Measure casual game engagement and enforce bot auto-clicker limits", "Tap Volume, Micro-Earning Yield",
         "Unique on tap session", "Confirmed & Verified (03_Feature_Events)", "Medium", "Enforces tap cooldown timer"),

        ("EVT-DEF-040", "captcha_completed", "Feature Engagement", "User successfully solves security verification challenge",
         "Fires when challenge verification passes human scoring threshold", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, challenge_type, solve_duration_seconds", "attempt_count",
         "String, String, String, Float", "solve_duration_seconds >= 1.5", "scoring algorithm grants pass",
         "Security Engine", "Validate human traffic on sensitive earning and cashout actions", "CAPTCHA Pass Rate (67.7% in data)",
         "Unique on challenge instance", "Confirmed & Verified (03_Feature_Events)", "Critical", "Unblocks pending cashout or task action"),

        # 12. Help and Support Interactions
        ("EVT-DEF-041", "help_center_viewed", "Help & Support", "User opens FAQ or knowledgebase troubleshooting directory",
         "Fires when help center dashboard renders", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "user_id, session_id, entry_source, initial_category_viewed", "search_query",
         "String, String, String, String", "entry_source IN ('Settings', 'Withdrawal_Error', 'Task_Failed', 'Direct')", "session_id active",
         "Client Telemetry SDK", "Measure self-service help discovery and product confusion points", "Help Center Contact Rate",
         "Deduplicate by session_id (1m window)", "Confirmed (entry_point in Sessions)", "Medium", "Renders support article search"),

        ("EVT-DEF-042", "support_ticket_created", "Help & Support", "User submits customer support inquiry ticket",
         "Fires when ticket is committed to helpdesk CRM (Zendesk/Freshdesk)", "Required", "Required", "N/A",
         "ISO 8601 UTC timestamp", "ticket_id, user_id, session_id, issue_category, priority", "attachment_count",
         "String, String, String, String, String", "issue_category IN ('Withdrawal_Delay', 'Missing_Reward', 'Bug', 'Account_Ban')", "ticket_id valid string",
         "Helpdesk Webhook", "Quantify operational customer friction and partner dispute volume", "Support Ticket Volume Per 1K DAU",
         "Unique on ticket_id", "Proposed (GAP-014)", "High", "Routes ticket to support agent queue"),
    ]
    
    for row in events:
        ws1.append(row)
        
    # ----------------------------------------------------
    # Sheet 2: Verified_vs_Proposed_Summary
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="Verified_vs_Proposed_Summary")
    headers2 = ["Product_Area", "Verified_Events_Count", "Proposed_Events_Count", "Total_Events_Count", "Key_Verified_Events", "Key_Proposed_Events"]
    ws2.append(headers2)
    summary_data = [
        ("User and Account", 0, 3, 3, "None (Only profile attributes in Users)", "user_registered, user_profile_updated, user_account_deleted"),
        ("Registration & Onboarding", 0, 4, 4, "None (Only onboarding_status in Users)", "registration_started, onboarding_step_viewed, onboarding_completed, onboarding_skipped"),
        ("Login and Sessions", 2, 2, 4, "session_start, session_end (02_Sessions)", "user_logged_in, user_login_failed"),
        ("Task Discovery & Completion", 3, 1, 4, "task_started, task_completed, task_validation_failed (05_Task_Activity)", "task_board_viewed"),
        ("Reward Lifecycle", 0, 3, 3, "None (reward_status coupled to tasks)", "reward_pending, reward_credited, reward_reversed"),
        ("Daily Rewards & Streaks", 3, 1, 4, "daily_reward_claimed, streak_claimed, streak_broken (03_Events)", "daily_reward_viewed"),
        ("Missions and Badges", 3, 0, 3, "mission_completed, badge_earned, level_up (03_Events)", "All core gamification events verified"),
        ("Wallet Transactions", 1, 2, 3, "wallet_viewed (03_Events - View only)", "wallet_transaction_created, currency_exchanged"),
        ("Withdrawals", 0, 4, 4, "None (Withdrawal dataset missing from pack)", "withdrawal_requested, withdrawal_processing, withdrawal_completed, withdrawal_rejected"),
        ("Referrals & Virality", 2, 2, 4, "referral_created, referral_shared (03_Events)", "referral_registered, referral_reward_credited"),
        ("Feature Engagement", 4, 0, 4, "ad_started, ad_completed, tap_completed, captcha_completed", "All core feature actions verified in 03_Events"),
        ("Help and Support", 1, 1, 2, "help_center_viewed (entry_point in Sessions)", "support_ticket_created"),
    ]
    for row in summary_data:
        ws2.append(row)
        
    # ----------------------------------------------------
    # Sheet 3: Event_Naming_Standards
    # ----------------------------------------------------
    ws3 = wb.create_sheet(title="Event_Naming_Standards")
    headers3 = ["Standard_Rule_ID", "Rule_Category", "Standard_Convention", "Correct_Example", "Incorrect_Example", "Enforcement_Rationale"]
    ws3.append(headers3)
    standards = [
        ("STD-EVT-01", "Casing Convention", "Strictly lower_snake_case with no uppercase characters or spaces", "task_completed, ad_started", "TaskCompleted, Task-Completed, Task Completed", "Ensures cross-platform JSON parser compatibility and database column mapping"),
        ("STD-EVT-02", "Grammar Structure", "Object (Noun) followed by Past-Tense Verb (or Action)", "user_registered, withdrawal_requested", "registered_user, request_withdrawal", "Groups all events for a specific domain alphabetically in data catalogs"),
        ("STD-EVT-03", "Temporal Consistency", "Verb tense must represent completed actions (past tense) unless explicitly initiating a state", "ad_completed, streak_claimed", "ad_completing, streak_claim", "Events represent historical facts that have already occurred"),
        ("STD-EVT-04", "Mandatory Envelope Keys", "Every event JSON payload must contain event_id, event_name, timestamp_utc, user_id, session_id", "{\"event_id\":\"EVT001\", \"timestamp_utc\":\"2026-11-01T...\"}", "{\"name\":\"ad\", \"time\":\"12:00\"}", "Guarantees referential integrity and standard ELT ingestion schema"),
        ("STD-EVT-05", "Timestamp Standard", "All event timestamps must be ISO 8601 UTC format with explicit 'Z' designator", "2026-11-24T10:30:00Z", "24/11/2026 10:30 AM, 1732444200", "Prevents timezone ambiguity across multi-regional users"),
        ("STD-EVT-06", "Currency Decimals", "Virtual currencies formatted as string or fixed decimal; never raw floating point", "\"amount\": 150.0000", "\"amount\": 150.00000000000003", "Avoids binary floating-point rounding errors in financial reconciliations"),
    ]
    for row in standards:
        ws3.append(row)
        
    doc_path = base_dir / "documentation" / "Event_Tracking_Plan.xlsx"
    root_path = base_dir / "Event_Tracking_Plan.xlsx"
    save_styled_workbook(wb, doc_path)
    wb.save(root_path)
    print(f"Saved: {root_path}")

if __name__ == "__main__":
    print("Generating Phase 2 Deliverable: Event_Tracking_Plan.xlsx...")
    create_event_tracking_plan()
    print("Event_Tracking_Plan.xlsx created successfully!")
