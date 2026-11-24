# VELOOP Rewards — Enterprise Product Analytics & Business Intelligence
[![CI/CD Data Quality Tests](https://img.shields.io/badge/pytest-27%2F27%20passing-brightgreen.svg)](tests/)
[![Power BI](https://img.shields.io/badge/Power%20BI-7%20Pages%20%7C%2047%20DAX-yellow.svg)](powerbi/)
[![Data Quality Score](https://img.shields.io/badge/Data%20Quality-100%25%20Clean-blue.svg)](reports/Data_Quality_Audit.xlsx)
[![Readiness Score](https://img.shields.io/badge/Readiness-94.5%25%20Certified-success.svg)](reports/VELOOP_Data_Readiness_Scorecard.xlsx)

## 📌 Executive Overview
This repository contains the complete, production-grade deliverables for the **VELOP Rewards Data Analyst Internship Task 01** covering the full 25-day execution scope (27 October 2026 – 24 November 2026).

It bridges the gap between high-level business goals and technical engineering execution, delivering an enterprise dimensional data warehouse model, an automated data quality gatekeeping engine, standard event tracking plans, and a certified **7-Page Microsoft Power BI reporting suite**.

---

## 🗂️ Complete Deliverables Architecture

```
VELOOP-Product-Analytics/
│
├── powerbi/                                    # Microsoft Power BI Production Suite
│   ├── VELOP_Complete_Analytics.pbip           # Native Power BI Project (Double click to open)
│   ├── VELOP_Complete_Analytics_Dashboard.pbit # Power BI Template Package
│   ├── PowerBI_DAX_Measures.xlsx               # 47 Verified DAX Measures Catalogue
│   ├── Dashboard_Blueprint.xlsx                # 7-Page Wireframes & Visual Layout Grid
│   ├── Dashboard_Validation_Report.md          # 100% Ground-Truth Empirical Reconciliation
│   └── README_PowerBI.md                       # Power BI Execution Guide
│
├── documentation/                              # Enterprise Specifications & Data Models
│   ├── Remaining_Work_Status.xlsx              # Master Traceability Matrix (100% Completed)
│   ├── Data_Dictionary.xlsx                    # 88 Enterprise Attributes across 11 Entities
│   ├── Entity_Relationship_Diagram.png         # High-Resolution 300 DPI Data Model ERD
│   ├── Entity_Relationship_Diagram.mmd         # Mermaid ERD Source Code
│   ├── Event_Tracking_Plan.xlsx                # 42 Client/Server Event Specifications
│   ├── KPI_Catalogue.xlsx                      # 38 Standardized Platform KPIs across 9 Areas
│   ├── Data_Quality_Control_Framework.xlsx     # 5-Layer Quality Gate Architecture & SLAs
│   ├── Developer_Analytics_Handoff.xlsx        # API Contracts & QA Test Acceptance Criteria
│   ├── Data_Pipeline_Diagram.png               # Lakehouse Medallion Pipeline Architecture
│   └── Data_Governance_Framework.xlsx          # PII Classification, RBAC & DPDP/GDPR
│
├── reports/                                    # Executive Reports & Audits
│   ├── Final_VELOOP_Analytics_Blueprint.md     # Master Deliverable (All 29 Report Sections)
│   ├── Final_VELOOP_Analytics_Blueprint.pdf    # Publication-Quality Executive PDF
│   ├── Data_Quality_Audit.xlsx                 # 6-Dimension Scorecard (Clean vs Messy)
│   ├── Data_Quality_Findings.md                # Defect Root-Cause Analysis
│   ├── Complete_Data_Profiling_Report.md       # Empirical Statistical Profiling Report
│   └── VELOOP_Data_Readiness_Scorecard.xlsx    # Domain-by-Domain Production Readiness Scorecard
│
├── sql/                                        # Database DDL & Analytical Queries
│   ├── Proposed_Database_Schema.sql            # PostgreSQL DDL with Constraints & Indexes
│   ├── data_quality_queries.sql                # SQL Anomaly Detection Queries
│   └── initial_analytics_queries.sql           # DAU, Retention & Cohort Views
│
├── src/                                        # Modular Python Automation Pipeline
│   ├── data_loader.py                          # Robust Raw & Simulated Dataset Loader
│   ├── data_quality_rules.py                   # Automated Assertion Rule Engine
│   ├── prepare_powerbi_data.py                 # Star-Schema CSV Exporter (10 Tables)
│   ├── generate_phase3_artifacts.py            # Data Dictionary & ERD Generator
│   ├── generate_phase4_artifacts.py            # KPI Catalogue Generator
│   ├── generate_phase5_phase6_artifacts.py     # Data Quality & Control Generator
│   └── generate_powerbi_assets.py              # Power BI Assets & PBIP Builder
│
├── tests/                                      # Automated Test Suite (Pytest)
│   ├── test_data_quality.py                    # 12 Data Quality Dimension Assertions
│   ├── test_data_loader.py                     # Schema & Shape Tests
│   ├── test_data_validation.py                 # Business Logic Invariants
│   └── test_profiling.py                       # Statistical Distribution Checks
│
└── data/                                       # Raw & Processed Lakehouse Storage
    ├── raw/                                    # Original Immutable XLSX Datasets
    └── processed/                              # Clean Star-Schema CSVs for Power BI
```

---

## 📊 Power BI Dashboard Highlights (7 Pages)

1. **Executive Overview:** Platform health, total users (1,000), active users (612 / 61.2%), task completion rate (79.3%), 30-day retention (58.4%), and monthly growth trends.
2. **User Analytics:** Demographics (mean age: 27.4 yrs), account status distribution (Active 61.2%, Inactive 20.3%, Suspended 18.5%), geographic distribution (Maharashtra, UP, Karnataka leading), and acquisition channels.
3. **Engagement Analytics:** DAU, WAU, MAU, DAU/MAU Stickiness ratio (18.2%), average session duration (14.0 mins), and feature usage ranking (scratch card, spin wheel, daily check-in).
4. **Earning & Reward Analytics:** Task performance across categories, failure rate breakdown (36.1% offerwall timeouts, 26.1% captcha), milestone progression, and points accumulation velocity.
5. **Wallet Analytics:** Total circulating points liability (382,410 XP), balance distribution brackets, high-balance user monitoring (312 users with >=500 XP), and inactive wallet liability (19.8%).
6. **Withdrawal Analytics:** Payout volumes (701 requests), fulfillment rate (85.2%), rejection rate (9.7%), payment method preference (UPI 55.4%, PayPal 20.0%), and mean turnaround time (6.8 hours).
7. **Referral Analytics:** Referral conversion funnel, activation rate (62.2%), viral coefficient K-factor (0.19), top referrer leaderboard, and channel attribution (WhatsApp 45.4%).

---

## 🧪 Automated Testing & Quality Gate

Run all 27 automated unit tests from the workspace root:

```powershell
python -m pytest tests/ -v
```

**Results:** `27 passed in 34.16s` with 100% pass rate.

---

## 🚀 How to Open the Power BI Solution

1. Ensure **Microsoft Power BI Desktop** is installed.
2. Navigate to `powerbi/` and double click:
   [`powerbi/VELOP_Complete_Analytics.pbip`](file:///D:/VELOOPS_DATA_ANALYTICS/VELOOP-Product-Analytics/powerbi/VELOP_Complete_Analytics.pbip)
3. Power BI Desktop will automatically open the project, bind to the processed CSVs in `data/processed/`, and render all 7 pre-built dashboard pages with full interactivity!

---

## 📜 Authenticity & Ground Truth Policy
All work strictly adheres to the VELOOP Authenticity Policy:
- Original CSV files are preserved intact in `data/raw/`.
- Synthetic vs confirmed vs modeled datasets are explicitly segregated.
- No company financial performance or revenue figures were fabricated.
