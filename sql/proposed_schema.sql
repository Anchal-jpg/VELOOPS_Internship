-- =============================================================================
-- VELOOP Product Analytics - Proposed & Verified Database Schemas
-- Author: Senior Data Analyst & Engineering Mentor Team
-- Project: VELOOP Rewards Data Analyst Internship (Task 01)
-- Scope: Days 1-10 Foundation
-- Dialect: ANSI SQL / PostgreSQL / Modern Cloud Data Warehouse Compatible
-- =============================================================================

-- =============================================================================
-- SECTION 1: VERIFIED SOURCE SCHEMAS
-- These schemas represent the empirical structures verified in the provided
-- simulated Excel workbooks (VELoop_Rewards_Data_01.xlsx & VELOOP_Simulated_User_Behavior_1000.xlsx).
-- =============================================================================

-- Table 1.1: Core Users Entity (Verified from Users_1000_Clean)
CREATE TABLE IF NOT EXISTS users (
    user_id                     VARCHAR(11) PRIMARY KEY,     -- Format: VLUSR######
    full_name                   VARCHAR(100) NOT NULL,
    email                       VARCHAR(150) NOT NULL UNIQUE,
    age                         INTEGER NOT NULL CHECK (age >= 13 AND age <= 100),
    gender                      VARCHAR(20) NOT NULL,
    state                       VARCHAR(50) NOT NULL,
    city                        VARCHAR(50),
    registration_datetime       TIMESTAMP NOT NULL,
    acquisition_source          VARCHAR(50) NOT NULL,
    referral_source_detail      VARCHAR(50),
    primary_device              VARCHAR(50) NOT NULL,
    platform                    VARCHAR(20) NOT NULL CHECK (platform IN ('Android', 'iOS', 'Web')),
    account_status              VARCHAR(20) NOT NULL CHECK (account_status IN ('Active', 'Suspended', 'Pending', 'Deactivated')),
    email_verification_status   VARCHAR(20) NOT NULL CHECK (email_verification_status IN ('Verified', 'Unverified')),
    onboarding_status           VARCHAR(20) NOT NULL CHECK (onboarding_status IN ('Completed', 'Incomplete')),
    last_login_datetime         TIMESTAMP,
    lifetime_sessions           INTEGER NOT NULL DEFAULT 0 CHECK (lifetime_sessions >= 0),
    active_days                 INTEGER NOT NULL DEFAULT 0 CHECK (active_days >= 0),
    xp_balance                  INTEGER NOT NULL DEFAULT 0 CHECK (xp_balance >= 0),
    referral_code               VARCHAR(20) NOT NULL UNIQUE,
    days_since_registration     INTEGER NOT NULL DEFAULT 0 CHECK (days_since_registration >= 0),
    is_active_7d                BOOLEAN NOT NULL DEFAULT FALSE,
    is_active_30d               BOOLEAN NOT NULL DEFAULT FALSE,
    consent_status              VARCHAR(20) NOT NULL DEFAULT 'Granted',
    marketing_opt_in            BOOLEAN NOT NULL DEFAULT FALSE,
    account_created_via         VARCHAR(30) NOT NULL DEFAULT 'Direct',
    country                     VARCHAR(10) NOT NULL DEFAULT 'IN',
    CONSTRAINT chk_user_chronology CHECK (last_login_datetime IS NULL OR registration_datetime <= last_login_datetime)
);

-- Table 1.2: User Sessions Entity (Verified from 02_Sessions)
CREATE TABLE IF NOT EXISTS sessions (
    session_id                  VARCHAR(11) PRIMARY KEY,     -- Format: SESS#######
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    session_start               TIMESTAMP NOT NULL,
    session_end                 TIMESTAMP NOT NULL,
    session_duration_seconds    INTEGER NOT NULL CHECK (session_duration_seconds >= 0),
    device                      VARCHAR(50) NOT NULL,
    platform                    VARCHAR(20) NOT NULL,
    entry_point                 VARCHAR(50) NOT NULL,
    exit_feature                VARCHAR(50),                 -- Nullable: 466 nulls (5.89%) observed on abrupt exit
    events_in_session           INTEGER NOT NULL DEFAULT 0 CHECK (events_in_session >= 0),
    features_used_count         INTEGER NOT NULL DEFAULT 0 CHECK (features_used_count >= 0),
    session_status              VARCHAR(20) NOT NULL DEFAULT 'Completed',
    CONSTRAINT chk_session_chronology CHECK (session_start <= session_end)
);

-- Table 1.3: Granular Feature Telemetry Events (Verified from 03_Feature_Events)
CREATE TABLE IF NOT EXISTS feature_events (
    event_id                    VARCHAR(11) PRIMARY KEY,     -- Format: EVT########
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    session_id                  VARCHAR(11) NOT NULL REFERENCES sessions(session_id) ON DELETE RESTRICT,
    event_datetime              TIMESTAMP NOT NULL,
    feature_name                VARCHAR(50) NOT NULL,
    event_name                  VARCHAR(50) NOT NULL,
    event_status                VARCHAR(20) NOT NULL CHECK (event_status IN ('Started', 'Success', 'Abandoned', 'Failed')),
    device                      VARCHAR(50) NOT NULL,
    platform                    VARCHAR(20) NOT NULL,
    acquisition_source          VARCHAR(50) NOT NULL,
    sequence_number             INTEGER NOT NULL CHECK (sequence_number >= 1),
    reward_related_flag         BOOLEAN NOT NULL DEFAULT FALSE,
    xp_related_flag             BOOLEAN NOT NULL DEFAULT FALSE
);

-- Table 1.4: Daily Activity Rollup (Verified from 04_Daily_Activity)
CREATE TABLE IF NOT EXISTS daily_activity (
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    activity_date               DATE NOT NULL,
    session_count               INTEGER NOT NULL DEFAULT 0,
    session_duration_minutes    DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    event_count                 INTEGER NOT NULL DEFAULT 0,
    feature_count               INTEGER NOT NULL DEFAULT 0,
    task_count                  INTEGER NOT NULL DEFAULT 0,
    completed_task_count        INTEGER NOT NULL DEFAULT 0,
    reward_activity_count       INTEGER NOT NULL DEFAULT 0,
    xp_activity_count           INTEGER NOT NULL DEFAULT 0,
    streak_activity             BOOLEAN NOT NULL DEFAULT FALSE,
    daily_reward_claimed        BOOLEAN NOT NULL DEFAULT FALSE,
    mission_activity            BOOLEAN NOT NULL DEFAULT FALSE,
    spin_activity               BOOLEAN NOT NULL DEFAULT FALSE,
    referral_activity           BOOLEAN NOT NULL DEFAULT FALSE,
    wallet_activity             BOOLEAN NOT NULL DEFAULT FALSE,
    active_flag                 BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (user_id, activity_date)
);

-- Table 1.5: Operational Task Activity (Verified from 05_Task_Activity)
CREATE TABLE IF NOT EXISTS task_activity (
    activity_id                 VARCHAR(15) PRIMARY KEY,     -- Format: ACT#######
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    task_id                     VARCHAR(20) NOT NULL,
    task_category               VARCHAR(50) NOT NULL,
    task_viewed_at              TIMESTAMP NOT NULL,
    task_started_at             TIMESTAMP NOT NULL,
    task_completed_at           TIMESTAMP,                   -- Nullable: null when Abandoned/Failed/Pending
    task_status                 VARCHAR(20) NOT NULL CHECK (task_status IN ('Completed', 'Abandoned', 'Failed', 'Pending')),
    failure_reason              VARCHAR(100),                -- Nullable: populated on 'Failed'
    reward_status               VARCHAR(20) NOT NULL CHECK (reward_status IN ('Credited', 'Not Credited', 'Pending')),
    device                      VARCHAR(50) NOT NULL,
    session_id                  VARCHAR(11) NOT NULL REFERENCES sessions(session_id) ON DELETE RESTRICT,
    CONSTRAINT chk_task_timing CHECK (task_viewed_at <= task_started_at AND (task_completed_at IS NULL OR task_started_at <= task_completed_at))
);

-- Table 1.6: User Milestones (Verified from 06_Milestones)
CREATE TABLE IF NOT EXISTS milestones (
    milestone_id                BIGSERIAL PRIMARY KEY,
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    milestone_type              VARCHAR(50) NOT NULL,
    milestone_datetime          TIMESTAMP NOT NULL,
    milestone_value             VARCHAR(50),
    source_event                VARCHAR(50),
    session_id                  VARCHAR(11) REFERENCES sessions(session_id) ON DELETE SET NULL -- 40 nulls observed
);


-- =============================================================================
-- SECTION 2: PROPOSED PRODUCTION SCHEMAS (CLOSING CRITICAL GAPS)
-- These schemas are designed by the analytics and data engineering team to 
-- resolve the critical data deficits identified in GAP-001 through GAP-004.
-- =============================================================================

-- Table 2.1: Decoupled Rewards Financial Ledger (Resolving GAP-003)
-- Decouples operational task logging from financial reward transactions.
CREATE TABLE IF NOT EXISTS rewards_ledger (
    reward_transaction_id       VARCHAR(20) PRIMARY KEY,     -- Format: RWD##########
    activity_id                 VARCHAR(15) REFERENCES task_activity(activity_id) ON DELETE RESTRICT,
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    source_feature              VARCHAR(50) NOT NULL,        -- Watch_Ads, Survey, App_Task, Streak, Mission
    currency_type               VARCHAR(10) NOT NULL CHECK (currency_type IN ('VE', 'XP', 'GEM', 'TOKEN', 'SPIN')),
    reward_amount               DECIMAL(14,4) NOT NULL CHECK (reward_amount > 0.0000),
    transaction_type            VARCHAR(20) NOT NULL CHECK (transaction_type IN ('CREDIT', 'DEBIT_REVERSAL', 'ADJUSTMENT')),
    reward_status               VARCHAR(20) NOT NULL CHECK (reward_status IN ('PENDING', 'CREDITED', 'REVERSED', 'CANCELLED')),
    idempotency_hash            VARCHAR(64) NOT NULL UNIQUE, -- SHA-256 (user_id + activity_id + currency + amount)
    balance_after               DECIMAL(14,4) NOT NULL CHECK (balance_after >= 0.0000),
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    credited_at                 TIMESTAMP,
    reversal_reason             VARCHAR(100)
);

-- Table 2.2: Double-Entry Wallet Transaction Ledger (Resolving GAP-001)
-- Full double-entry balance ledger replacing passive wallet_viewed event.
CREATE TABLE IF NOT EXISTS wallet_transactions (
    transaction_id              VARCHAR(24) PRIMARY KEY,     -- Format: WLT############
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    currency                    VARCHAR(10) NOT NULL CHECK (currency IN ('VE', 'XP', 'GEM', 'TOKEN', 'SPIN')),
    transaction_type            VARCHAR(30) NOT NULL,
    direction                   VARCHAR(6) NOT NULL CHECK (direction IN ('CREDIT', 'DEBIT')),
    amount                      DECIMAL(14,4) NOT NULL CHECK (amount > 0.0000),
    balance_before              DECIMAL(14,4) NOT NULL CHECK (balance_before >= 0.0000),
    balance_after               DECIMAL(14,4) NOT NULL CHECK (balance_after >= 0.0000),
    transaction_status          VARCHAR(20) NOT NULL DEFAULT 'SETTLED' CHECK (transaction_status IN ('PENDING', 'SETTLED', 'LOCKED', 'REVERSED', 'FAILED')),
    source_event_id             VARCHAR(11) REFERENCES feature_events(event_id) ON DELETE SET NULL,
    reference_id                VARCHAR(36),                 -- External activity_id or withdrawal_id
    idempotency_key             VARCHAR(64) NOT NULL UNIQUE,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_wallet_delta CHECK (
        (direction = 'CREDIT' AND balance_after = balance_before + amount) OR
        (direction = 'DEBIT' AND balance_after = balance_before - amount)
    )
);

-- Table 2.3: Production Withdrawal Requests & Payout Pipeline (Resolving GAP-002)
-- 5-stage state machine tracking fiat/crypto cashouts.
CREATE TABLE IF NOT EXISTS withdrawal_requests (
    withdrawal_id               VARCHAR(24) PRIMARY KEY,     -- Format: WDR############
    user_id                     VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    amount_tokens               DECIMAL(12,4) NOT NULL CHECK (amount_tokens > 0.0000),
    amount_fiat                 DECIMAL(10,2) NOT NULL CHECK (amount_fiat > 0.00),
    currency_code               VARCHAR(3) NOT NULL DEFAULT 'INR',
    payout_method               VARCHAR(20) NOT NULL CHECK (payout_method IN ('UPI', 'PAYPAL', 'BANK_TRANSFER', 'CRYPTO_USDT')),
    payout_destination_masked   VARCHAR(100) NOT NULL,       -- Masked VPA / Email / Bank Account
    withdrawal_status           VARCHAR(20) NOT NULL DEFAULT 'REQUESTED' CHECK (withdrawal_status IN ('REQUESTED', 'PROCESSING', 'COMPLETED', 'REJECTED', 'REVERSED')),
    gateway_provider            VARCHAR(30),                 -- Cashfree, Razorpay, PayPal, Binance
    gateway_transaction_ref     VARCHAR(100),
    gateway_fee_amount          DECIMAL(8,2) NOT NULL DEFAULT 0.00 CHECK (gateway_fee_amount >= 0.00),
    rejection_code              VARCHAR(50),
    requested_at                TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at                TIMESTAMP,
    CONSTRAINT chk_wdr_timing CHECK (completed_at IS NULL OR requested_at <= completed_at)
);

-- Table 2.4: Relational Referral Directed Graph (Resolving GAP-004)
-- Directed graph linking referrers to referees with qualification tracking.
CREATE TABLE IF NOT EXISTS referral_relationships (
    referral_id                 BIGSERIAL PRIMARY KEY,
    referrer_user_id            VARCHAR(11) NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    referee_user_id             VARCHAR(11) NOT NULL UNIQUE REFERENCES users(user_id) ON DELETE RESTRICT,
    referral_code_used          VARCHAR(20) NOT NULL,
    attribution_channel         VARCHAR(50) NOT NULL DEFAULT 'In-App Share',
    is_qualified                BOOLEAN NOT NULL DEFAULT FALSE,
    qualification_criteria      VARCHAR(50) DEFAULT 'Complete 1st Task',
    qualified_at                TIMESTAMP,
    referrer_reward_credited    BOOLEAN NOT NULL DEFAULT FALSE,
    reward_transaction_id       VARCHAR(20) REFERENCES rewards_ledger(reward_transaction_id) ON DELETE SET NULL,
    created_at                  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_no_self_referral CHECK (referrer_user_id <> referee_user_id)
);

