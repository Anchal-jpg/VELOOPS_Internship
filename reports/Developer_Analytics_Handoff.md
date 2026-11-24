# VELOOP Rewards — Developer Analytics Implementation Handoff Guide
**Internship Work-Scope Target:** Phase 8 Deliverable  
**Creation Date:** 24 November 2026  
**Document Reference:** `documentation/Developer_Analytics_Handoff.md`  
**Master Specification:** [`Developer_Analytics_Handoff.xlsx`](file:///D:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Developer_Analytics_Handoff.xlsx)

---

## 1. Purpose & Integration Overview

This technical handoff document provides software engineers, frontend developers, and backend API teams with the exact schemas, contract definitions, validation assertions, and QA test protocols required to instrument telemetry across the VELOOP Rewards application.

---

## 2. Global Event Envelope Contract

Every client and server event MUST adhere to the standard JSON envelope:

```json
{
  "event_id": "EVT_UUID_V4",
  "event_name": "task_completed",
  "client_timestamp": "2026-11-24T11:30:00.000Z",
  "server_received_at": "2026-11-24T11:30:00.120Z",
  "user_id": "VLUSR001001",
  "session_id": "SESS0009921",
  "device_telemetry": {
    "platform": "Android",
    "os_version": "14",
    "app_version": "2.4.1",
    "device_model": "Samsung SM-S918B"
  },
  "properties": {
    "task_id": "TSK_SURVEY_01",
    "category": "Surveys",
    "reward_points": 100
  }
}
```

---

## 3. QA Acceptance Criteria & Validation Rules

1. **Idempotency Guarantee:** All financial and transactional events (`wallet_transaction_created`, `withdrawal_requested`) MUST transmit a unique `idempotency_key` in the HTTP header. Retries must not trigger double point allocations.
2. **Offline Queuing:** Mobile clients must buffer telemetry locally in SQLite when offline and flush in sequential order with original `client_timestamp` upon network reconnection.
3. **HTTP Status Codes:** Ingestion API returns `202 Accepted` for valid event streams and `422 Unprocessable Entity` for schema contract violations.
