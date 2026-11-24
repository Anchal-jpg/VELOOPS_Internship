# VELOOP Rewards — Enterprise Data Quality Control Framework Report
**Internship Work-Scope Target:** Day 24 (Phase 6 Deliverable)  
**Creation Date:** 24 November 2026  
**Document Reference:** `reports/Data_Quality_Control_Report.md`  
**Master Framework Spreadsheet:** [`Data_Quality_Control_Framework.xlsx`](file:///D:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/reports/Data_Quality_Control_Framework.xlsx)

---

## 1. Executive Summary & Purpose

The **Data Quality Control Framework (DQCF)** establishes the operational architecture, SLA thresholds, automated gatekeeping rules, and incident remediation workflows required to maintain high data reliability across the VELOOP Rewards platform.

Designed around a **5-Layer Defense-in-Depth Architecture**, the framework ensures that data anomalies identified during the Phase 5 audit (duplicate accounts, invalid timestamps, missing profile fields) are intercepted and quarantined before contaminating production analytical warehouses or executive dashboards.

---

## 2. The 5-Layer Quality Control Architecture

```
[ L1: Ingestion Gateway ] -> API payload schema validation (FastAPI / Pydantic)
       | (Pass)
[ L2: Staging Cleansing ] -> Deduplication, type casting & dead-letter queue (Airflow / dbt)
       | (Pass)
[ L3: Warehouse Storage ] -> Database constraints, referential integrity (PostgreSQL / Snowflake)
       | (Pass)
[ L4: Active Monitoring ] -> Daily automated rule assertion test suite (Pytest / Great Expectations)
       | (Pass)
[ L5: Governance & SLAs ] -> Weekly stewardship reviews & Power BI Quality Scorecards
```

---

## 3. Defect Severity & SLA Threshold Matrix

| Severity Tier | Classification | Definition | Permissible Error Budget | Response SLA | Resolution SLA |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **P0 - Critical** | Blocker | Broken primary keys, duplicate identities, financial balance corruption, pipeline crash | **0.0% (Zero Tolerance)** | < 15 minutes | < 2 hours |
| **P1 - High** | Degradation | Missing mandatory attributes, unparseable dates, foreign key buffer delay | **< 0.1%** | < 1 hour | < 8 hours |
| **P2 - Medium** | Non-Critical | Missing optional demographics, slight formatting drift, transient telemetry drop | **< 1.0%** | < 4 hours | < 24 hours |
| **P3 - Low** | Informational | Deprecated tracking fields, cosmetic string spacing, non-impacting metadata | **< 5.0%** | Next Sprint | Next Release |

---

## 4. Incident Remediation & RACI Escalation Matrix

```
+------------------------------------+---------------+-----------------+------------------+-----------------+
| Incident Type                      | Responsible   | Accountable     | Consulted        | Informed        |
+------------------------------------+---------------+-----------------+------------------+-----------------+
| Duplicate User Registration (P0)   | Data Engineer | Eng Lead        | Product Analyst  | Head of Product |
| Ingestion Pipeline Failure (P0)    | Data Engineer | Eng Lead        | DevOps Lead      | Head of Product |
| Missing Tracking Events (P1)       | Product Eng   | Product Analyst | BI Developer     | Growth Lead     |
| Demographic Null Drift (P2)        | Product Eng   | Product Analyst | UX Researcher    | Marketing Lead  |
| Schema Deprecation / Change (P3)   | Data Analyst  | Data Engineer   | BI Developer     | End Users       |
+------------------------------------+---------------+-----------------+------------------+-----------------+
```

---

## 5. Ongoing Quality Verification

The automated test suite implemented in `tests/test_data_quality.py` is integrated into the CI/CD deployment pipeline. Any pull request introducing schema changes, data transformations, or new event models must execute all 27 unit tests with 100% pass rates prior to merging into production branches.
