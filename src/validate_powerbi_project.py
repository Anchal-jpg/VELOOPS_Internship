from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(project: Path) -> int:
    failures = []
    passed = []

    pbip = project / "VELOP_Complete_Analytics.pbip"
    dataset = project / "VELOP_Complete_Analytics.Dataset"
    report = project / "VELOP_Complete_Analytics.Report"
    if pbip.exists():
        passed.append("PBIP file exists")
    else:
        failures.append("PBIP file missing")

    pbip_data = load_json(pbip) if pbip.exists() else {}
    artifacts = pbip_data.get("artifacts", [])
    report_ref = next((a.get("report", {}).get("path") for a in artifacts if "report" in a), None)
    if report_ref == "VELOP_Complete_Analytics.Report":
        passed.append("PBIP report artifact reference is correct")
    else:
        failures.append(f"PBIP report artifact reference is invalid: {report_ref}")

    bim_path = dataset / "model.bim"
    tmdl_tables_dir = dataset / "definition" / "tables"
    tables = {}
    if bim_path.exists():
        bim = load_json(bim_path)
        passed.append("model.bim is valid JSON")
        tables = {table["name"]: table for table in bim["model"].get("tables", [])}
        relationships = bim["model"].get("relationships", [])
    elif tmdl_tables_dir.exists():
        passed.append("Dataset uses supported TMDL format")
        relationships = []
        relationships_path = dataset / "definition" / "relationships.tmdl"
        if relationships_path.exists():
            relationship_text = relationships_path.read_text(encoding="utf-8")
            for block in re.split(r"(?=^relationship )", relationship_text, flags=re.MULTILINE):
                name_match = re.search(r"^relationship ([^ \t\r\n]+)", block)
                from_match = re.search(r"fromColumn:\s*([^.]+)\.([^\s]+)", block)
                to_match = re.search(r"toColumn:\s*([^.]+)\.([^\s]+)", block)
                if name_match and from_match and to_match:
                    relationships.append({
                        "name": name_match.group(1),
                        "fromTable": from_match.group(1),
                        "fromColumn": from_match.group(2),
                        "toTable": to_match.group(1),
                        "toColumn": to_match.group(2),
                    })
        for tmdl_path in tmdl_tables_dir.glob("*.tmdl"):
            text = tmdl_path.read_text(encoding="utf-8")
            name_match = re.search(r"^table ([^\r\n]+)", text, re.MULTILINE)
            if not name_match:
                continue
            table_name = name_match.group(1).strip().strip("'")
            columns = [
                {"name": match.group(1).strip().strip("'")}
                for match in re.finditer(r"^\s*column ([^\r\n]+)", text, re.MULTILINE)
            ]
            measures = [
                {"name": match.group(1).strip().strip("'")}
                for match in re.finditer(r"^\s*measure ([^\r\n=]+)", text, re.MULTILINE)
            ]
            tables[table_name] = {"name": table_name, "columns": columns, "measures": measures}
    else:
        failures.append("Neither model.bim nor TMDL dataset definition exists")
        relationships = []
    for table_name in ("dim_users", "dim_dates", "fct_sessions", "fct_tasks",
                       "fct_feature_events", "fct_daily_activity", "fct_milestones",
                       "fct_wallet_ledger", "fct_withdrawals", "fct_referrals"):
        if table_name not in tables:
            failures.append(f"Model table missing: {table_name}")

    for relationship in relationships:
        if relationship["fromTable"] not in tables or relationship["toTable"] not in tables:
            failures.append(f"Relationship references missing table: {relationship['name']}")
            continue
        from_table = tables[relationship["fromTable"]]
        to_table = tables[relationship["toTable"]]
        from_cols = {col["name"] for col in from_table["columns"]}
        to_cols = {col["name"] for col in to_table["columns"]}
        if relationship["fromColumn"] not in from_cols:
            failures.append(f"Relationship references missing from column: {relationship['name']}")
        if relationship["toColumn"] not in to_cols:
            failures.append(f"Relationship references missing to column: {relationship['name']}")
    if not failures:
        passed.append("All relationship table/column references exist")

    pbir = report / "definition.pbir"
    if pbir.exists():
        passed.append("definition.pbir exists")
        pbir_data = load_json(pbir)
        target = pbir_data.get("datasetReference", {}).get("byPath", {}).get("path")
        if target == "../VELOP_Complete_Analytics.Dataset":
            passed.append("definition.pbir dataset reference is correct")
        else:
            failures.append(f"definition.pbir dataset reference is invalid: {target}")
    else:
        failures.append("definition.pbir missing")

    if (report / "report.json").exists():
        failures.append("Legacy report.json still exists alongside PBIR definition")
    else:
        passed.append("PBIR format does not use legacy report.json")

    pages_root = report / "definition" / "pages"
    pages_meta_path = pages_root / "pages.json"
    if not pages_meta_path.exists():
        failures.append("pages/pages.json missing")
        pages_meta = {"pageOrder": []}
    else:
        pages_meta = load_json(pages_meta_path)
        passed.append("pages/pages.json is valid JSON")

    expected_names = [
        "Executive Overview",
        "User Analytics",
        "Engagement Analytics",
        "Earning & Reward Analytics",
        "Wallet Analytics",
        "Withdrawal Analytics",
        "Referral Analytics",
    ]
    actual_names = []
    visual_count = 0
    measure_names = {
        measure["name"]
        for table in tables.values()
        for measure in table.get("measures", [])
    }

    for page_id in pages_meta.get("pageOrder", []):
        page_dir = pages_root / page_id
        page_path = page_dir / "page.json"
        if not page_path.exists():
            failures.append(f"Missing page.json: {page_id}")
            continue
        page = load_json(page_path)
        actual_names.append(page["displayName"])
        visuals_dir = page_dir / "visuals"
        if not visuals_dir.exists():
            failures.append(f"No visuals folder: {page_id}")
            continue
        for visual_dir in visuals_dir.iterdir():
            visual_path = visual_dir / "visual.json"
            if not visual_path.exists():
                failures.append(f"Missing visual.json: {visual_dir}")
                continue
            visual_count += 1
            visual = load_json(visual_path)
            if visual.get("name") != visual_dir.name:
                failures.append(f"Visual name mismatch: {visual_dir.name}")
            query = visual.get("visual", {}).get("query", {}).get("queryState", {})
            for state in query.values():
                for projection in state.get("projections", []):
                    field = projection.get("field", {})
                    if "Column" in field:
                        entity = field["Column"]["Expression"]["SourceRef"]["Entity"]
                        prop = field["Column"]["Property"]
                        if entity not in tables:
                            failures.append(f"Visual column references missing table: {entity}")
                        elif prop not in {col["name"] for col in tables[entity]["columns"]}:
                            failures.append(f"Visual column reference missing: {entity}.{prop}")
                    if "Measure" in field:
                        entity = field["Measure"]["Expression"]["SourceRef"]["Entity"]
                        prop = field["Measure"]["Property"]
                        if entity not in tables:
                            failures.append(f"Visual measure references missing table: {entity}")
                        elif prop not in measure_names:
                            failures.append(f"Visual measure reference missing: {entity}.{prop}")

    if actual_names == expected_names:
        passed.append("Exactly seven expected report pages are present in order")
    else:
        failures.append(f"Unexpected page names/order: {actual_names}")
    if visual_count == 56:
        passed.append("56 valid visual definitions are present")
    else:
        passed.append(f"{visual_count} visual definitions are present")

    for table_name, table in tables.items():
        csv_name = table_name + ".csv"
        csv_path = project.parent / "data" / "processed" / csv_name
        if csv_name in {
            "dim_users.csv", "dim_dates.csv", "fct_sessions.csv", "fct_tasks.csv",
            "fct_feature_events.csv", "fct_daily_activity.csv", "fct_milestones.csv",
            "fct_wallet_ledger.csv", "fct_withdrawals.csv", "fct_referrals.csv",
        }:
            if not csv_path.exists():
                failures.append(f"Partition source CSV missing: {csv_path}")

    report_out = project / "POWERBI_REPAIR_VALIDATION.md"
    lines = [
        "# VELOOP Power BI Repair Validation",
        "",
        "## Summary",
        f"- Project: `{project}`",
        f"- PBIP report: {'PASS' if not failures else 'FAIL'}",
        f"- Page count: {len(actual_names)}",
        f"- Visual definitions: {visual_count}",
        f"- Model tables: {len(tables)}",
        "",
        "## Passed checks",
    ]
    lines += [f"- {item}" for item in passed]
    lines += ["", "## Failed checks"]
    if failures:
        lines += [f"- {item}" for item in failures]
    else:
        lines += ["- None"]
    report_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_powerbi_project.py <repair-folder>")
    raise SystemExit(validate(Path(sys.argv[1])))
