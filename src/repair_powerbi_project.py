from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"


def type_for(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_integer_dtype(series):
        return "int64"
    if pd.api.types.is_float_dtype(series):
        return "double"
    if "date" in series.name.lower() or "datetime" in series.name.lower():
        return "dateTime"
    return "string"


def table_from_csv(name: str, csv_path: Path) -> dict:
    df = pd.read_csv(csv_path)
    columns = []
    key_candidates = {
        "dim_users": "user_id",
        "dim_dates": "date_key",
        "fct_sessions": "session_id",
        "fct_tasks": "activity_id",
        "fct_feature_events": "event_id",
        "fct_daily_activity": "activity_date",
        "fct_milestones": "milestone_type",
        "fct_wallet_ledger": "transaction_id",
        "fct_withdrawals": "withdrawal_id",
        "fct_referrals": "referral_id",
    }
    key = key_candidates.get(name)
    for column in df.columns:
        item = {"name": column, "dataType": type_for(df[column]), "sourceColumn": column}
        if column == key:
            item["isKey"] = True
        columns.append(item)
    expression = (
        "let\n"
        f'    Source = Csv.Document(File.Contents("{csv_path.as_posix()}"), '
        '[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n'
        "    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true])\n"
        "in\n"
        "    PromotedHeaders"
    )
    return {
        "name": name,
        "columns": columns,
        "partitions": [{
            "name": f"{name}-Partition",
            "mode": "import",
            "source": {"type": "m", "expression": expression},
        }],
    }


def measure(name: str, expression: str) -> dict:
    return {"name": name, "expression": expression}


def source_ref(entity: str) -> dict:
    return {"SourceRef": {"Entity": entity}}


def column_field(entity: str, prop: str, active: bool = True) -> dict:
    return {
        "field": {
            "Column": {
                "Expression": source_ref(entity),
                "Property": prop,
            }
        },
        "queryRef": f"{entity}.{prop}",
        "active": active,
    }


def measure_field(entity: str, prop: str) -> dict:
    return {
        "field": {
            "Measure": {
                "Expression": source_ref(entity),
                "Property": prop,
            }
        },
        "queryRef": f"{entity}.{prop}",
        "active": True,
    }


def projection_visual(name: str, visual_type: str, x: float, y: float, w: float, h: float,
                     query_state: dict, title: str, z: int = 1000) -> tuple[str, dict]:
    visual_id = name
    visual = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.2.0/schema.json",
        "name": visual_id,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": visual_type,
            "query": {"queryState": query_state},
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "text": {"expr": {"Literal": {"Value": json.dumps(title)}}}
                    }
                }]
            },
        },
    }
    return visual_id, visual


def card_visual(name: str, entity: str, measure_name: str, x: float, y: float,
                w: float = 300, h: float = 90, z: int = 1000) -> dict:
    _, visual = projection_visual(
        name, "card", x, y, w, h,
        {"Values": {"projections": [measure_field(entity, measure_name)]}},
        measure_name, z,
    )
    return visual


def column_visual(name: str, entity: str, category: str, value_entity: str,
                  measure_name: str, x: float, y: float, w: float, h: float, z: int,
                  title: str) -> dict:
    _, visual = projection_visual(
        name, "columnChart", x, y, w, h,
        {
            "Category": {"projections": [column_field(entity, category)]},
            "Y": {"projections": [measure_field(value_entity, measure_name)]},
        },
        title, z,
    )
    return visual


def table_visual(name: str, entity: str, fields: list[tuple[str, str]], x: float, y: float,
                 w: float, h: float, z: int, title: str) -> dict:
    projections = []
    for field_entity, field_name in fields:
        if field_name.startswith("__MEASURE__"):
            projections.append(measure_field(field_entity, field_name.replace("__MEASURE__", "", 1)))
        else:
            projections.append(column_field(field_entity, field_name))
    _, visual = projection_visual(
        name, "table", x, y, w, h,
        {"Values": {"projections": projections}},
        title, z,
    )
    return visual


def slicer_visual(name: str, entity: str, field_name: str, x: float, y: float,
                  w: float, h: float, z: int, title: str) -> dict:
    _, visual = projection_visual(
        name, "slicer", x, y, w, h,
        {"Values": {"projections": [column_field(entity, field_name)]}},
        title, z,
    )
    return visual


def repair(destination: Path) -> None:
    dataset = destination / "VELOP_Complete_Analytics.Dataset"
    report = destination / "VELOP_Complete_Analytics.Report"
    bim_path = dataset / "model.bim"

    bim = json.loads(bim_path.read_text(encoding="utf-8"))
    bim["compatibilityLevel"] = 1550
    bim["model"]["defaultPowerBIDataSourceVersion"] = "powerBI_V3"
    bim["model"]["discourageImplicitMeasures"] = True
    tables = bim["model"]["tables"]

    verified_csv_tables = (
        "dim_dates",
        "dim_users",
        "fct_sessions",
        "fct_tasks",
        "fct_feature_events",
        "fct_daily_activity",
        "fct_milestones",
        "fct_wallet_ledger",
        "fct_withdrawals",
        "fct_referrals",
    )
    rebuilt_tables = {name: table_from_csv(name, DATA / f"{name}.csv") for name in verified_csv_tables}
    tables[:] = [rebuilt_tables.get(table["name"], table) for table in tables]
    for name in verified_csv_tables:
        if name not in {table["name"] for table in tables}:
            tables.append(rebuilt_tables[name])

    table_by_name = {table["name"]: table for table in tables}

    table_by_name["dim_users"]["measures"] = [
        measure("Total Registered Users", "COUNTROWS(dim_users)"),
        measure("Active Users 7D", "COUNTROWS(FILTER(dim_users, dim_users[is_active_7d] = TRUE()))"),
        measure("Active Users 30D", "COUNTROWS(FILTER(dim_users, dim_users[is_active_30d] = TRUE()))"),
        measure("Suspended Accounts", 'CALCULATE(COUNTROWS(dim_users), dim_users[account_status] = "Suspended")'),
        measure("Average User Age", "AVERAGE(dim_users[age])"),
        measure("Circulating XP", "SUM(dim_users[xp_balance])"),
        measure("Referred Signups", "COUNTROWS(FILTER(dim_users, NOT(ISBLANK(dim_users[referral_source_detail]))))"),
        measure("Organic or Unspecified Acquisition", "COUNTROWS(FILTER(dim_users, ISBLANK(dim_users[referral_source_detail])))"),
    ]
    table_by_name["fct_sessions"]["measures"] = [
        measure("Total Recorded Sessions", "COUNTROWS(fct_sessions)"),
        measure("Average Session Duration Seconds", "AVERAGE(fct_sessions[session_duration_seconds])"),
        measure("Average Session Duration Minutes", "DIVIDE([Average Session Duration Seconds], 60)"),
        measure("Distinct Session Users", "DISTINCTCOUNT(fct_sessions[user_id])"),
    ]
    table_by_name["fct_tasks"]["measures"] = [
        measure("Total Task Attempts", "COUNTROWS(fct_tasks)"),
        measure("Completed Tasks", 'CALCULATE(COUNTROWS(fct_tasks), fct_tasks[task_status] = "Completed")'),
        measure("Failed Tasks", 'CALCULATE(COUNTROWS(fct_tasks), fct_tasks[task_status] = "Failed")'),
        measure("Abandoned Tasks", 'CALCULATE(COUNTROWS(fct_tasks), fct_tasks[task_status] = "Abandoned")'),
        measure("Task Completion Rate", 'DIVIDE([Completed Tasks], [Total Task Attempts])'),
    ]
    table_by_name["fct_feature_events"]["measures"] = [
        measure("Total Feature Events", "COUNTROWS(fct_feature_events)"),
        measure("Successful Feature Events", 'CALCULATE(COUNTROWS(fct_feature_events), fct_feature_events[event_status] = "Success")'),
        measure("Feature Event Success Rate", "DIVIDE([Successful Feature Events], [Total Feature Events])"),
    ]
    table_by_name["fct_daily_activity"]["measures"] = [
        measure("Recorded Daily Activity Rows", "COUNTROWS(fct_daily_activity)"),
        measure("Total Recorded Active Flags", "SUM(fct_daily_activity[active_flag])"),
        measure("Total Daily Sessions", "SUM(fct_daily_activity[session_count])"),
        measure("Total Daily Feature Events", "SUM(fct_daily_activity[event_count])"),
    ]
    table_by_name["fct_milestones"]["measures"] = [
        measure("Total Recorded Milestones", "COUNTROWS(fct_milestones)"),
        measure("Distinct Milestone Types", "DISTINCTCOUNT(fct_milestones[milestone_type])"),
    ]
    table_by_name["fct_wallet_ledger"]["measures"] = [
        measure("Ledger Transaction Count", "COUNTROWS(fct_wallet_ledger)"),
        measure("Gross Credited Points", 'CALCULATE(SUM(fct_wallet_ledger[points_amount]), fct_wallet_ledger[direction] = "CREDIT")'),
        measure("Distinct Wallet Users", "DISTINCTCOUNT(fct_wallet_ledger[user_id])"),
    ]
    table_by_name["fct_withdrawals"]["measures"] = [
        measure("Total Withdrawal Requests", "COUNTROWS(fct_withdrawals)"),
        measure("Completed Withdrawals", 'CALCULATE(COUNTROWS(fct_withdrawals), fct_withdrawals[status] = "Completed")'),
        measure("Rejected Withdrawals", 'CALCULATE(COUNTROWS(fct_withdrawals), fct_withdrawals[status] = "Rejected")'),
        measure("Withdrawal Fulfillment Rate", "DIVIDE([Completed Withdrawals], [Total Withdrawal Requests])"),
        measure("Average Turnaround Hours", "AVERAGE(fct_withdrawals[turnaround_time_hours])"),
        measure("Total Redeemed Points", "SUM(fct_withdrawals[points_redeemed])"),
    ]
    table_by_name["fct_referrals"]["measures"] = [
        measure("Referral Records", "COUNTROWS(fct_referrals)"),
        measure("Activated Referral Records", 'CALCULATE(COUNTROWS(fct_referrals), fct_referrals[status] = "Activated")'),
        measure("Referral Points Awarded", "SUM(fct_referrals[reward_points_awarded])"),
    ]

    relationships = bim["model"].setdefault("relationships", [])
    existing_relationship_names = {rel["name"] for rel in relationships}
    additions = [
        ("rel_users_feature_events", "fct_feature_events", "user_id", "dim_users", "user_id"),
        ("rel_users_daily_activity", "fct_daily_activity", "user_id", "dim_users", "user_id"),
        ("rel_users_milestones", "fct_milestones", "user_id", "dim_users", "user_id"),
    ]
    for name, from_table, from_col, to_table, to_col in additions:
        if name not in existing_relationship_names:
            relationships.append({
                "name": name,
                "fromTable": from_table,
                "fromColumn": from_col,
                "toTable": to_table,
                "toColumn": to_col,
            })

    bim_path.write_text(json.dumps(bim, indent=2, ensure_ascii=False), encoding="utf-8")


    # Replace legacy report.json with the enhanced PBIR definition.
    legacy_report = report / "report.json"
    if legacy_report.exists():
        legacy_report.unlink()
    definition = report / "definition"
    if definition.exists():
        shutil.rmtree(definition)
    pages_dir = definition / "pages"
    pages_dir.mkdir(parents=True)

    (definition / "version.json").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0",
    }, indent=2), encoding="utf-8")
    (definition / "report.json").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.2.0/schema.json",
        "themeCollection": {
            "baseTheme": {
                "name": "CY24SU10",
                "reportVersionAtImport": "5.61",
                "type": "SharedResources",
            }
        },
        "layoutOptimization": "None",
        "settings": {
            "useStylableVisualContainerHeader": True,
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True,
        },
    }, indent=2), encoding="utf-8")

    page_specs = [
        ("Executive Overview", [
            ("dim_users", "Total Registered Users"),
            ("dim_users", "Active Users 7D"),
            ("fct_tasks", "Completed Tasks"),
            ("fct_sessions", "Total Recorded Sessions"),
        ], ("fct_tasks", "task_status", "fct_tasks", "Total Task Attempts", "Task Attempts by Status")),
        ("User Analytics", [
            ("dim_users", "Total Registered Users"),
            ("dim_users", "Active Users 30D"),
            ("dim_users", "Suspended Accounts"),
            ("dim_users", "Average User Age"),
        ], ("dim_users", "account_status", "dim_users", "Total Registered Users", "Users by Account Status")),
        ("Engagement Analytics", [
            ("fct_sessions", "Total Recorded Sessions"),
            ("fct_sessions", "Distinct Session Users"),
            ("fct_sessions", "Average Session Duration Minutes"),
            ("fct_feature_events", "Total Feature Events"),
        ], ("fct_feature_events", "feature_name", "fct_feature_events", "Total Feature Events", "Feature Events by Feature")),
        ("Earning & Reward Analytics", [
            ("fct_tasks", "Total Task Attempts"),
            ("fct_tasks", "Completed Tasks"),
            ("fct_tasks", "Task Completion Rate"),
            ("fct_tasks", "Abandoned Tasks"),
        ], ("fct_tasks", "task_category", "fct_tasks", "Completed Tasks", "Completed Tasks by Category")),
        ("Wallet Analytics", [
            ("dim_users", "Circulating XP"),
            ("fct_wallet_ledger", "Ledger Transaction Count"),
            ("fct_wallet_ledger", "Gross Credited Points"),
            ("fct_wallet_ledger", "Distinct Wallet Users"),
        ], ("fct_wallet_ledger", "transaction_type", "fct_wallet_ledger", "Gross Credited Points", "Points by Transaction Type")),
        ("Withdrawal Analytics", [
            ("fct_withdrawals", "Total Withdrawal Requests"),
            ("fct_withdrawals", "Completed Withdrawals"),
            ("fct_withdrawals", "Withdrawal Fulfillment Rate"),
            ("fct_withdrawals", "Average Turnaround Hours"),
        ], ("fct_withdrawals", "status", "fct_withdrawals", "Total Withdrawal Requests", "Withdrawal Requests by Status")),
        ("Referral Analytics", [
            ("fct_referrals", "Referral Records"),
            ("fct_referrals", "Activated Referral Records"),
            ("fct_referrals", "Referral Points Awarded"),
            ("dim_users", "Referred Signups"),
        ], ("fct_referrals", "share_channel", "fct_referrals", "Referral Records", "Referral Records by Channel")),
    ]

    page_ids = [
        "7d30a001000000000001",
        "7d30a002000000000002",
        "7d30a003000000000003",
        "7d30a004000000000004",
        "7d30a005000000000005",
        "7d30a006000000000006",
        "7d30a007000000000007",
    ]
    (pages_dir / "pages.json").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
        "pageOrder": page_ids,
        "activePageName": page_ids[0],
    }, indent=2), encoding="utf-8")

    for index, (title, cards, chart_spec) in enumerate(page_specs):
        page_id = page_ids[index]
        page_dir = pages_dir / page_id
        visuals_dir = page_dir / "visuals"
        visuals_dir.mkdir(parents=True)
        (page_dir / "page.json").write_text(json.dumps({
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.3.0/schema.json",
            "name": page_id,
            "displayName": title,
            "displayOption": "FitToPage",
            "height": 720,
            "width": 1280,
        }, indent=2), encoding="utf-8")

        visuals = []
        # Header uses a text box visual type for a clear page title.
        _, header = projection_visual(
            f"header_{index + 1}", "textbox", 20, 10, 1240, 40,
            {}, title, 900,
        )
        # Add title text; schema-compatible text box fields are left for Desktop to edit.
        header["visual"]["objects"] = {
            "general": [{
                "properties": {
                    "paragraphs": [{
                        "textRuns": [{"value": title, "textStyle": {"fontSize": "16pt", "fontWeight": "bold"}}]
                    }]
                }
            }]
        }
        visuals.append((f"header_{index + 1}", header))

        card_x = [20, 325, 630, 935]
        for card_index, (entity, measure_name) in enumerate(cards):
            card_id = f"{page_id}_card_{card_index + 1}"
            visuals.append((card_id, card_visual(
                card_id, entity, measure_name, card_x[card_index], 65, 280, 95,
                1000 + card_index,
            )))

        chart_entity, chart_category, value_entity, value_measure, chart_title = chart_spec
        chart_id = f"{page_id}_main_chart"
        visuals.append((chart_id, column_visual(
            chart_id, chart_entity, chart_category, value_entity, value_measure,
            20, 180, 780, 470, 1100, chart_title,
        )))

        table_id = f"{page_id}_detail_table"
        table_fields = [
            (chart_entity, chart_category),
            (value_entity, "__MEASURE__" + value_measure),
        ]
        visuals.append((table_id, table_visual(
            table_id, chart_entity, table_fields, 820, 180, 440, 350, 1200,
            "Detail",
        )))

        slicer_id = f"{page_id}_filter"
        slicer_entity = chart_entity
        slicer_field = chart_category
        visuals.append((slicer_id, slicer_visual(
            slicer_id, slicer_entity, slicer_field, 820, 540, 440, 110, 1300,
            "Filter",
        )))

        for visual_id, visual in visuals:
            visual_dir = visuals_dir / visual_id
            visual_dir.mkdir(parents=True)
            (visual_dir / "visual.json").write_text(json.dumps(visual, indent=2), encoding="utf-8")

    (report / "definition.pbir").write_text(json.dumps({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {
            "byPath": {"path": "../VELOP_Complete_Analytics.Dataset"}
        },
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: repair_powerbi_project.py <repair-folder>")
    repair(Path(sys.argv[1]))
