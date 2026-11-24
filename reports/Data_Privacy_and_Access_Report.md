# VELOOP Rewards — Data Privacy, Security & Access Control Report
**Internship Work-Scope Target:** Phase 10 Deliverable  
**Creation Date:** 24 November 2026  
**Document Reference:** `reports/Data_Privacy_and_Access_Report.md`  
**Master Framework:** [`Data_Governance_Framework.xlsx`](file:///D:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/Data_Governance_Framework.xlsx)

---

## 1. Compliance Mandate

The VELOOP Rewards data architecture is strictly designed to comply with the **Digital Personal Data Protection Act (DPDP Act 2023)** and the **General Data Protection Regulation (GDPR)**.

---

## 2. Key Privacy Mechanisms

1. **Pseudonymization by Design:** In analytical fact tables (`fct_sessions`, `fct_tasks`, `fct_wallet_ledger`), records are linked strictly via synthetic pseudonymous identifier `user_id`. Direct identifiers (`full_name`, `email`, phone numbers) are isolated in an encrypted identity vault accessible only to authorized compliance administrators.
2. **Role-Based Access Control (RBAC):**
   - **Executive / Management:** High-level aggregated metrics; no row-level PII visibility.
   - **Product Analysts:** Pseudonymized user behavior telemetry; masked emails.
   - **Customer Support:** User-specific lookup by verified ticket; unmasked contact details with audit logging.
   - **Data Engineers:** DDL/DML access to pipeline infrastructure; audited queries.
3. **Right to Erasure (RTBF):** Automated deletion pipeline removes personal records within 30 calendar days upon user request, while retaining anonymized, aggregated ledger summaries for statutory financial auditing.
