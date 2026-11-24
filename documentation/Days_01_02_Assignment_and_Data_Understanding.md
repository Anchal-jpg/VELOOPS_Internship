# VELOOP REWARDS — DAYS 1–2: ASSIGNMENT & DATA UNDERSTANDING SYNTHESIS

**Author:** Senior Data Analyst & Engineering Mentor Team  
**Execution Scope:** Days 1–2 (27 October 2026 – 28 October 2026)  
**Document Generation Date:** 13 November 2026  
**Document Status:** Complete & Audited  
**Repository Location:** `documentation/Days_01_02_Assignment_and_Data_Understanding.md`  

---

## 1. Assignment Overview & Strategic Intent

The **VELOOP Rewards Task 01** represents a foundational blueprint engagement for a developing online rewards platform. Unlike conventional analytics projects where mature data lakes and years of historical telemetry already exist, VELOOP is actively designing its analytical architecture and data infrastructure. 

### Core Responsibility
As senior data and product analysts, our mandate is **not to manufacture flattering performance figures**, but to answer five strategic questions for VELOOP:
1. **What must VELOOP track?** (Granular event taxonomy, user journeys, system transactions).
2. **How should VELOOP structure it?** (Relational schemas, event tracking plans, logical data models).
3. **How do we know the data is trustworthy?** (Data quality controls, foreign key integrity, anomaly audits).
4. **What should leadership measure?** (Standardized KPIs, financial liabilities, cohort retention).
5. **What should engineering implement?** (Developer specifications, idempotent transaction logging, event payloads).

---

## 2. Product Understanding & Ecosystem Architecture

VELOOP operates as a multi-currency user reward ecosystem designed to incentivize daily engagement, ad consumption, offer completion, and social viral loops.

### Virtual Currencies & Assets
- **VEs (Virtual Earnings):** Micro-earnings awarded for high-frequency actions (Tap & Earn, CAPTCHA, Ad views).
- **XP (Experience Points):** Progression metric determining user level, unlocking multipliers and exclusive tasks.
- **Gems:** Premium in-app utility currency used to enter raffles, spin high-tier wheels, or unlock VIP missions.
- **Tokens:** Liquid platform tokens redeemable for real-world fiat cashouts, gift cards, or crypto.
- **Spins:** Consumable tickets for the chance-based wheel mechanic.

```
       +-------------------------------------------------------------+
       |                  VELOOP REWARDS ECOSYSTEM                   |
       +-------------------------------------------------------------+
                                      |
         +----------------------------+----------------------------+
         |                                                         |
         v                                                         v
+------------------+                                     +------------------+
|   EARNING CORE   |                                     |  GAMIFICATION &  |
|                  |                                     |    RETENTION     |
| - Watch Ads      |                                     | - Daily Rewards  |
| - Tap & Earn     |                                     | - Streaks        |
| - Mining         |                                     | - Missions       |
| - Surveys & Tasks|                                     | - Level System   |
| - Follow & Earn  |                                     | - Badges/Ranks   |
+--------+---------+                                     +--------+---------+
         |                                                         |
         +----------------------------+----------------------------+
                                      |
                                      v
                        +---------------------------+
                        |     WALLET & EXCHANGE     |
                        |                           |
                        | - Multi-Currency Balances |
                        | - Token/Gem Conversion    |
                        | - Ledger Transaction Log  |
                        +-------------+-------------+
                                      |
                                      v
                        +---------------------------+
                        |    WITHDRAWAL PIPELINE    |
                        |                           |
                        | - Payout Requests (UPI/PP)|
                        | - Fraud & KYC Verification|
                        | - Payment Gateway Handoff |
                        +---------------------------+
```

---

## 3. Data Classification Discipline

In compliance with assignment Section 6 and Section 34, every data element and specification in this project is explicitly categorized into one of four verified tiers:

```
+----------------------------------------------------------------------------------------------------+
| DATA CLASSIFICATION REGISTER                                                                       |
+--------------------+-----------------------------------------------------+-------------------------+
| Tier               | Definition                                          | Examples in Project     |
+--------------------+-----------------------------------------------------+-------------------------+
| CONFIRMED          | Verified directly against assignment requirements   | 15 Feature domains;     |
|                    | or inspected raw datasets.                          | 1,000 clean user rows;  |
|                    |                                                     | 35,704 event rows;      |
|                    |                                                     | user_id format regex.   |
+--------------------+-----------------------------------------------------+-------------------------+
| SIMULATED          | Fictional data supplied for testing. Must never be  | Registration timestamps;|
|                    | cited as real VELOOP performance or revenue.        | session durations;      |
|                    |                                                     | synthetic survey tasks. |
+--------------------+-----------------------------------------------------+-------------------------+
| PROPOSED           | Analytical models, event tracking schemas, and KPIs | Double-entry ledger DDL;|
|                    | designed by the analyst to resolve system gaps.     | 5-stage withdrawal flow;|
|                    | Requires engineering review before implementation.  | registration funnels.   |
+--------------------+-----------------------------------------------------+-------------------------+
| TO BE VERIFIED     | Assumptions and technical unknowns that require     | Payment gateway specs;  |
|                    | confirmation with VELOOP backend developers.        | client offline caching; |
|                    |                                                     | ad network SDK timeout. |
+--------------------+-----------------------------------------------------+-------------------------+
```

---

## 4. Initial 10-Day Work Breakdown Structure (WBS)

The first 10 days of the 22–25 day total assignment focus on auditing data readiness, specifying foundational user, earning, and financial analytics, building modular Python profiling tools, and writing SQL data models:

```
[Days 1-2] Discovery & Data Inspection
   ├── PDF Requirements Audit & Governance Policy Enforcement
   ├── Raw Dataset Profiling & Referential Integrity Check
   └── Artifacts: Assignment_Requirement_Matrix, Dataset_Inspection_Report, Source_Register, Feature_Inventory

[Days 3-4] Product Data Readiness Audit
   ├── 15-Feature Action-Outcome Mapping & Coverage Matrix
   ├── 10+ Critical Analytics Gaps Identification & Scoring
   └── Artifacts: Product_Data_Readiness_Audit, Data_Coverage_Matrix, Gap_Assessment, Readiness_Report

[Days 5-6] User & Account Analytics Specification
   ├── Identity Hierarchy (VLUSR / SESS / EVT) & Funnel State Machines
   ├── Demographic, Technical & Geographic Data Contracts
   └── Artifacts: User_Analytics_Specification, User_Account_Analytics_Report

[Days 7-8] Earning & Reward Analytics Specification
   ├── Task Lifecycle Modeling (Discovery -> Completed -> Credited)
   ├── Decoupling Task Execution from Financial Reward Ledger
   └── Artifacts: Earning_Reward_Analytics_Specification, Reward_Lifecycle_Report

[Days 9-10] Wallet & Withdrawal Analytics Specification
   ├── Double-Entry Ledger Architecture & Idempotent Transactions
   ├── 5-Stage Withdrawal Pipeline & Anti-Fraud Verification
   └── Artifacts: Wallet_Analytics_Specification, Withdrawal_Analytics_Specification, Wallet_Withdrawal_Report

[Days 1-10 Foundations] Python, SQL & Comprehensive Synthesis
   ├── 7 Modular Python Profiling Scripts & Jupyter Notebook (01_data_profiling.ipynb)
   ├── 3 Enterprise SQL Scripts (Proposed DDL, DQ Assertions, Analytics Queries)
   └── Deliverable: First_10_Days_Completion_Report
```

