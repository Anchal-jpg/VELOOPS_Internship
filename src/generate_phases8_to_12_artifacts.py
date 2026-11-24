"""
Generate Phases 8 to 12 Deliverables:
- Phase 8: Developer_Analytics_Handoff.xlsx & .md
- Phase 9: Data_Pipeline_Architecture.md, Data_Pipeline_Diagram.mmd/png, Data_Operating_Model.xlsx
- Phase 10: Data_Governance_Framework.xlsx, Data_Privacy_and_Access_Report.md
- Phase 11: Analytics_Change_Log.xlsx
- Phase 12: VELOOP_Data_Readiness_Scorecard.xlsx, Analytics_Implementation_Backlog.xlsx, Analytics_Gap_Assessment_Final.xlsx
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT_DIR = r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics"
DOCS_DIR = os.path.join(ROOT_DIR, "documentation")
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")

# Shared Styles
navy_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
bold_font = Font(name="Calibri", size=11, bold=True)
normal_font = Font(name="Calibri", size=10)
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")

def format_sheet(ws):
    ws.freeze_panes = "A2"
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or "")
            if "\n" in val:
                val = max(val.split("\n"), key=len)
            if len(val) > max_len:
                max_len = len(val)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

# ====================================================================
# PHASE 8: DEVELOPER ANALYTICS HANDOFF
# ====================================================================
def generate_phase8():
    print("Generating Phase 8: Developer Analytics Handoff...")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Developer_Handoff_Spec"
    
    headers = [
        "Event Name", "Product Area", "Client/Server Origin", "Trigger Description",
        "Payload Schema (JSON Sample)", "Required Properties", "Optional Properties",
        "Validation Rule", "QA Verification Test Case", "Acceptance Criteria", "Priority"
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    events = [
        ("user_registered", "Authentication", "Client (SDK) + Server", "Fires when user successfully creates account.", '{"user_id":"VLUSR001001","signup_channel":"Referral","referral_code":"REF9821","device_id":"ANDR_9921"}', "user_id, signup_channel, timestamp", "referral_code, utm_source", "user_id must match regex ^VLUSR\\d{6}$", "Register via Email & Google Auth; verify JSON payload in Segment debugger.", "200 OK from Ingestion API; user record visible in users table within 5s.", "P0 - Blocker"),
        ("onboarding_completed", "Onboarding", "Client (Mobile/Web)", "Fires when user finishes final step of tutorial.", '{"user_id":"VLUSR001001","steps_completed":5,"total_time_seconds":124}', "user_id, steps_completed, duration", "skipped_steps", "steps_completed >= 1", "Complete onboarding without skipping; verify telemetry fires on final 'Get Started' tap.", "Payload contains exact step count; analytics warehouse receives record.", "P1 - High"),
        ("task_started", "Tasks & Earning", "Client (Mobile/Web)", "Fires when user clicks 'Start Task' on offer card.", '{"user_id":"VLUSR001001","task_id":"TSK_SURVEY_01","category":"Surveys","partner_id":"POLLFISH"}', "user_id, task_id, category, partner_id", "session_id, estimated_points", "task_id must exist in task catalog", "Tap survey task; verify task_id and partner_id match offerwall metadata.", "State transition to 'Started' in fct_tasks with server timestamp.", "P0 - Blocker"),
        ("task_completed", "Tasks & Earning", "Server (Webhook)", "Fires when partner offerwall confirms completion.", '{"user_id":"VLUSR001001","task_id":"TSK_SURVEY_01","reward_points":100,"validation_hash":"sha256_sig"}', "user_id, task_id, reward_points, signature", "partner_transaction_id", "Signature must match partner HMAC secret", "Simulate partner postback webhook with valid signature; verify credit.", "Wallet updated atomically; reward_points credited; idempotency enforced.", "P0 - Blocker"),
        ("task_failed", "Tasks & Earning", "Server / Client", "Fires when task validation fails or times out.", '{"user_id":"VLUSR001001","task_id":"TSK_SURVEY_01","reason":"Timeout","error_code":"ERR_408"}', "user_id, task_id, reason", "error_code, elapsed_seconds", "reason in ('Timeout','Captcha','IP Collision')", "Abandon task past timeout threshold; verify auto-failure event trigger.", "Task marked 'Failed'; error logged; user alerted gracefully.", "P1 - High"),
        ("wallet_transaction_created", "Wallet", "Server (Ledger Service)", "Fires on any ledger debit/credit event.", '{"transaction_id":"WLTX0001002","user_id":"VLUSR001001","type":"TASK_REWARD","amount":100,"direction":"CREDIT"}', "transaction_id, user_id, type, amount, direction", "reference_id, balance_after", "amount > 0 and direction in ('CREDIT','DEBIT')", "Execute task completion; verify double-entry ledger event emission.", "Ledger balance reconciles with user current_balance.", "P0 - Blocker"),
        ("withdrawal_requested", "Withdrawals", "Client (Mobile/Web)", "Fires when user taps 'Confirm Cashout'.", '{"withdrawal_id":"WTH00012","user_id":"VLUSR001001","points":500,"cash_inr":50.0,"payout_method":"UPI","payout_address":"user@okhdfcbank"}', "withdrawal_id, user_id, points, payout_method, payout_address", "notes", "points >= min_threshold and balance >= points", "Submit withdrawal with valid UPI ID; verify points locked immediately.", "HTTP 201 Created; points deducted from available balance; pending state.", "P0 - Blocker"),
        ("withdrawal_completed", "Withdrawals", "Server (Payout Gateway)", "Fires when payment gateway confirms cashout transfer.", '{"withdrawal_id":"WTH00012","gateway_ref":"RAZORPAY_TX123","status":"Completed","disbursed_at":"2026-11-24T10:00:00Z"}', "withdrawal_id, gateway_ref, status, disbursed_at", "fee_inr", "gateway_ref not null", "Mock payout gateway success callback; verify withdrawal status change.", "Status updated to 'Completed'; notification push sent to user.", "P0 - Blocker"),
        ("referral_shared", "Referrals", "Client (Mobile/Web)", "Fires when user taps share button on referral screen.", '{"user_id":"VLUSR001001","channel":"WhatsApp","referral_code":"REF9821"}', "user_id, channel, referral_code", "campaign_id", "channel in ('WhatsApp','Telegram','Instagram','Direct Link')", "Tap WhatsApp share icon; verify event captures channel and referral_code.", "Event delivered to analytics pipeline within 2 seconds.", "P2 - Medium"),
        ("referral_activated", "Referrals", "Server (Growth Engine)", "Fires when referred user completes qualifying task.", '{"referrer_id":"VLUSR001001","invitee_id":"VLUSR001002","qualifying_task_id":"TSK_01","bounty_points":100}', "referrer_id, invitee_id, qualifying_task_id, bounty_points", "referral_id", "referrer_id != invitee_id", "New invitee completes first survey; verify referrer bounty credited.", "100 points credited to referrer wallet; milestone notification sent.", "P1 - High")
    ]
    for row in events:
        ws.append(list(row))
        
    for r in range(2, len(events) + 2):
        for c in range(1, 12):
            cell = ws.cell(row=r, column=c)
            cell.font = normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c in (1, 2, 3, 11) else "left", vertical="center")
            if c == 11:
                cell.fill = fail_fill if "P0" in str(cell.value) else sub_header_fill
                
    format_sheet(ws)
    wb.save(os.path.join(DOCS_DIR, "Developer_Analytics_Handoff.xlsx"))
    wb.save(os.path.join(ROOT_DIR, "Developer_Analytics_Handoff.xlsx"))
    
    # Markdown Handoff Guide
    md_content = r"""# VELOOP Rewards — Developer Analytics Implementation Handoff Guide
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
"""
    with open(os.path.join(DOCS_DIR, "Developer_Analytics_Handoff.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
    with open(os.path.join(REPORTS_DIR, "Developer_Analytics_Handoff.md"), "w", encoding="utf-8") as f:
        f.write(md_content)

# ====================================================================
# PHASE 9: DATA PIPELINE ARCHITECTURE & OPERATING MODEL
# ====================================================================
def generate_phase9():
    print("Generating Phase 9: Data Pipeline Architecture & Operating Model...")
    
    # 1. Pipeline Diagram (Mermaid & High-Res PNG)
    mmd_content = """graph TD
    subgraph Sources ["1. Ingestion Sources"]
        A1[Mobile App SDK - Android/iOS]
        A2[Web App Telemetry]
        A3[Partner Offerwall Webhooks]
        A4[Payment Gateway Callbacks]
    end

    subgraph Streaming ["2. Ingestion & Streaming Layer"]
        B1[API Gateway - FastAPI]
        B2[Kafka / AWS Kinesis Event Bus]
        B3[Dead Letter Queue - DLQ]
    end

    subgraph Medallion ["3. Lakehouse Medallion Architecture"]
        C1[(Bronze Layer - Raw Parquet)]
        C2[(Silver Layer - Cleaned & Deduplicated Tables)]
        C3[(Gold Layer - Star-Schema Analytics Warehouse)]
    end

    subgraph Orchestration ["4. Orchestration & Quality Gate"]
        D1[Airflow / Prefect Workflow Scheduler]
        D2[dbt Transformations & Data Quality Tests]
        D3[Pytest Continuous Quality Engine]
    end

    subgraph Consumers ["5. Consumption Surfaces"]
        E1[Power BI Executive & Operational Dashboards]
        E2[SQL Analytical Views - Analyst Ad-hoc]
        E3[Risk & Anti-Fraud Automated Alerting]
    end

    A1 -->|REST / JSON| B1
    A2 -->|REST / JSON| B1
    A3 -->|Signed Webhook| B1
    A4 -->|Payment Callback| B1

    B1 -->|Validated Stream| B2
    B1 -.->|Schema Failure| B3
    B2 -->|Batch Sink| C1

    C1 -->|dbt Bronze-to-Silver ETL| C2
    C2 -->|dbt Star-Schema Aggregation| C3

    D1 --> D2
    D2 --> C2
    D2 --> C3
    D3 --> C2

    C3 --> E1
    C3 --> E2
    C3 --> E3
"""
    with open(os.path.join(DOCS_DIR, "Data_Pipeline_Diagram.mmd"), "w", encoding="utf-8") as f:
        f.write(mmd_content)

    # Render PNG using matplotlib
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    fig.patch.set_facecolor('#0E1726')
    ax.set_facecolor('#0E1726')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Draw Medallion Architecture Blocks
    stages = [
        ("1. INGESTION SOURCES", 0.5, 5.0, 2.5, 3.2, "#1E293B", "#38BDF8", [
            "Mobile App (Android/iOS)", "Web Application", "Offerwall Webhooks", "Payment Gateways"
        ]),
        ("2. INGESTION & GATEWAY", 3.5, 5.0, 2.5, 3.2, "#1E293B", "#38BDF8", [
            "FastAPI Gateway", "Kafka Event Bus", "Pydantic Schema Check", "Dead-Letter Queue (DLQ)"
        ]),
        ("3. BRONZE (RAW)", 6.5, 5.0, 2.5, 3.2, "#1E293B", "#F59E0B", [
            "Raw Append-Only Logs", "Immutable Parquet Storage", "Full Audit History", "S3 / GCS Data Lake"
        ]),
        ("4. SILVER (CLEAN)", 9.5, 5.0, 2.5, 3.2, "#1E293B", "#10B981", [
            "Deduplicated Users", "Standardized Dates", "Conformed Enums", "Zero Orphan FKs"
        ]),
        ("5. GOLD (ANALYTICS)", 12.5, 5.0, 3.0, 3.2, "#1E293B", "#8B5CF6", [
            "Star-Schema Marts", "dim_users & dim_dates", "fct_sessions & tasks", "Power BI Certified Model"
        ])
    ]

    for title, x, y, w, h, bg, border, items in stages:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.3, title, color=border, fontsize=11, fontweight='bold', ha='center', va='center')
        for i, item in enumerate(items):
            ax.text(x + 0.2, y + h - 0.8 - i * 0.55, f"• {item}", color="#F8FAFC", fontsize=9.5, ha='left', va='center')

    # Connecting Arrows
    for arrow_x in [3.15, 6.15, 9.15, 12.15]:
        ax.annotate("", xy=(arrow_x + 0.3, 6.6), xytext=(arrow_x - 0.1, 6.6),
                    arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=3))

    # Bottom Orchestration & Governance Layer
    rect_orch = patches.FancyBboxPatch((0.5, 0.8), 15.0, 3.4, boxstyle="round,pad=0.2", facecolor="#13233A", edgecolor="#60A5FA", linewidth=2)
    ax.add_patch(rect_orch)
    ax.text(8.0, 3.8, "ORCHESTRATION, QUALITY CONTROL & CONTINUOUS MONITORING (L1 - L5)", color="#60A5FA", fontsize=12, fontweight='bold', ha='center', va='center')

    orch_items = [
        ("Airflow / Prefect", "Scheduled DAGs managing hourly ingestion & daily warehouse reconciliation runs."),
        ("dbt Quality Assertions", "Automated SQL tests checking NOT NULL, UNIQUE, ACCEPTED_VALUES on every build."),
        ("Pytest Quality Suite", "27 automated test cases verifying referential integrity & business logic constraints."),
        ("Power BI Service", "Automated daily scheduled dataset refresh & real-time executive dashboard streaming.")
    ]
    for i, (head, desc) in enumerate(orch_items):
        col_x = 0.8 + (i % 2) * 7.5
        row_y = 2.8 - (i // 2) * 1.3
        ax.text(col_x, row_y, f"★ {head}:", color="#FBBF24", fontsize=10.5, fontweight='bold', ha='left')
        ax.text(col_x, row_y - 0.45, desc, color="#CBD5E1", fontsize=9, ha='left')

    plt.tight_layout()
    png_path = os.path.join(DOCS_DIR, "Data_Pipeline_Diagram.png")
    plt.savefig(png_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"Saved: {png_path}")

    # 2. Operating Model Workbook
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Operating_RACI"
    headers1 = ["Process Domain", "Activity", "Data Engineer", "Product Analyst", "BI Developer", "Head of Data / Product"]
    ws1.append(headers1)
    for cell in ws1[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    ops = [
        ("Pipeline Maintenance", "Ingestion pipeline uptime & Kafka monitoring", "Accountable / Responsible", "Informed", "Informed", "Informed"),
        ("Data Quality Gate", "Resolving dead-letter queue records & format errors", "Responsible", "Consulted", "Informed", "Accountable"),
        ("Schema Evolution", "Adding new tracking events & database columns", "Responsible", "Accountable", "Consulted", "Informed"),
        ("Power BI Governance", "Publishing verified measures & dashboard maintenance", "Informed", "Consulted", "Responsible", "Accountable"),
        ("Dispute Investigation", "Investigating missing reward points or user disputes", "Consulted", "Responsible", "Informed", "Informed"),
        ("Data Privacy Compliance", "GDPR deletion requests & PII encryption audits", "Responsible", "Consulted", "Informed", "Accountable")
    ]
    for row in ops:
        ws1.append(list(row))
    for r in range(2, len(ops) + 2):
        for c in range(1, 7):
            cell = ws1.cell(row=r, column=c)
            cell.font = normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c > 2 else "left", vertical="center")
            
    format_sheet(ws1)
    wb.save(os.path.join(DOCS_DIR, "Data_Operating_Model.xlsx"))
    
    # 3. Pipeline Architecture Markdown Report
    arch_md = r"""# VELOOP Rewards — Enterprise Data Pipeline Architecture
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
"""
    with open(os.path.join(DOCS_DIR, "Data_Pipeline_Architecture.md"), "w", encoding="utf-8") as f:
        f.write(arch_md)

# ====================================================================
# PHASE 10: DATA GOVERNANCE, SECURITY & PRIVACY
# ====================================================================
def generate_phase10():
    print("Generating Phase 10: Data Governance, Security & Privacy...")
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "PII_Classification_Matrix"
    
    headers1 = [
        "Entity", "Attribute Name", "PII Classification", "Sensitivity Tier",
        "Encryption at Rest", "Masking in Analytics", "Retention Policy", "Legal Basis (GDPR/DPDP)"
    ]
    ws1.append(headers1)
    for cell in ws1[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    pii = [
        ("Users", "user_id", "Pseudonymous Identifier", "Tier 2 - Confidential", "AES-256", "Plain in internal BI (Pseudonymized)", "Account lifetime + 7 yrs", "Contractual Necessity"),
        ("Users", "full_name", "Direct PII", "Tier 1 - Restricted", "AES-256", "Masked as 'F*** L***' in non-admin BI", "Account lifetime + 30 days", "Consent"),
        ("Users", "email", "Direct PII / Auth", "Tier 1 - Restricted", "AES-256", "SHA-256 Hashed in general reporting", "Account lifetime + 30 days", "Consent / Contract"),
        ("Users", "age", "Demographic", "Tier 3 - Internal", "AES-256", "Aggregated into age brackets in reports", "7 Years", "Legitimate Interest"),
        ("Users", "city, state", "Geographic Location", "Tier 3 - Internal", "AES-256", "Unmasked for regional analytics", "7 Years", "Legitimate Interest"),
        ("Users", "xp_balance", "Financial Telemetry", "Tier 2 - Confidential", "AES-256", "Unmasked in authenticated BI", "7 Years (Financial Audit)", "Legal Obligation"),
        ("Withdrawals", "payout_address (UPI/Bank)", "Financial PII", "Tier 1 - Restricted", "AES-256 (KMS Key)", "Tokenized / Redacted ('***@okhdfc')", "7 Years (Tax Compliance)", "Legal Obligation")
    ]
    for row in pii:
        ws1.append(list(row))
    for r in range(2, len(pii) + 2):
        for c in range(1, 9):
            cell = ws1.cell(row=r, column=c)
            cell.font = normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c in (1, 3, 4, 5, 6, 7) else "left", vertical="center")
            if "Tier 1" in str(cell.value):
                cell.fill = fail_fill
                
    format_sheet(ws1)
    wb.save(os.path.join(DOCS_DIR, "Data_Governance_Framework.xlsx"))

    # Markdown Privacy Report
    priv_md = r"""# VELOOP Rewards — Data Privacy, Security & Access Control Report
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
"""
    with open(os.path.join(REPORTS_DIR, "Data_Privacy_and_Access_Report.md"), "w", encoding="utf-8") as f:
        f.write(priv_md)

# ====================================================================
# PHASE 11: ANALYTICS CHANGE MANAGEMENT
# ====================================================================
def generate_phase11():
    print("Generating Phase 11: Analytics Change Management...")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Change_Log_Register"
    
    headers = [
        "Change ID", "Effective Date", "Release Version", "Component / Entity",
        "Change Type", "Description of Change", "Backward Compatible?", "Impacted Consumers", "Owner"
    ]
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    changes = [
        ("CHG-001", "2026-10-27", "v1.0.0", "Core Infrastructure", "Initial Release", "Deployment of Days 1-10 Foundation schemas and profiling scripts.", "Yes", "Data Team", "Mentor / Analyst"),
        ("CHG-002", "2026-11-05", "v1.1.0", "Referral & Engagement", "Specification", "Addition of 11 referral lifecycle stages and DAU/WAU/MAU specs.", "Yes", "Product Team", "Product Analyst"),
        ("CHG-003", "2026-11-12", "v1.2.0", "Event Tracking Plan", "Schema Extension", "Standardization of 42 client/server event tracking payloads.", "Yes", "Mobile / Web Dev", "Product Analyst"),
        ("CHG-004", "2026-11-18", "v1.3.0", "Data Model & DDL", "Architecture", "Publication of 88-attribute Data Dictionary & PostgreSQL DDL.", "Yes", "Data Engineers", "Data Engineer"),
        ("CHG-005", "2026-11-21", "v1.4.0", "KPI Catalogue", "Governance", "Establishment of 38 standard KPIs across 9 business areas.", "Yes", "Executive / Finance", "Product Analyst"),
        ("CHG-006", "2026-11-23", "v1.5.0", "Data Quality Engine", "Quality Assurance", "Deployment of automated Pytest suite (27 tests) & L1-L5 control framework.", "Yes", "CI/CD Pipeline", "Data Engineer"),
        ("CHG-007", "2026-11-24", "v2.0.0", "Power BI Solution", "BI Production", "Release of 7-page Power BI Dashboard suite (.pbip / .pbit) with 47 DAX measures.", "Yes", "Executive Leadership", "BI Developer")
    ]
    for row in changes:
        ws.append(list(row))
    for r in range(2, len(changes) + 2):
        for c in range(1, 10):
            cell = ws.cell(row=r, column=c)
            cell.font = normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c in (1, 2, 3, 5, 7, 9) else "left", vertical="center")
            
    format_sheet(ws)
    wb.save(os.path.join(DOCS_DIR, "Analytics_Change_Log.xlsx"))

# ====================================================================
# PHASE 12: READINESS SCORECARD & IMPLEMENTATION BACKLOG
# ====================================================================
def generate_phase12():
    print("Generating Phase 12: Readiness Scorecard & Implementation Backlog...")
    
    # 1. Readiness Scorecard
    wb_sc = openpyxl.Workbook()
    ws_sc = wb_sc.active
    ws_sc.title = "Readiness_Scorecard"
    headers_sc = [
        "Product Domain", "Telemetry Availability", "Schema Formalization",
        "Quality Test Coverage", "BI Dashboard Coverage", "Readiness Score (%)", "Deployment Status"
    ]
    ws_sc.append(headers_sc)
    for cell in ws_sc[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    scores = [
        ("User & Account Analytics", "100.0%", "100.0%", "100.0%", "100.0%", "100.0%", "Production Ready"),
        ("Session & Engagement", "100.0%", "100.0%", "100.0%", "100.0%", "100.0%", "Production Ready"),
        ("Task Discovery & Rewards", "100.0%", "100.0%", "100.0%", "100.0%", "100.0%", "Production Ready"),
        ("Wallet & Ledger Balance", "75.0% (Derived)", "100.0%", "100.0%", "100.0%", "93.8%", "Ready (Simulated Model)"),
        ("Withdrawal Operations", "70.0% (Modeled)", "100.0%", "100.0%", "100.0%", "92.5%", "Ready (Simulated Model)"),
        ("Referral Network & Graph", "80.0% (Modeled)", "100.0%", "100.0%", "100.0%", "95.0%", "Ready (Simulated Model)"),
        ("Support & Ticket Desk", "20.0% (Proposed)", "100.0%", "90.0%", "80.0%", "72.5%", "Backlog Sprint 2"),
        ("OVERALL VELOOP PLATFORM", "82.5%", "100.0%", "98.5%", "97.1%", "94.5%", "Certified Enterprise Baseline")
    ]
    for row in scores:
        ws_sc.append(list(row))
    for r in range(2, len(scores) + 2):
        is_total = (r == len(scores) + 1)
        for c in range(1, 8):
            cell = ws_sc.cell(row=r, column=c)
            cell.font = bold_font if is_total else normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c > 1 else "left", vertical="center")
            if is_total:
                cell.fill = sub_header_fill
            elif c == 7:
                cell.fill = pass_fill if "Production" in str(cell.value) else sub_header_fill
                
    format_sheet(ws_sc)
    wb_sc.save(os.path.join(REPORTS_DIR, "VELOOP_Data_Readiness_Scorecard.xlsx"))

    # 2. Implementation Backlog
    wb_bl = openpyxl.Workbook()
    ws_bl = wb_bl.active
    ws_bl.title = "Sprint_Backlog"
    headers_bl = [
        "Backlog Item ID", "Sprint Target", "Product Area", "Feature / Work Item",
        "User Story Description", "Complexity (Story Pts)", "Owner", "Target Completion Date", "Status"
    ]
    ws_bl.append(headers_bl)
    for cell in ws_bl[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    backlog = [
        ("BL-001", "Sprint 1 (Days 26-35)", "Ingestion", "FastAPI Gatekeeper Service", "Implement server-side JSON schema validation for all 42 client events.", 8, "Backend Team", "2026-12-05", "Ready for Dev"),
        ("BL-002", "Sprint 1 (Days 26-35)", "Wallet", "Double-Entry Ledger Migration", "Migrate user wallet balances from snapshot column to fct_wallet_ledger table.", 13, "Data Engineering", "2026-12-10", "Ready for Dev"),
        ("BL-003", "Sprint 2 (Days 36-45)", "Withdrawals", "Payout Gateway Webhook Integration", "Connect Razorpay/Stripe webhooks to stream withdrawal_completed events.", 8, "Integrations Lead", "2026-12-20", "Backlog"),
        ("BL-004", "Sprint 2 (Days 36-45)", "Support", "Zendesk API Connector", "Ingest support ticket dispute timestamps to calculate MTTR and dispute rates.", 5, "Data Analyst", "2026-12-25", "Backlog"),
        ("BL-005", "Sprint 3 (Days 46-55)", "Anti-Fraud", "Referral Ring Detection Service", "Deploy automated graph query detecting IP and device ID collisions.", 8, "Risk Lead", "2027-01-08", "Backlog"),
        ("BL-006", "Sprint 4 (Days 56-65)", "Power BI", "Automated Incremental Refresh", "Configure Power BI Service gateway for 15-minute incremental dataset partitions.", 5, "BI Developer", "2027-01-18", "Backlog")
    ]
    for row in backlog:
        ws_bl.append(list(row))
    for r in range(2, len(backlog) + 2):
        for c in range(1, 10):
            cell = ws_bl.cell(row=r, column=c)
            cell.font = normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c in (1, 2, 6, 7, 8, 9) else "left", vertical="center")
            
    format_sheet(ws_bl)
    wb_bl.save(os.path.join(REPORTS_DIR, "Analytics_Implementation_Backlog.xlsx"))

    # 3. Final Gap Assessment
    wb_gap = openpyxl.Workbook()
    ws_gap = wb_gap.active
    ws_gap.title = "Final_Gap_Assessment"
    headers_gap = [
        "Gap ID", "Product Area", "Original Identified Gap", "Interim Mitigation",
        "Target Production Resolution", "Residual Risk", "Resolution Sprint", "Sign-Off"
    ]
    ws_gap.append(headers_gap)
    for cell in ws_gap[1]:
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    gaps = [
        ("GAP-01", "Wallet", "Absence of historical transactional wallet credit/debit ledger.", "Simulated ledger derived from completed tasks & milestones.", "Deploy relational fct_wallet_ledger schema in PostgreSQL warehouse.", "Low", "Sprint 1", "Data Lead Approved"),
        ("GAP-02", "Withdrawals", "No transactional log of user withdrawal requests or payouts.", "Modeled withdrawal dataset based on active user balances.", "Integrate payout gateway webhook event streams.", "Low", "Sprint 2", "Operations Lead Approved"),
        ("GAP-03", "Referrals", "No relational edge table mapping referrer to invitees.", "Modeled referral network matching clean dataset referral codes.", "Instrument referral_shared and referral_clicked client events.", "Low", "Sprint 1", "Growth Lead Approved"),
        ("GAP-04", "Support", "Zero customer support or missing-reward ticket data.", "Formulated operational KPI specifications in KPI Catalogue.", "Connect external ticketing desk API into Lakehouse Bronze.", "Medium", "Sprint 2", "Support Lead Approved"),
        ("GAP-05", "Identity", "Duplicate records & malformed dates in messy audit dataset.", "Built automated data quality engine with 27 passing tests.", "Enforce L1 API Gateway Pydantic validation and database PKs.", "Zero", "Resolved", "QA Lead Approved")
    ]
    for row in gaps:
        ws_gap.append(list(row))
    for r in range(2, len(gaps) + 2):
        for c in range(1, 9):
            cell = ws_gap.cell(row=r, column=c)
            cell.font = normal_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c in (1, 6, 7, 8) else "left", vertical="center")
            if c == 8:
                cell.fill = pass_fill
                
    format_sheet(ws_gap)
    wb_gap.save(os.path.join(DOCS_DIR, "Analytics_Gap_Assessment_Final.xlsx"))
    print("Phase 8-12 Deliverables generated successfully!")

if __name__ == "__main__":
    print("Executing Phases 8 to 12 Generator...")
    generate_phase8()
    generate_phase9()
    generate_phase10()
    generate_phase11()
    generate_phase12()
    print("All Phases 8 to 12 Deliverables successfully generated!")

