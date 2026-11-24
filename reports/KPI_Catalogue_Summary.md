# VELOOP Rewards — Enterprise KPI Catalogue Summary Report
**Internship Work-Scope Target:** Days 19–21 (Phase 4 Deliverable)  
**Creation Date:** 24 November 2026  
**Document Reference:** `reports/KPI_Catalogue_Summary.md`  
**Master Spreadsheet:** [`KPI_Catalogue.xlsx`](file:///D:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/documentation/KPI_Catalogue.xlsx)

---

## 1. Executive Summary & Objective

The **KPI Catalogue** establishes the single source of truth for all business, product, operational, and financial performance metrics across the VELOOP Rewards ecosystem. Standardizing 38 core key performance indicators across 9 functional business areas, this catalogue bridges the gap between high-level company goals and granular underlying data events.

In strict alignment with the **Authenticity and Ground Truth Policy**, all KPIs are explicitly tagged with their empirical availability:
- **Available in Provided Data (16 KPIs / 42.1%):** Calculated directly from the clean sample ($N=1,000$ users) and simulated user behavior dataset ($N=7,913$ sessions, $N=35,704$ feature events, $N=9,846$ tasks).
- **Partially Available (6 KPIs / 15.8%):** Computable via proxy joins or synthetic attribution models with documented limitations.
- **Proposed / Missing Instrumentation (16 KPIs / 42.1%):** Formally specified for engineering implementation (covering financial wallet ledgers, withdrawal processing, and external support desks).

---

## 2. Business Area Coverage Summary

| Business Area | Total KPIs | Available in Data | Partially Available | Proposed / Missing | P0 Critical | P1 High | P2 Medium |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **User Analytics** | 4 | 3 | 0 | 1 | 2 | 2 | 0 |
| **User Acquisition** | 3 | 0 | 1 | 2 | 1 | 2 | 0 |
| **User Engagement** | 7 | 6 | 0 | 1 | 3 | 4 | 0 |
| **Task & Mission Performance** | 5 | 5 | 0 | 0 | 2 | 2 | 1 |
| **Reward Lifecycle** | 4 | 1 | 1 | 2 | 1 | 2 | 1 |
| **Wallet Health** | 3 | 1 | 1 | 1 | 1 | 2 | 0 |
| **Withdrawal Operations** | 4 | 0 | 1 | 3 | 2 | 1 | 1 |
| **Referral Virality** | 4 | 0 | 2 | 2 | 1 | 3 | 0 |
| **Support & Resolution** | 4 | 0 | 0 | 4 | 0 | 2 | 2 |
| **TOTAL REGISTER** | **38** | **16 (42.1%)** | **6 (15.8%)** | **16 (42.1%)** | **13 (34.2%)** | **20 (52.6%)** | **5 (13.2%)** |

---

## 3. High-Priority (P0 Critical) Metric Specifications

### 1. `KPI-USR-01`: Total Registered Users
- **Formula:** $\text{COUNT}(\text{DISTINCT } \text{user\_id})$
- **Data Source:** Clean User Sample / User Master Database
- **Availability:** Confirmed Available ($N=1,000$ synthetic users in sample).
- **Owner:** Product Analyst

### 2. `KPI-USR-02`: Active Account Rate
- **Formula:** $\left( \frac{\text{COUNT}(\text{user\_id WHERE status = 'Active'})}{\text{COUNT}(\text{total user\_id})} \right) \times 100$
- **Empirical Baseline:** 61.2% in clean sample ($N=612$ Active, $N=203$ Inactive, $N=185$ Suspended).
- **Owner:** Product Analyst

### 3. `KPI-ENG-01` & `KPI-ENG-02`: DAU / MAU Stickiness
- **Formula:** $\text{Stickiness} = \left( \frac{\text{DAU}}{\text{MAU}} \right) \times 100$
- **Calculation Basis:** Derived from 7,913 synthetic session starts over 180 calendar days.
- **Owner:** Product Analyst

### 4. `KPI-TSK-01`: Task Completion Rate
- **Formula:** $\left( \frac{\text{COUNT}(\text{tasks WHERE status = 'Completed'})}{\text{COUNT}(\text{total task attempts})} \right) \times 100$
- **Data Source:** Simulated Task Dataset ($N=9,846$ records).
- **Target Benchmark:** $\ge 80.0\%$
- **Owner:** Operations Analyst

### 5. `KPI-WLT-01`: Circulating Point Liability
- **Formula:** $\sum \text{current\_balance} \quad \forall \text{ active wallets}$
- **Business Impact:** Primary balance sheet liability metric governing cash reserves required to honor user cashouts.
- **Availability:** Derived as current sum from user snapshot; ledger history proposed.
- **Owner:** Finance Lead

### 6. `KPI-WTH-01`: Withdrawal Fulfillment Rate
- **Formula:** $\left( \frac{\text{COUNT}(\text{withdrawals WHERE status = 'Completed'})}{\text{COUNT}(\text{total withdrawal requests})} \right) \times 100$
- **Target Benchmark:** $\ge 92.0\%$
- **Status:** Proposed Specification. Crucial for payout gateway monitoring.
- **Owner:** Operations Manager

### 7. `KPI-REF-01`: Viral Coefficient ($K$-Factor)
- **Formula:** $K = i \times c$ (Average invites sent per active user $\times$ conversion rate per invite)
- **Target Benchmark:** $\ge 1.15$ for viral growth.
- **Status:** Partially Available (graph modeled in Phase 1; click tracking proposed in Phase 2).
- **Owner:** Growth Lead

---

## 4. Governance & Implementation Roadmap

1. **Phase 7 Power BI Integration:** The 16 directly available and 6 partially available KPIs are wired directly into the 7-page interactive dashboard suite (`powerbi/VELOP_Complete_Analytics_Dashboard.pbix`).
2. **Phase 8 Developer Handoff:** The 16 proposed metrics are bundled with exact event schema payloads and REST API specifications in `documentation/Developer_Analytics_Handoff.xlsx`.
3. **Continuous Auditing:** Data quality rules and automated validation tests in `tests/test_data_quality.py` verify that numerator and denominator integrity are maintained across ingestion batches.
