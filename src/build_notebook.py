"""
Script to build notebooks/01_data_profiling.ipynb
"""

import nbformat as nbf
from pathlib import Path

nb = nbf.v4.new_notebook()

cells = []

# Cell 1: Title & Context (Markdown)
cells.append(nbf.v4.new_markdown_cell("""# VELOOP Rewards — Comprehensive Data Profiling Foundation
**Author:** Senior Data Analyst & Product Analytics Mentor  
**Project:** VELOOP Rewards Data Analyst Internship (Task 01)  
**Execution Scope:** Days 1–10 Engineering Foundation  
**Target Work Period:** 27 October 2026 – 05 November 2026  

---
### Mandatory Data Authenticity Policy Notice
All datasets analyzed in this notebook are **synthetic and simulated**. In compliance with assignment Section 2 and Section 34, none of the metrics, user counts, task counts, or percentages calculated herein represent actual VELOOP company statistics, real user behavior, or commercial revenue.

### Notebook Objectives:
1. Load all supplied datasets from raw Excel storage safely into memory.
2. Inspect schemas, column counts, record counts, and data types.
3. Validate candidate primary keys and test cross-table referential integrity.
4. Analyze missing value distributions and assess domain-specific business logic validity.
5. Profile duplicate records and isolate anomalies injected into the messy audit packs.
6. Analyze temporal date spans and chronological sequencing.
7. Execute business validation rules via `DataValidator`.
8. Document all unavailable datasets and analytical limitations explicitly without fabricating results.
"""))

# Cell 2: Setup and Imports (Code)
cells.append(nbf.v4.new_code_cell("""import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to python path for modular import
notebook_dir = Path.cwd()
src_dir = notebook_dir.parent / "src" if (notebook_dir.parent / "src").exists() else notebook_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from data_loader import DataLoader
from dataset_inspector import DatasetInspector
from missing_value_analysis import MissingValueAnalyzer
from duplicate_analysis import DuplicateAnalyzer
from column_summary import ColumnSummaryAnalyzer
from data_validation import DataValidator
from report_utils import ReportUtils

print(f"Environment initialized. Pandas version: {pd.__version__}")
"""))

# Cell 3: Data Loading (Code)
cells.append(nbf.v4.new_code_cell("""# Initialize DataLoader
raw_dir = notebook_dir.parent / "data" / "raw" if (notebook_dir.parent / "data" / "raw").exists() else notebook_dir / "data" / "raw"
loader = DataLoader(raw_data_dir=raw_dir)

# Load core clean datasets
datasets = loader.load_all_clean_datasets()

# Load audit / messy datasets
users_messy = loader.load_users_messy()
events_messy = loader.load_event_messy_audit()

print("Successfully loaded datasets:")
for name, df in datasets.items():
    print(f"  - {name}: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"  - users_messy: {users_messy.shape[0]:,} rows x {users_messy.shape[1]} columns")
print(f"  - events_messy: {events_messy.shape[0]:,} rows x {events_messy.shape[1]} columns")
"""))

# Cell 4: Section 1 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 1. Dataset Dimensions & Memory Footprint Overview
Examine the high-level metrics for all loaded tables.
"""))

# Cell 5: Basic Info (Code)
cells.append(nbf.v4.new_code_cell("""summary_records = []
for name, df in datasets.items():
    inspector = DatasetInspector(df, dataset_name=name)
    info = inspector.get_basic_info()
    summary_records.append(info)

summary_df = pd.DataFrame(summary_records)
summary_df
"""))

# Cell 6: Section 2 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 2. Schema Inspection & Data Types Profile
Inspect column types, null counts, null percentages, and unique values for each core table.
"""))

# Cell 7: Schema Profile (Code)
cells.append(nbf.v4.new_code_cell("""# Inspect Users Clean schema
users_inspector = DatasetInspector(datasets['users'], dataset_name='users')
users_schema = users_inspector.inspect_columns()
print("=== USERS CLEAN SCHEMA PROFILE ===")
users_schema
"""))

# Cell 8: Sessions & Events Schema Profile (Code)
cells.append(nbf.v4.new_code_cell("""# Inspect Sessions & Feature Events schema
sessions_inspector = DatasetInspector(datasets['sessions'], dataset_name='sessions')
print("=== SESSIONS SCHEMA PROFILE ===")
display(sessions_inspector.inspect_columns())

events_inspector = DatasetInspector(datasets['feature_events'], dataset_name='feature_events')
print("=== FEATURE EVENTS SCHEMA PROFILE ===")
display(events_inspector.inspect_columns())
"""))

# Cell 9: Task Activity Schema Profile (Code)
cells.append(nbf.v4.new_code_cell("""# Inspect Task Activity schema
tasks_inspector = DatasetInspector(datasets['task_activity'], dataset_name='task_activity')
print("=== TASK ACTIVITY SCHEMA PROFILE ===")
tasks_inspector.inspect_columns()
"""))

# Cell 10: Section 3 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 3. Primary Key Candidate Identification
Verify which columns meet the mathematical requirements of a Primary Key: **Zero Nulls** and **100% Uniqueness**.
"""))

# Cell 11: PK Candidate Evaluation (Code)
cells.append(nbf.v4.new_code_cell("""for name, df in datasets.items():
    inspector = DatasetInspector(df, dataset_name=name)
    candidates = inspector.identify_potential_primary_keys()
    print(f"Dataset '{name}': Primary Key Candidate(s) -> {candidates}")
"""))

# Cell 12: Section 4 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 4. Referential Integrity & Foreign Key Linkage
Test relational consistency across entities to detect any orphan records.
"""))

# Cell 13: Referential Integrity Analysis (Code)
cells.append(nbf.v4.new_code_cell("""# Test user_id foreign keys against parent Users table
fk_tests = [
    ("Sessions -> Users", datasets['sessions'], "user_id", datasets['users'], "user_id"),
    ("Feature Events -> Users", datasets['feature_events'], "user_id", datasets['users'], "user_id"),
    ("Daily Activity -> Users", datasets['daily_activity'], "user_id", datasets['users'], "user_id"),
    ("Task Activity -> Users", datasets['task_activity'], "user_id", datasets['users'], "user_id"),
    ("Milestones -> Users", datasets['milestones'], "user_id", datasets['users'], "user_id"),
    ("Feature Events -> Sessions", datasets['feature_events'], "session_id", datasets['sessions'], "session_id"),
    ("Task Activity -> Sessions", datasets['task_activity'], "session_id", datasets['sessions'], "session_id"),
    ("Milestones -> Sessions", datasets['milestones'], "session_id", datasets['sessions'], "session_id"),
]

fk_results = []
for test_name, c_df, c_col, p_df, p_col in fk_tests:
    res = DatasetInspector.check_referential_integrity(c_df, c_col, p_df, p_col, relation_name=test_name)
    fk_results.append({
        "Relation": res["relation_name"],
        "Child Records": res["total_child_records"],
        "Child Distinct": res["distinct_child_values"],
        "Parent Distinct": res["distinct_parent_values"],
        "Orphans Count": res["orphan_distinct_count"],
        "Valid FK": res["is_valid_fk"]
    })

pd.DataFrame(fk_results)
"""))

# Cell 14: Section 5 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 5. Missing Value Profiling & Domain Logic Evaluation
Evaluate columns containing null values and assess whether missingness aligns with expected domain behavior.
"""))

# Cell 15: Missing Value Analysis (Code)
cells.append(nbf.v4.new_code_cell("""for name in ['users', 'sessions', 'task_activity', 'milestones']:
    analyzer = MissingValueAnalyzer(datasets[name], dataset_name=name)
    missing_df = analyzer.summarize_missing()
    if not missing_df.empty:
        print(f"=== MISSING VALUES IN {name.upper()} ===")
        display(missing_df)
"""))

# Cell 16: Conditional Missingness in Tasks (Code)
cells.append(nbf.v4.new_code_cell("""# Analyze conditional missingness of task_completed_at and failure_reason across task_status
task_analyzer = MissingValueAnalyzer(datasets['task_activity'], dataset_name='task_activity')
print("=== MISSING COMPLETION TIMESTAMP BY TASK STATUS ===")
display(task_analyzer.analyze_conditional_missingness('task_status', 'task_completed_at'))

print("=== MISSING FAILURE REASON BY TASK STATUS ===")
display(task_analyzer.analyze_conditional_missingness('task_status', 'failure_reason'))
"""))

# Cell 17: Section 6 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 6. Duplicate Analysis & Clean vs Messy Comparison
Verify full-row duplicates and examine injected anomalies in `Users_Messy_Audit`.
"""))

# Cell 18: Duplicate Analysis Code
cells.append(nbf.v4.new_code_cell("""# Check full-row duplicates across clean tables
for name, df in datasets.items():
    analyzer = DuplicateAnalyzer(df, dataset_name=name)
    dup_res = analyzer.find_full_row_duplicates()
    print(f"Dataset '{name}': {dup_res['duplicate_count']} full duplicates")

# Compare Clean vs Messy Users
dup_analyzer = DuplicateAnalyzer(datasets['users'], dataset_name='users')
comp_res = dup_analyzer.compare_clean_vs_messy(datasets['users'], users_messy, id_col='user_id')
print("\\n=== CLEAN VS MESSY USERS AUDIT COMPARISON ===")
for k, v in comp_res.items():
    print(f"  {k}: {v}")
"""))

# Cell 19: Injected Duplicates Isolation (Code)
cells.append(nbf.v4.new_code_cell("""# Isolate the exact duplicate records in Users_Messy_Audit
messy_dup_analyzer = DuplicateAnalyzer(users_messy, dataset_name='users_messy')
messy_dups = messy_dup_analyzer.check_key_duplicates(['user_id'])
print(f"Total duplicate user_id records in messy dataset: {messy_dups['duplicate_key_count']}")
messy_dups['sample_duplicate_groups'][['user_id', 'full_name', 'email', 'city', 'age', 'registration_datetime', 'data_environment']].head(10)
"""))

# Cell 20: Section 7 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 7. Temporal & Date Span Profiling
Profile registration timestamps, session start/end, and event activity timelines.
"""))

# Cell 21: Datetime Profiling (Code)
cells.append(nbf.v4.new_code_cell("""for name in ['users', 'sessions', 'feature_events', 'task_activity']:
    col_analyzer = ColumnSummaryAnalyzer(datasets[name], dataset_name=name)
    dt_summary = col_analyzer.summarize_datetime_columns()
    if not dt_summary.empty:
        print(f"=== TEMPORAL PROFILE: {name.upper()} ===")
        display(dt_summary)
"""))

# Cell 22: Section 8 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 8. Feature Events & Task Categorical Distributions
Examine distribution of interactions across features, event statuses, and task categories.
"""))

# Cell 23: Feature & Task Distributions (Code)
cells.append(nbf.v4.new_code_cell("""# Feature Events Breakdown
print("=== FEATURE EVENTS BY FEATURE NAME ===")
display(datasets['feature_events']['feature_name'].value_counts().to_frame("Event_Count"))

print("=== FEATURE EVENTS BY EVENT STATUS ===")
display(datasets['feature_events']['event_status'].value_counts().to_frame("Status_Count"))

print("=== TASK ACTIVITY BY CATEGORY & STATUS ===")
task_pivot = pd.crosstab(datasets['task_activity']['task_category'], datasets['task_activity']['task_status'], margins=True)
display(task_pivot)
"""))

# Cell 24: Section 9 Markdown
cells.append(nbf.v4.new_markdown_cell("""## 9. Automated Business Rules & Quality Assertions
Execute automated validation tests across domain models using `DataValidator`.
"""))

# Cell 25: Business Rules Validation (Code)
cells.append(nbf.v4.new_code_cell("""# Run validation rules
user_val = DataValidator.validate_users(datasets['users'])
sess_val = DataValidator.validate_sessions(datasets['sessions'])
task_val = DataValidator.validate_tasks(datasets['task_activity'])

all_validations = user_val + sess_val + task_val
val_df = pd.DataFrame(all_validations)
print("=== BUSINESS RULES VALIDATION SUMMARY ===")
display(val_df[['entity', 'rule', 'passed', 'violations_count', 'severity', 'description']])
"""))

# Cell 26: Section 10 Markdown - Explicit Limitations & Gaps
cells.append(nbf.v4.new_markdown_cell("""## 10. Explicit Analytical Limitations & Missing Data Findings

In strict accordance with the **Mandatory Data Authenticity Policy** (Section 2) and **Non-Negotiable Integrity Rules** (Section 34), we record the following empirical limitations:

1. **Absence of Wallet Transaction Ledger:**
   - In `03_Feature_Events`, the `Wallet` feature is limited exclusively to `wallet_viewed` (2,172 events).
   - Zero financial credit, debit, or balance ledger records exist in the provided dataset pack.
   - Consequently, wallet velocity, balance liability, and currency exchange volume cannot be calculated from empirical data and must not be fabricated.

2. **Absence of Dedicated Withdrawals Dataset:**
   - The ~1,200 withdrawal records anticipated in Section 28 are missing from the raw files.
   - Payout requests, gateway fulfillment latency, payment rail fees, and cashout retention cannot be analyzed empirically.

3. **Coupled Task-Reward Logging:**
   - In `05_Task_Activity`, column `reward_status` simply records `'Credited'`, `'Not Credited'`, or `'Pending'`.
   - The exact currency quantum, currency type (VE, XP, Gem, Token), and ledger transaction IDs are absent from the raw operational task records.

4. **Missing Relational Referral Graph:**
   - While `referral_code` and `referral_source_detail` exist in `Users_1000_Clean`, there is no directed edge table linking referrer to referee.
   - Viral K-factor and multi-tier network loops cannot be calculated without the edge dataset.

5. **Lack of Granular Auth & Funnel Telemetry:**
   - Individual steps during registration and onboarding are not emitted as events in `03_Feature_Events`.
   - Only aggregate profile status flags (`email_verification_status`, `onboarding_status`) exist in the Users profile.

---
### Conclusion
The empirical foundation established in this notebook confirms that VELOOP possesses strong telemetry for core gamification and tasks, but requires significant data infrastructure engineering for financial ledgers, withdrawal pipelines, and funnel tracking before production launch.
"""))

nb.cells = cells

output_path = Path(r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics\notebooks\01_data_profiling.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Jupyter Notebook structure written to: {output_path}")

# Execute cells and populate outputs in-process
import io
import sys
import os
from contextlib import redirect_stdout, redirect_stderr

base_dir = Path(r"D:\VELOOPS_DATA_ANALYTICS\VELOOP-Product-Analytics")
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
os.chdir(str(base_dir))

with open(output_path, "r", encoding="utf-8") as f:
    nb = nbf.read(f, as_version=4)

exec_globals = {"__name__": "__main__"}
exec_count = 1
errors = []

for idx, cell in enumerate(nb.cells):
    if cell.cell_type == "code":
        code = cell.source
        f_out = io.StringIO()
        try:
            with redirect_stdout(f_out), redirect_stderr(f_out):
                exec_globals["display"] = lambda x: print(x)
                exec(code, exec_globals)
            out_str = f_out.getvalue()
            cell.outputs = [nbf.v4.new_output(output_type="stream", name="stdout", text=out_str)] if out_str else []
            cell.execution_count = exec_count
            exec_count += 1
        except Exception as e:
            errors.append((idx, str(e)))
            cell.outputs = [nbf.v4.new_output(output_type="stream", name="stderr", text=str(e))]
            print(f"Cell {idx} error: {e}")

with open(output_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

if errors:
    print(f"Execution completed with {len(errors)} error(s): {errors}")
else:
    print(f"SUCCESS: All {exec_count-1} code cells executed cleanly with 0 errors! Outputs saved in notebook.")

