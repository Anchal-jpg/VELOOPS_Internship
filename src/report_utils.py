"""
VELOOP Product Analytics - Report Utilities Module
Author: VELOOP Senior Data Analyst / Mentor Team
Work Scope: Days 1-10 Foundation
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class ReportUtils:
    """
    Formatting utilities for Markdown reports and professional Excel workbooks.
    """

    # Brand / Professional Color Palette
    PRIMARY_COLOR = "1E3A8A"  # Deep Navy
    SECONDARY_COLOR = "2563EB"  # Royal Blue
    ACCENT_COLOR = "0D9488"  # Teal
    HEADER_FILL = "1E293B"  # Slate Dark
    ZEBRA_FILL = "F8FAFC"  # Light Slate
    BORDER_COLOR = "CBD5E1"  # Light Border Gray

    @staticmethod
    def df_to_markdown_table(df: pd.DataFrame, max_rows: Optional[int] = None) -> str:
        """Convert a pandas DataFrame to a clean GitHub-flavored markdown table."""
        target_df = df.head(max_rows) if max_rows else df
        return target_df.to_markdown(index=False)

    @classmethod
    def apply_excel_styling(
        cls,
        wb: openpyxl.Workbook,
        sheet_name: str,
        title: Optional[str] = None,
        enable_filters: bool = True
    ) -> None:
        """
        Applies corporate design standards to an openpyxl sheet:
        - Navy header with bold white text
        - Clear borders
        - Alternating row fills (zebra)
        - Column auto-width adjustment
        - Freeze panes on header
        - Auto-filters
        """
        if sheet_name not in wb.sheetnames:
            return

        ws = wb[sheet_name]
        ws.views.sheetView[0].showGridLines = True

        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color=cls.HEADER_FILL, end_color=cls.HEADER_FILL, fill_type="solid")
        zebra_fill = PatternFill(start_color=cls.ZEBRA_FILL, end_color=cls.ZEBRA_FILL, fill_type="solid")
        regular_font = Font(name="Calibri", size=10)

        thin_side = Side(border_style="thin", color=cls.BORDER_COLOR)
        cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

        max_row = ws.max_row
        max_col = ws.max_column

        # Style header row (Row 1)
        for col in range(1, max_col + 1):
            cell = ws.cell(row=1, column=col)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = cell_border

        ws.row_dimensions[1].height = 28

        # Style data rows
        for row in range(2, max_row + 1):
            ws.row_dimensions[row].height = 20
            is_zebra = (row % 2 == 0)
            for col in range(1, max_col + 1):
                cell = ws.cell(row=row, column=col)
                cell.font = regular_font
                cell.border = cell_border
                if is_zebra:
                    cell.fill = zebra_fill

                # Basic alignment by value type
                val = cell.value
                if isinstance(val, (int, float)):
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center")

        # Column widths auto-adjustment
        for col in range(1, max_col + 1):
            col_letter = get_column_letter(col)
            max_len = 0
            for row in range(1, max_row + 1):
                val = ws.cell(row=row, column=col).value
                if val is not None:
                    max_len = max(max_len, len(str(val)))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        # Freeze panes on header row
        ws.freeze_panes = "A2"

        # Enable auto-filter
        if enable_filters and max_row > 1:
            ws.auto_filter.ref = f"A1:{get_column_letter(max_col)}{max_row}"

