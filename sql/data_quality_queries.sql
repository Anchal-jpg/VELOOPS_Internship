-- =============================================================================
-- VELOOP Product Analytics - Data Quality & Integrity Assertion Queries
-- Author: Senior Data Analyst & Engineering Mentor Team
-- Project: VELOOP Rewards Data Analyst Internship (Task 01)
-- Scope: Days 1-10 Foundation
-- Rule: Queries return violation rows. An empty result set (0 rows) indicates PASS.
-- =============================================================================

-- =============================================================================
-- TEST 1: Primary Key Uniqueness & Nullability on Users Entity
-- Objective: Ensure user_id has zero nulls and zero duplicates.
-- Expected Result: 0 rows returned on clean data; returns 8 rows on Users_Messy_Audit.
-- =============================================================================
SELECT 
    user_id,
    COUNT(*) AS occurrence_count
FROM users
GROUP BY user_id
HAVING COUNT(*) > 1 OR user_id IS NULL;


-- =============================================================================
-- TEST 2: Primary Key Uniqueness on Sessions Entity
-- Objective: Assert session_id is globally unique across all 7,913 recorded sessions.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    session_id,
    COUNT(*) AS occurrence_count
FROM sessions
GROUP BY session_id
HAVING COUNT(*) > 1 OR session_id IS NULL;


-- =============================================================================
-- TEST 3: Primary Key Uniqueness on Feature Events
-- Objective: Assert event_id is globally unique across 35,704 events.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    event_id,
    COUNT(*) AS occurrence_count
FROM feature_events
GROUP BY event_id
HAVING COUNT(*) > 1 OR event_id IS NULL;


-- =============================================================================
-- TEST 4: Primary Key Uniqueness on Task Activity
-- Objective: Assert activity_id is globally unique across 9,846 task activities.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    activity_id,
    COUNT(*) AS occurrence_count
FROM task_activity
GROUP BY activity_id
HAVING COUNT(*) > 1 OR activity_id IS NULL;


-- =============================================================================
-- TEST 5: Foreign Key Referential Integrity - Orphan Sessions in Feature Events
-- Objective: Ensure every event in feature_events belongs to a valid session in sessions.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    fe.event_id,
    fe.session_id,
    fe.event_datetime,
    fe.feature_name
FROM feature_events fe
LEFT JOIN sessions s ON fe.session_id = s.session_id
WHERE s.session_id IS NULL;


-- =============================================================================
-- TEST 6: Foreign Key Referential Integrity - Orphan Users Across Child Tables
-- Objective: Ensure all user_ids in sessions and tasks exist in the parent users table.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 'sessions' AS source_table, s.session_id AS record_id, s.user_id
FROM sessions s
LEFT JOIN users u ON s.user_id = u.user_id
WHERE u.user_id IS NULL

UNION ALL

SELECT 'task_activity' AS source_table, t.activity_id AS record_id, t.user_id
FROM task_activity t
LEFT JOIN users u ON t.user_id = u.user_id
WHERE u.user_id IS NULL;


-- =============================================================================
-- TEST 7: Milestone Session Integrity (Isolating the 40 Null Session Anomalies)
-- Objective: Identify milestone records missing a session_id.
-- Expected Result: Exactly 40 rows returned (Documented architectural finding).
-- =============================================================================
SELECT 
    m.milestone_id,
    m.user_id,
    m.milestone_type,
    m.milestone_datetime,
    m.source_event,
    m.session_id
FROM milestones m
WHERE m.session_id IS NULL;


-- =============================================================================
-- TEST 8: Temporal Chronology - Registration vs Last Login
-- Objective: Assert registration_datetime <= last_login_datetime.
-- Expected Result: 0 rows returned on clean data.
-- =============================================================================
SELECT 
    user_id,
    registration_datetime,
    last_login_datetime,
    (last_login_datetime - registration_datetime) AS delta
FROM users
WHERE last_login_datetime IS NOT NULL 
  AND registration_datetime > last_login_datetime;


-- =============================================================================
-- TEST 9: Session Duration Consistency
-- Objective: Assert recorded session_duration_seconds matches end - start.
-- Expected Result: 0 rows returned (allows 2 second buffer for clock skew).
-- =============================================================================
SELECT 
    session_id,
    session_start,
    session_end,
    session_duration_seconds,
    EXTRACT(EPOCH FROM (session_end - session_start)) AS calculated_seconds,
    ABS(session_duration_seconds - EXTRACT(EPOCH FROM (session_end - session_start))) AS discrepancy
FROM sessions
WHERE ABS(session_duration_seconds - EXTRACT(EPOCH FROM (session_end - session_start))) > 2;


-- =============================================================================
-- TEST 10: Task Completed Consistency
-- Objective: Assert that all Completed tasks have a non-null task_completed_at
--            and reward_status = 'Credited'.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    activity_id,
    user_id,
    task_id,
    task_status,
    task_completed_at,
    reward_status
FROM task_activity
WHERE task_status = 'Completed' 
  AND (task_completed_at IS NULL OR reward_status <> 'Credited');


-- =============================================================================
-- TEST 11: Task Failure Consistency
-- Objective: Assert that all Failed tasks have an explicit failure_reason.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    activity_id,
    user_id,
    task_id,
    task_status,
    failure_reason
FROM task_activity
WHERE task_status = 'Failed' 
  AND (failure_reason IS NULL OR TRIM(failure_reason) = '');


-- =============================================================================
-- TEST 12: XP Balance Non-Negativity
-- Objective: Assert xp_balance >= 0 across all user profiles.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    user_id,
    xp_balance
FROM users
WHERE xp_balance < 0;


-- =============================================================================
-- TEST 13: User Age Bounds Check
-- Objective: Assert user age falls within legally eligible bounds (13 to 100).
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    user_id,
    age
FROM users
WHERE age < 13 OR age > 100;


-- =============================================================================
-- TEST 14: Feature Event Status Enum Validity
-- Objective: Assert event_status values belong strictly to allowed enum set.
-- Expected Result: 0 rows returned.
-- =============================================================================
SELECT 
    event_id,
    feature_name,
    event_name,
    event_status
FROM feature_events
WHERE event_status NOT IN ('Started', 'Success', 'Abandoned', 'Failed');


-- =============================================================================
-- TEST 15: Injected Audit Pack Anomaly Isolation (Users_Messy_Audit)
-- Objective: Isolate deliberately injected duplicate user records in the messy audit sheet.
-- Expected Result: Exactly 8 duplicate groups returned.
-- =============================================================================
SELECT 
    user_id,
    COUNT(*) AS duplicate_row_count,
    MIN(full_name) AS sample_name,
    COUNT(city) AS non_null_city_count,
    COUNT(age) AS non_null_age_count
FROM users_messy_audit
GROUP BY user_id
HAVING COUNT(*) > 1;

