# VELOOP Rewards — Enterprise Data Pipeline Architecture
**Internship Work-Scope Target:** Phase 9 Deliverable  
**Creation Date:** 24 November 2026  
**Document Reference:** `documentation/Data_Pipeline_Architecture.md`  
**Diagram Reference:** [`Data_Pipeline_Diagram.png`](file:///D:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Data_Pipeline_Diagram.png)

---

## 1. Architectural Overview

The VELOOP analytics platform leverages a **Medallion Lakehouse Architecture** (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) designed to deliver sub-second event ingestion, automated quality gatekeeping, and certified business intelligence reporting.

---

## 2. Medallion Layer Specifications

1. **Bronze Layer (Raw Ingestion):**
   - Stores immutable, append-only raw JSON and Parquet files directly from mobile SDKs, webhooks, and gateway APIs.
   - Preserves source audit trails, client timestamps, and HTTP headers without modification.
2. **Silver Layer (Cleaned & Conformed):**
   - Executes deduplication (window functions), datatype casting, ISO timestamp normalization, and quarantine of invalid records.
   - Enforces 100% referential integrity; ensures child events resolve to known `user_id` records.
3. **Gold Layer (Analytics Marts):**
   - High-performance dimensional star-schema (`dim_users`, `dim_dates`, `fct_tasks`, `fct_sessions`, `fct_wallet_ledger`, `fct_withdrawals`, `fct_referrals`).
   - Powers the certified Microsoft Power BI reporting suite and ad-hoc SQL exploratory queries.

---

## 3. Disaster Recovery & High Availability

- **RPO (Recovery Point Objective):** $\le 15$ minutes via continuous point-in-time database WAL archiving.
- **RTO (Recovery Time Objective):** $\le 2$ hours automated containerized failover to secondary cloud region.
