from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"


TABLE_FILES = {
    "dim_dates.csv": "dim_dates.tmdl",
    "dim_users.csv": "dim_users.tmdl",
    "fct_sessions.csv": "fct_sessions.tmdl",
    "fct_tasks.csv": "fct_tasks.tmdl",
    "fct_feature_events.csv": "fct_feature_events.tmdl",
    "fct_daily_activity.csv": "fct_daily_activity.tmdl",
    "fct_milestones.csv": "fct_milestones.tmdl",
    "fct_wallet_ledger.csv": "fct_wallet_ledger.tmdl",
    "fct_withdrawals.csv": "fct_withdrawals.tmdl",
    "fct_referrals.csv": "fct_referrals.tmdl",
}


def m_type(column: str, series: pd.Series) -> str:
    name = column.lower()
    if pd.api.types.is_datetime64_any_dtype(series):
        return "type datetime"
    if "datetime" in name or "timestamp" in name or name.endswith("_date") or name.endswith("_at"):
        return "type datetime"
    if pd.api.types.is_integer_dtype(series):
        return "Int64.Type"
    if pd.api.types.is_float_dtype(series):
        return "type number"
    if pd.api.types.is_bool_dtype(series):
        return "type logical"
    return "type text"


def replace_partition(tmdl_path: Path, csv_path: Path) -> None:
    text = tmdl_path.read_text(encoding="utf-8")
    df = pd.read_csv(csv_path)
    conversions = []
    for column in df.columns:
        conversions.append(f'{{"{column}", {m_type(column, df[column])}}}')
    typed_list = ", ".join(conversions)
    expression = (
        "\tpartition " + tmdl_path.stem + "-Partition = m\n"
        "\t\tmode: import\n"
        "\t\tsource =\n"
        "\t\t\t\tlet\n"
        f'\t\t\t\t    Source = Csv.Document(File.Contents("{csv_path.as_posix()}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n'
        "\t\t\t\t    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n"
        f"\t\t\t\t    TypedColumns = Table.TransformColumnTypes(PromotedHeaders, {{{typed_list}}}, \"en-US\")\n"
        "\t\t\t\tin\n"
        "\t\t\t\t    TypedColumns\n"
    )
    marker = "\tpartition "
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"No partition found in {tmdl_path}")
    text = text[:start] + expression
    tmdl_path.write_text(text.rstrip() + "\n", encoding="utf-8")


def repair(dataset: Path) -> None:
    tables_dir = dataset / "definition" / "tables"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = dataset.parent / f"repaired_tmdl_backup_{stamp}"
    shutil.copytree(dataset, backup)

    for csv_name, tmdl_name in TABLE_FILES.items():
        csv_path = DATA / csv_name
        if not csv_path.exists():
            raise RuntimeError(f"Missing CSV source: {csv_path}")
        tmdl_path = tables_dir / tmdl_name
        if not tmdl_path.exists():
            raise RuntimeError(f"Missing TMDL table: {tmdl_path}")
        replace_partition(tmdl_path, csv_path)

    report = {
        "backup": str(backup),
        "csv_sources": {name: str(DATA / name) for name in TABLE_FILES},
        "tmdl_tables_updated": sorted(TABLE_FILES.values()),
    }
    (dataset.parent / "TMDL_REPAIR_REPORT.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: repair_tmdl_queries.py <Dataset-folder>")
    repair(Path(sys.argv[1]))
