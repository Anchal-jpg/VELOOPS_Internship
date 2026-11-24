-- =============================================================================
-- VELOOP Product Analytics - Initial Baseline Analytics Queries
-- Author: Senior Data Analyst & Engineering Mentor Team
-- Project: VELOOP Rewards Data Analyst Internship (Task 01)
-- Scope: Days 1-10 Foundation
-- Dialect: Standard SQL / PostgreSQL Compatible
-- =============================================================================

-- =============================================================================
-- QUERY 1: User Cohort Acquisition & Acquisition Channel Mix
-- Business Question: How are registered users distributed across acquisition channels
--                     and what is their email verification / onboarding rate?
-- =============================================================================
SELECT 
    acquisition_source,
    COUNT(*) AS total_signups,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS channel_share_pct,
    SUM(CASE WHEN email_verification_status = 'Verified' THEN 1 ELSE 0 END) AS verified_users,
    ROUND(SUM(CASE WHEN email_verification_status = 'Verified' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS verification_rate_pct,
    SUM(CASE WHEN onboarding_status = 'Completed' THEN 1 ELSE 0 END) AS onboarded_users,
    ROUND(SUM(CASE WHEN onboarding_status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS onboarding_completion_pct,
    ROUND(AVG(xp_balance), 1) AS avg_xp_balance
FROM users
GROUP BY acquisition_source
ORDER BY total_signups DESC;


-- =============================================================================
-- QUERY 2: User Activity & Stickiness Index (DAU / MAU)
-- Business Question: What is the overall active ratio of our simulated user base?
-- =============================================================================
SELECT 
    COUNT(*) AS total_registered_users,
    SUM(CASE WHEN is_active_7d = TRUE THEN 1 ELSE 0 END) AS wau_count,
    ROUND(SUM(CASE WHEN is_active_7d = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS wau_pct,
    SUM(CASE WHEN is_active_30d = TRUE THEN 1 ELSE 0 END) AS mau_count,
    ROUND(SUM(CASE WHEN is_active_30d = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS mau_pct,
    SUM(CASE WHEN last_login_datetime IS NULL THEN 1 ELSE 0 END) AS d0_dormant_users,
    ROUND(SUM(CASE WHEN last_login_datetime IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS d0_dormant_pct
FROM users;


-- =============================================================================
-- QUERY 3: Task Conversion Funnel by Task Category
-- Business Question: What is the completion, abandonment, and failure rate across
--                     the 8 distinct task categories?
-- =============================================================================
SELECT 
    task_category,
    COUNT(*) AS total_tasks_started,
    SUM(CASE WHEN task_status = 'Completed' THEN 1 ELSE 0 END) AS completed_count,
    ROUND(SUM(CASE WHEN task_status = 'Completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS completion_rate_pct,
    SUM(CASE WHEN task_status = 'Abandoned' THEN 1 ELSE 0 END) AS abandoned_count,
    ROUND(SUM(CASE WHEN task_status = 'Abandoned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS abandonment_rate_pct,
    SUM(CASE WHEN task_status = 'Failed' THEN 1 ELSE 0 END) AS failed_count,
    ROUND(SUM(CASE WHEN task_status = 'Failed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS failure_rate_pct,
    SUM(CASE WHEN task_status = 'Pending' THEN 1 ELSE 0 END) AS pending_count
FROM task_activity
GROUP BY task_category
ORDER BY total_tasks_started DESC;


-- =============================================================================
-- QUERY 4: Failure Reason Distribution Across Task Categories
-- Business Question: Why do tasks fail, and are certain categories vulnerable to timeouts?
-- =============================================================================
SELECT 
    task_category,
    failure_reason,
    COUNT(*) AS failure_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY task_category), 2) AS pct_of_category_failures
FROM task_activity
WHERE task_status = 'Failed'
GROUP BY task_category, failure_reason
ORDER BY task_category, failure_count DESC;


-- =============================================================================
-- QUERY 5: Session Engagement & Navigation Depth Analysis
-- Business Question: What is average session duration, event density, and where do
--                     users exit the application?
-- =============================================================================
SELECT 
    platform,
    device,
    COUNT(*) AS total_sessions,
    ROUND(AVG(session_duration_seconds), 1) AS avg_duration_sec,
    ROUND(AVG(events_in_session), 1) AS avg_events_per_session,
    ROUND(AVG(features_used_count), 1) AS avg_features_per_session,
    SUM(CASE WHEN exit_feature IS NULL THEN 1 ELSE 0 END) AS abrupt_exits_null_count,
    ROUND(SUM(CASE WHEN exit_feature IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS abrupt_exit_pct
FROM sessions
GROUP BY platform, device
ORDER BY total_sessions DESC;


-- =============================================================================
-- QUERY 6: Feature Telemetry Adoption & Success Velocity Ranking
-- Business Question: Which features generate the highest event volume and success rates?
-- =============================================================================
SELECT 
    feature_name,
    COUNT(*) AS total_events,
    COUNT(DISTINCT user_id) AS unique_active_users,
    COUNT(DISTINCT session_id) AS unique_sessions,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT user_id), 2) AS events_per_user,
    SUM(CASE WHEN event_status = 'Success' THEN 1 ELSE 0 END) AS success_events,
    ROUND(SUM(CASE WHEN event_status = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS success_rate_pct,
    SUM(CASE WHEN event_status = 'Failed' THEN 1 ELSE 0 END) AS failed_events
FROM feature_events
GROUP BY feature_name
ORDER BY total_events DESC;


-- =============================================================================
-- QUERY 7: CAPTCHA Bot Defense Performance by Platform
-- Business Question: What proportion of verification challenges fail, indicating bot threat?
-- =============================================================================
SELECT 
    platform,
    COUNT(*) AS total_captcha_events,
    SUM(CASE WHEN event_name = 'captcha_started' THEN 1 ELSE 0 END) AS challenges_started,
    SUM(CASE WHEN event_name = 'captcha_completed' THEN 1 ELSE 0 END) AS challenges_passed,
    SUM(CASE WHEN event_name = 'captcha_failed' THEN 1 ELSE 0 END) AS challenges_failed,
    ROUND(
        SUM(CASE WHEN event_name = 'captcha_failed' THEN 1 ELSE 0 END) * 100.0 / 
        NULLIF(SUM(CASE WHEN event_name IN ('captcha_completed', 'captcha_failed') THEN 1 ELSE 0 END), 0),
        2
    ) AS failure_rate_pct
FROM feature_events
WHERE feature_name = 'CAPTCHA'
GROUP BY platform
ORDER BY total_captcha_events DESC;


-- =============================================================================
-- QUERY 8: Milestone Velocity (Time-to-Milestone from Registration)
-- Business Question: How many hours does it take for a registered user to hit key milestones?
-- =============================================================================
SELECT 
    m.milestone_type,
    COUNT(*) AS total_milestones_achieved,
    COUNT(DISTINCT m.user_id) AS distinct_users,
    ROUND(AVG(EXTRACT(EPOCH FROM (m.milestone_datetime - u.registration_datetime)) / 3600.0), 1) AS avg_hours_from_registration,
    ROUND(MIN(EXTRACT(EPOCH FROM (m.milestone_datetime - u.registration_datetime)) / 3600.0), 1) AS min_hours,
    ROUND(MAX(EXTRACT(EPOCH FROM (m.milestone_datetime - u.registration_datetime)) / 3600.0), 1) AS max_hours
FROM milestones m
JOIN users u ON m.user_id = u.user_id
GROUP BY m.milestone_type
ORDER BY total_milestones_achieved DESC;


-- =============================================================================
-- QUERY 9: User XP Accumulation by Age Cohort & Acquisition Source
-- Business Question: Which demographic cohorts accumulate the highest XP progression?
-- =============================================================================
SELECT 
    CASE 
        WHEN age BETWEEN 18 AND 24 THEN '18-24 (Gen Z)'
        WHEN age BETWEEN 25 AND 34 THEN '25-34 (Millennials)'
        WHEN age BETWEEN 35 AND 49 THEN '35-49 (Gen X)'
        ELSE '50+ (Mature)'
    END AS age_cohort,
    acquisition_source,
    COUNT(*) AS user_count,
    ROUND(AVG(xp_balance), 0) AS avg_xp,
    ROUND(AVG(lifetime_sessions), 1) AS avg_lifetime_sessions,
    ROUND(AVG(active_days), 1) AS avg_active_days
FROM users
GROUP BY 1, 2
ORDER BY age_cohort, avg_xp DESC;


-- =============================================================================
-- QUERY 10: Analytical Gap Diagnostics (Documentation of Missing Financial Tables)
-- Business Question: Query demonstrating that financial ledger and withdrawal records
--                     are absent from raw data and must not be fabricated.
-- =============================================================================
SELECT 
    'wallet_viewed_only' AS telemetry_state,
    COUNT(*) AS view_events_count,
    0 AS total_debit_transactions,
    0 AS total_credit_transactions,
    0 AS total_withdrawal_requests,
    'CRITICAL GAP: Financial ledger and withdrawal tables missing from data pack' AS documentation_notice
FROM feature_events
WHERE feature_name = 'Wallet';

