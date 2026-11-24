"""
Script to generate Phase 0 Deliverable: Remaining_Work_Status.xlsx
Maps all deliverables, assignment requirements, and phase roadmaps.
"""

import sys
from pathlib import Path
import openpyxl

base_dir = Path(r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics")
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from report_utils import ReportUtils

def save_styled_workbook(wb: openpyxl.Workbook, file_path: Path):
    for sheet_name in wb.sheetnames:
        ReportUtils.apply_excel_styling(wb, sheet_name)
    wb.save(file_path)
    print(f"Saved: {file_path}")

def create_remaining_work_status():
    wb = openpyxl.Workbook()
    
    # ----------------------------------------------------
    # Sheet 1: Deliverable_Audit_Status
    # ----------------------------------------------------
    ws1 = wb.active
    ws1.title = "Deliverable_Audit_Status"
    
    headers1 = [
        "Deliverable_ID", "Phase", "Deliverable_Name", "File_Type",
        "Target_Path", "Audit_Status", "File_Exists_On_Disk",
        "Quality_Assessment", "Validation_Evidence"
    ]
    ws1.append(headers1)
    
    deliverables = [
        # Phase 0: Foundations (Days 1-10 audit)
        ("DEL-001", "Phase 0", "Assignment_Requirement_Matrix.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: 30 requirements mapped with WBS and evaluation", "Inspected on disk; styled with openpyxl"),
        ("DEL-002", "Phase 0", "Dataset_Inspection_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "Rigorous: Profiling of clean/messy data, schemas, nulls, FKs", "Inspected on disk; references 1,000 users and 35k events"),
        ("DEL-003", "Phase 0", "Source_Verification_Register.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: 20 facts classified as Confirmed/Proposed/Simulated", "Inspected on disk; complies with Sec 6"),
        ("DEL-004", "Phase 0", "Product_Feature_Inventory.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: 20 features mapped across areas, currencies, risks", "Inspected on disk; complies with Sec 5"),
        ("DEL-005", "Phase 0", "Product_Data_Readiness_Audit.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: 22 modules audited across actions, outcomes, scores", "Inspected on disk; complies with WP A"),
        ("DEL-006", "Phase 0", "Data_Coverage_Matrix.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: Standardized event taxonomy with 28 detailed mappings", "Inspected on disk; complies with WP A4"),
        ("DEL-007", "Phase 0", "Analytics_Gap_Assessment.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "Exceeds requirement: 15 critical gaps prioritized with remediation plans", "Inspected on disk; complies with WP R"),
        ("DEL-008", "Phase 0", "Product_Data_Readiness_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "High quality: Executive scorecard, area breakdowns, gap deep-dives", "Inspected on disk; includes Mermaid diagrams"),
        ("DEL-009", "Phase 0", "User_Analytics_Specification.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: ID regexes, 30 profile fields, 6 lifecycle states, funnels", "Inspected on disk; complies with WP B"),
        ("DEL-010", "Phase 0", "User_Account_Analytics_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "High quality: Telemetry contracts, JSON payloads, baseline stats", "Inspected on disk; includes lifecycle state diagrams"),
        ("DEL-011", "Phase 0", "Earning_Reward_Analytics_Specification.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: Decoupled rewards ledger, 5 failure reasons, KPIs", "Inspected on disk; complies with WP C"),
        ("DEL-012", "Phase 0", "Reward_Lifecycle_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "High quality: 10-stage task lifecycle, third-party dependency analysis", "Inspected on disk; empirical failure distributions"),
        ("DEL-013", "Phase 0", "Wallet_Analytics_Specification.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: Double-entry ledger, 11 transaction types, delta checks", "Inspected on disk; complies with WP D"),
        ("DEL-014", "Phase 0", "Withdrawal_Analytics_Specification.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: 5-stage payout pipeline, 4 rails (UPI/PayPal), failure codes", "Inspected on disk; complies with WP D"),
        ("DEL-015", "Phase 0", "Wallet_Withdrawal_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "High quality: Explicit notice of missing data; mathematical invariants", "Inspected on disk; zero fabrication guarantee"),
        ("DEL-016", "Phase 0", "Python Profiling Modules (7 scripts)", "Python", "src/*.py", "Completed and validated", True, "Modular: data_loader, inspector, missing, duplicate, summary, val, utils", "15 unit tests passing in tests/"),
        ("DEL-017", "Phase 0", "01_data_profiling.ipynb", "Jupyter", "notebooks/", "Completed and validated", True, "Executed: 15 code cells with rich table outputs and limitations", "JSON verified; all outputs populated in-place"),
        ("DEL-018", "Phase 0", "SQL Foundation Scripts (3 files)", "SQL", "sql/*.sql", "Completed and validated", True, "Production quality: DDL with verified vs proposed, 15 DQ tests, 10 queries", "Syntax verified; ANSI / PostgreSQL compliant"),
        ("DEL-019", "Phase 0", "First_10_Days_Completion_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "Comprehensive: Addresses all 15 required sections with evidence links", "Inspected on disk; verified complete"),
        ("DEL-020", "Phase 0", "Remaining_Work_Status.xlsx", "Excel", "documentation/ & root", "In progress", True, "This deliverable: Comprehensive audit and traceability matrix", "Currently being generated"),
        
        # Phase 1: Days 11-12 (Referral & Engagement Analytics)
        ("DEL-021", "Phase 1", "Referral_Analytics_Specification.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: 11 lifecycle stages, schema specs, fraud rules, viral KPIs", "Inspected on disk; styled with openpyxl"),
        ("DEL-022", "Phase 1", "Engagement_Analytics_Specification.xlsx", "Excel", "documentation/ & root", "Completed and validated", True, "High quality: DAU/WAU/MAU taxonomy, 15 feature adoption stats, stickiness", "Inspected on disk; styled with openpyxl"),
        ("DEL-023", "Phase 1", "Referral_Engagement_Report.md", "Markdown", "reports/ & root", "Completed and validated", True, "Comprehensive: Viral loops, anti-fraud guardrails, empirical baselines", "Inspected on disk; includes Mermaid diagrams"),
        
        # Phase 2: Days 13-15 (Event Tracking Plan)
        ("DEL-024", "Phase 2", "Event_Tracking_Plan.xlsx", "Excel", "documentation/ & root", "Not started", False, "At least 25 standardized event definitions across 12 product areas", "Pending Phase 2 execution"),
        
        # Phase 3: Days 16-18 (Data Dictionary & Data Model)
        ("DEL-025", "Phase 3", "Data_Dictionary.xlsx", "Excel", "reports/ & documentation/", "Not started", False, "At least 75 standardized fields across 11 entities with validation", "Pending Phase 3 execution"),
        ("DEL-026", "Phase 3", "Data_Model_Documentation.md", "Markdown", "documentation/", "Not started", False, "Relational 3NF & dimensional model documentation", "Pending Phase 3 execution"),
        ("DEL-027", "Phase 3", "Entity_Relationship_Diagram.mmd", "Mermaid", "documentation/", "Not started", False, "Mermaid ER diagram text definition", "Pending Phase 3 execution"),
        ("DEL-028", "Phase 3", "Entity_Relationship_Diagram.png", "Image", "documentation/", "Not started", False, "Visual ER diagram render", "Pending Phase 3 execution"),
        ("DEL-029", "Phase 3", "Proposed_Database_Schema.sql", "SQL", "sql/", "Not started", False, "Full dimensional and relational DDL schema", "Pending Phase 3 execution"),
        
        # Phase 4: Days 19-21 (KPI Catalogue)
        ("DEL-030", "Phase 4", "KPI_Catalogue.xlsx", "Excel", "reports/ & documentation/", "Not started", False, "At least 30 standardized KPIs across 9 categories with SQL formulas", "Pending Phase 4 execution"),
        
        # Phase 5: Days 22-24 (Data Profiling & Data Quality Audit)
        ("DEL-031", "Phase 5", "Complete_Data_Profiling_Report.md", "Markdown", "reports/", "Not started", False, "Comprehensive profiling report incorporating all cleaned data", "Pending Phase 5 execution"),
        ("DEL-032", "Phase 5", "Data_Quality_Audit.xlsx", "Excel", "reports/ & documentation/", "Not started", False, "Exhaustive audit register of all anomalies and messy injections", "Pending Phase 5 execution"),
        ("DEL-033", "Phase 5", "Data_Quality_Findings.md", "Markdown", "reports/", "Not started", False, "Root cause analysis of all data quality defects", "Pending Phase 5 execution"),
        ("DEL-034", "Phase 5", "Data_Quality_Test_Cases.xlsx", "Excel", "documentation/", "Not started", False, "Formal test case catalog for data quality test suites", "Pending Phase 5 execution"),
        ("DEL-035", "Phase 5", "src/data_quality_rules.py", "Python", "src/", "Not started", False, "Automated data quality assertion functions", "Pending Phase 5 execution"),
        ("DEL-036", "Phase 5", "tests/test_data_quality.py", "Python", "tests/", "Not started", False, "Pytest suite for data quality assertion tests", "Pending Phase 5 execution"),
        
        # Phase 6: Data Quality Control Framework
        ("DEL-037", "Phase 6", "Data_Quality_Control_Framework.xlsx", "Excel", "documentation/", "Not started", False, "5-level control framework (App, Collection, Storage, Transform, BI)", "Pending Phase 6 execution"),
        ("DEL-038", "Phase 6", "Data_Quality_Control_Report.md", "Markdown", "reports/", "Not started", False, "Practical data governance implementation report", "Pending Phase 6 execution"),
        
        # Phase 7: Power BI Dashboards
        ("DEL-039", "Phase 7", "VELOOP_Complete_Analytics_Dashboard.pbix", "Power BI", "powerbi/", "Not started", False, "Complete Power BI report with 7 dedicated pages", "Power BI Desktop verified on machine"),
        ("DEL-040", "Phase 7", "PowerBI_DAX_Measures.xlsx", "Excel", "powerbi/", "Not started", False, "Catalogue of all DAX measures with formulas and validation", "Pending Phase 7 execution"),
        ("DEL-041", "Phase 7", "PowerBI_Data_Model_Documentation.md", "Markdown", "powerbi/", "Not started", False, "Star schema, relationships, hierarchies documentation", "Pending Phase 7 execution"),
        ("DEL-042", "Phase 7", "Dashboard_Blueprint.xlsx", "Excel", "powerbi/", "Not started", False, "Layout wireframes, slicers, visual specs for all 7 pages", "Pending Phase 7 execution"),
        ("DEL-043", "Phase 7", "Dashboard_Validation_Report.md", "Markdown", "powerbi/", "Not started", False, "Validation of dashboard measures against raw source figures", "Pending Phase 7 execution"),
        
        # Phase 8: Developer Analytics Handoff
        ("DEL-044", "Phase 8", "Developer_Analytics_Handoff.xlsx", "Excel", "documentation/", "Not started", False, "Developer implementation matrix for all proposed events", "Pending Phase 8 execution"),
        ("DEL-045", "Phase 8", "Developer_Analytics_Handoff.md", "Markdown", "documentation/", "Not started", False, "Engineering specification with payloads, acceptance criteria", "Pending Phase 8 execution"),
        
        # Phase 9: Data Pipeline & Operating Model
        ("DEL-046", "Phase 9", "Data_Pipeline_Architecture.md", "Markdown", "documentation/", "Not started", False, "End-to-end architecture (Collection -> Storage -> DW -> Power BI)", "Pending Phase 9 execution"),
        ("DEL-047", "Phase 9", "Data_Pipeline_Diagram.mmd", "Mermaid", "documentation/", "Not started", False, "Mermaid pipeline flow diagram", "Pending Phase 9 execution"),
        ("DEL-048", "Phase 9", "Data_Pipeline_Diagram.png", "Image", "documentation/", "Not started", False, "Pipeline visual render", "Pending Phase 9 execution"),
        ("DEL-049", "Phase 9", "Data_Operating_Model.xlsx", "Excel", "documentation/", "Not started", False, "RACI matrix, refresh frequencies, backup, monitoring", "Pending Phase 9 execution"),
        
        # Phase 10: Data Access, Privacy & Governance
        ("DEL-050", "Phase 10", "Data_Governance_Framework.xlsx", "Excel", "documentation/", "Not started", False, "RBAC, data classification, minimization, retention policies", "Pending Phase 10 execution"),
        ("DEL-051", "Phase 10", "Data_Privacy_and_Access_Report.md", "Markdown", "documentation/", "Not started", False, "Compliance report (DPDP Act, GDPR, sanitization)", "Pending Phase 10 execution"),
        
        # Phase 11: Analytics Change Management
        ("DEL-052", "Phase 11", "Analytics_Change_Log.xlsx", "Excel", "documentation/", "Not started", False, "Version control for event and KPI definition changes", "Pending Phase 11 execution"),
        
        # Phase 12: Readiness Scorecard & Implementation Backlog
        ("DEL-053", "Phase 12", "VELOOP_Data_Readiness_Scorecard.xlsx", "Excel", "reports/ & documentation/", "Not started", False, "14-area readiness evaluation with evidence", "Pending Phase 12 execution"),
        ("DEL-054", "Phase 12", "Analytics_Implementation_Backlog.xlsx", "Excel", "reports/ & documentation/", "Not started", False, "Prioritized Jira-style development backlog with owner roles", "Pending Phase 12 execution"),
        ("DEL-055", "Phase 12", "Analytics_Gap_Assessment_Final.xlsx", "Excel", "documentation/", "Not started", False, "Final reconciled gap assessment with resolution roadmap", "Pending Phase 12 execution"),
        
        # Phase 13: Final Consolidated Report
        ("DEL-056", "Phase 13", "Final_VELOOP_Analytics_Blueprint.md", "Markdown", "reports/", "Not started", False, "Master executive document addressing all 29 final report sections", "Pending Phase 13 execution"),
        ("DEL-057", "Phase 13", "Final_VELOOP_Analytics_Blueprint.pdf", "PDF", "reports/", "Not started", False, "Professionally styled PDF export of the master blueprint", "Pending Phase 13 execution"),
    ]
    
    for row in deliverables:
        ws1.append(row)
        
    # ----------------------------------------------------
    # Sheet 2: Assignment_Traceability_Matrix
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="Assignment_Traceability_Matrix")
    headers2 = [
        "Req_ID", "Assignment_Section", "Section_Title",
        "Official_PDF_Requirement", "Target_Deliverable_Files",
        "Implementation_Phase", "Audit_Status", "Verification_Evidence"
    ]
    ws2.append(headers2)
    
    trace_rows = [
        ("TRC-001", "Section 2", "Important Data Authenticity Policy", "Must never describe simulated data as actual VELOOP stats, earnings, revenue, retention", "Dataset_Inspection_Report.md, First_10_Days_Completion_Report.md, README.md", "Phase 0 (Days 1-2)", "Completed and validated", "Explicit authenticity banners on all markdown reports and scripts"),
        ("TRC-002", "Section 5", "Product Context", "Understand VELOOP ecosystem: VEs, XP, Gems, Tokens, Spins, tasks, wallet, withdrawals", "Product_Feature_Inventory.xlsx, Days_01_02_Assignment_and_Data_Understanding.md", "Phase 0 (Days 1-2)", "Completed and validated", "20 features and 5 currencies mapped and catalogued"),
        ("TRC-003", "Section 6", "Source & Evidence Discipline", "Maintain Source & Verification Register: Confirmed, Proposed, To Be Verified, Simulated", "Source_Verification_Register.xlsx", "Phase 0 (Days 1-2)", "Completed and validated", "20 audited items with verification notes and dates"),
        ("TRC-004", "Section 7 (WP A)", "Product Data Readiness Audit", "Map product areas, features, user actions, system actions, business questions, 10+ gaps", "Product_Data_Readiness_Audit.xlsx, Data_Coverage_Matrix.xlsx, Analytics_Gap_Assessment.xlsx, Product_Data_Readiness_Report.md", "Phase 0 (Days 3-4)", "Completed and validated", "22 modules audited, 15 critical gaps documented"),
        ("TRC-005", "Section 8 (WP B)", "User & Account Analytics", "Define stable user ID, session ID, registration, login, onboarding, lifecycle state machine", "User_Analytics_Specification.xlsx, User_Account_Analytics_Report.md", "Phase 0 (Days 5-6)", "Completed and validated", "Regex standards, 30 profile fields, 6 lifecycle states"),
        ("TRC-006", "Section 9 (WP C)", "Earning & Reward Analytics", "Task discovery, start, completion, validation, pending, credited, reversed; failure reasons", "Earning_Reward_Analytics_Specification.xlsx, Reward_Lifecycle_Report.md", "Phase 0 (Days 7-8)", "Completed and validated", "Decoupled rewards ledger, 5 empirical failure modes, RRR KPI"),
        ("TRC-007", "Section 10 (WP D)", "Wallet & Withdrawal Analytics", "Wallet transaction model, double-entry, withdrawal lifecycle, failure codes, AML rules", "Wallet_Analytics_Specification.xlsx, Withdrawal_Analytics_Specification.xlsx, Wallet_Withdrawal_Report.md", "Phase 0 (Days 9-10)", "Completed and validated", "Double-entry schema, 5-stage payout pipeline, rails (UPI/PayPal)"),
        ("TRC-008", "Section 11 (WP E)", "Referral & Engagement Analytics", "Referral creation, sharing, clicks, conversion, rewards, invalid referrals; DAU/WAU/MAU", "Referral_Analytics_Specification.xlsx, Engagement_Analytics_Specification.xlsx, Referral_Engagement_Report.md", "Phase 1 (Days 11-12)", "Completed and validated", "11 lifecycle stages, anti-fraud rules, DAU/WAU/MAU taxonomy"),
        ("TRC-009", "Section 12 (WP F)", "Production Event Tracking Plan", "At least 25 meaningful events with naming standards, properties, data types, acceptance criteria", "Event_Tracking_Plan.xlsx", "Phase 2 (Days 13-15)", "Not started", "Scheduled for Phase 2"),
        ("TRC-010", "Section 13 (WP G)", "VELOP Data Dictionary", "At least 75 meaningful fields covering 11 entities with validation rules and analytical uses", "Data_Dictionary.xlsx", "Phase 3 (Days 16-18)", "Not started", "Scheduled for Phase 3"),
        ("TRC-011", "Section 14 (WP H)", "Logical Data Model", "Relational model, ER diagram, primary/foreign keys, 1:1, 1:N, M:N relationships, constraints", "Data_Model_Documentation.md, Entity_Relationship_Diagram.mmd, Proposed_Database_Schema.sql", "Phase 3 (Days 16-18)", "Not started", "Scheduled for Phase 3"),
        ("TRC-012", "Section 15 (WP I)", "KPI Catalogue", "At least 30 meaningful KPIs across 9 categories with exact formulas, required fields, sources", "KPI_Catalogue.xlsx", "Phase 4 (Days 19-21)", "Not started", "Scheduled for Phase 4"),
        ("TRC-013", "Section 16 (WP J)", "Simulated Data Profiling", "Profiling summaries, schema, nulls, duplicates, potential IDs, date fields, limitations", "01_data_profiling.ipynb, Complete_Data_Profiling_Report.md", "Phase 5 (Days 22-24)", "Partially Complete (Foundation Executed)", "Foundation executed in 01_data_profiling.ipynb; full report in Phase 5"),
        ("TRC-014", "Section 17 (WP K)", "Data Quality Audit", "Inspect missing values, duplicates, invalid timestamps, capitalization, orphan records, diffs", "Data_Quality_Audit.xlsx, Data_Quality_Findings.md, tests/test_data_quality.py", "Phase 5 (Days 22-24)", "Not started", "Scheduled for Phase 5"),
        ("TRC-015", "Section 18 (WP L)", "Data Quality Control Framework", "5-level control framework: App entry, event collection, raw storage, transform, BI", "Data_Quality_Control_Framework.xlsx, Data_Quality_Control_Report.md", "Phase 6", "Not started", "Scheduled for Phase 6"),
        ("TRC-016", "Section 19 (WP M)", "Analytics Dashboard Blueprint", "7 Power BI dashboards (Executive, User, Engagement, Reward, Wallet, Withdrawal, Referral)", "powerbi/*.pbix, PowerBI_DAX_Measures.xlsx, Dashboard_Blueprint.xlsx, Dashboard_Validation_Report.md", "Phase 7", "Not started", "Power BI Desktop verified on system; Scheduled for Phase 7"),
        ("TRC-017", "Section 20 (WP N)", "Developer Analytics Handoff", "Engineering specifications for event payloads, triggers, deduplication, acceptance criteria", "Developer_Analytics_Handoff.xlsx, Developer_Analytics_Handoff.md", "Phase 8", "Not started", "Scheduled for Phase 8"),
        ("TRC-018", "Section 21 (WP O)", "Data Pipeline & Operating Model", "Pipeline architecture diagram, producers, storage, validation, transformation, monitoring, RACI", "Data_Pipeline_Architecture.md, Data_Pipeline_Diagram.mmd, Data_Operating_Model.xlsx", "Phase 9", "Not started", "Scheduled for Phase 9"),
        ("TRC-019", "Section 22 (WP P)", "Data Access, Privacy & Governance", "RBAC, data classification, PII protection, data minimization, retention, deletion, audit logs", "Data_Governance_Framework.xlsx, Data_Privacy_and_Access_Report.md", "Phase 10", "Not started", "Scheduled for Phase 10"),
        ("TRC-020", "Section 23 (WP Q)", "Analytics Change Management", "Change log tracking version changes to events, KPIs, dashboards, reasons, approvals", "Analytics_Change_Log.xlsx", "Phase 11", "Not started", "Scheduled for Phase 11"),
        ("TRC-021", "Section 26 & 27", "Final Implementation Backlog & Deliverables", "Prioritized backlog and 21 required final deliverables inventory", "Analytics_Implementation_Backlog.xlsx, VELOOP_Data_Readiness_Scorecard.xlsx", "Phase 12", "Not started", "Scheduled for Phase 12"),
        ("TRC-022", "Section 27 (Deliverable 21)", "Final Consolidated Report", "Comprehensive 29-section executive report with citations, evidence, and recommendations", "reports/Final_VELOOP_Analytics_Blueprint.md, Final_VELOOP_Analytics_Blueprint.pdf", "Phase 13", "Not started", "Scheduled for Phase 13"),
    ]
    
    for row in trace_rows:
        ws2.append(row)
        
    # ----------------------------------------------------
    # Sheet 3: Phase_Execution_Roadmap
    # ----------------------------------------------------
    ws3 = wb.create_sheet(title="Phase_Execution_Roadmap")
    headers3 = [
        "Phase_ID", "Phase_Title", "Target_Work_Days", "Primary_Objective",
        "Key_Deliverables", "Input_Dependencies", "Phase_Status"
    ]
    ws3.append(headers3)
    
    roadmap_rows = [
        ("Phase 0", "Project Audit & Baseline Verification", "Day 10 (Review)", "Audit all first 10 days work; verify Power BI environment; build Remaining_Work_Status.xlsx", "Remaining_Work_Status.xlsx, Test verification logs", "Existing files & PDF", "In progress"),
        ("Phase 1", "Referral & Engagement Analytics", "Days 11-12", "Model referral virality loops and define DAU/WAU/MAU engagement retention metrics", "Referral_Analytics_Specification.xlsx, Engagement_Analytics_Specification.xlsx, Referral_Engagement_Report.md", "Phase 0 Audit", "Completed"),
        ("Phase 2", "Event Tracking Plan", "Days 13-15", "Define 25+ standardized enterprise event schemas across 12 product areas", "Event_Tracking_Plan.xlsx", "Phase 1 Specifications", "Queued"),
        ("Phase 3", "Data Dictionary & Logical Data Model", "Days 16-18", "Standardize 75+ fields and design 3NF / Dimensional ER relational data models", "Data_Dictionary.xlsx, Data_Model_Documentation.md, Entity_Relationship_Diagram.mmd/png, Proposed_Database_Schema.sql", "Phase 2 Event Plan", "Queued"),
        ("Phase 4", "KPI Catalogue", "Days 19-21", "Define 30+ standardized metrics across 9 categories with reproducible SQL formulas", "KPI_Catalogue.xlsx", "Phase 3 Data Model", "Queued"),
        ("Phase 5", "Data Profiling & Quality Audit", "Days 22-24", "Exhaustive anomaly profiling, messy data isolation, automated test suite", "Complete_Data_Profiling_Report.md, Data_Quality_Audit.xlsx, Data_Quality_Findings.md, data_quality_rules.py, test_data_quality.py", "Phase 4 KPI Catalogue", "Queued"),
        ("Phase 6", "Data Quality Control Framework", "Day 24", "Design 5-level operational quality control framework (App, Collection, Storage, Transform, BI)", "Data_Quality_Control_Framework.xlsx, Data_Quality_Control_Report.md", "Phase 5 DQ Audit", "Queued"),
        ("Phase 7", "Power BI Dashboards (High Priority)", "Days 20-22 (Parallel)", "Build 7-page interactive PBIX dashboard, DAX measures catalogue, wireframe blueprint", "VELOOP_Complete_Analytics_Dashboard.pbix, PowerBI_DAX_Measures.xlsx, Dashboard_Blueprint.xlsx, Dashboard_Validation_Report.md", "Phase 3 Model & Phase 4 KPIs", "Queued (Power BI Desktop Verified)"),
        ("Phase 8", "Developer Analytics Handoff", "Day 23", "Translate event tracking plan into testable developer payloads and acceptance criteria", "Developer_Analytics_Handoff.xlsx, Developer_Analytics_Handoff.md", "Phase 2 Event Plan", "Queued"),
        ("Phase 9", "Data Pipeline & Operating Model", "Day 24", "Design ELT pipeline architecture, data flow diagrams, RACI matrix, refresh SLAs", "Data_Pipeline_Architecture.md, Data_Pipeline_Diagram.mmd/png, Data_Operating_Model.xlsx", "Phase 3 Model & Phase 7 BI", "Queued"),
        ("Phase 10", "Data Privacy & Governance", "Day 24", "Define RBAC permissions, PII minimization, retention, deletion, DPDP/GDPR compliance", "Data_Governance_Framework.xlsx, Data_Privacy_and_Access_Report.md", "Phase 3 Data Dictionary", "Queued"),
        ("Phase 11", "Analytics Change Management", "Day 25", "Establish change management protocols and historical/future analytics change log", "Analytics_Change_Log.xlsx", "All previous phases", "Queued"),
        ("Phase 12", "Readiness Scorecard & Implementation Backlog", "Day 25", "Evaluate 14-area readiness scorecard and prioritize development backlog", "VELOOP_Data_Readiness_Scorecard.xlsx, Analytics_Implementation_Backlog.xlsx, Analytics_Gap_Assessment_Final.xlsx", "Phases 1-11", "Queued"),
        ("Phase 13", "Final Consolidated Report", "Day 25", "Author master 29-section executive blueprint consolidating all project evidence", "Final_VELOOP_Analytics_Blueprint.md, Final_VELOOP_Analytics_Blueprint.pdf", "All Phases (0-12)", "Queued"),
    ]
    
    for row in roadmap_rows:
        ws3.append(row)
        
    doc_path = base_dir / "documentation" / "Remaining_Work_Status.xlsx"
    root_path = base_dir / "Remaining_Work_Status.xlsx"
    save_styled_workbook(wb, doc_path)
    wb.save(root_path)
    print(f"Saved: {root_path}")

if __name__ == "__main__":
    print("Generating Phase 0 Deliverable: Remaining_Work_Status.xlsx...")
    create_remaining_work_status()
    print("Remaining_Work_Status.xlsx created successfully!")
