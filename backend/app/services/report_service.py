import io
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.borrow import BorrowRecord, BorrowStatus
from app.models.equipment import Equipment, EquipmentStatus
from app.models.maintenance import MaintenanceRecord, MaintenanceRecordType, MaintenanceStatus

_FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
_FONT_NAME = "DejaVuSans"
_FONT_NAME_BOLD = "DejaVuSans-Bold"
_fonts_registered = False


def _ensure_fonts_registered() -> None:
    """reportlab's built-in fonts don't cover Vietnamese diacritics, and the slim
    Docker base image has no system fonts installed — bundle + register DejaVu
    Sans once so PDF exports render Vietnamese text correctly everywhere."""
    global _fonts_registered
    if _fonts_registered:
        return
    pdfmetrics.registerFont(TTFont(_FONT_NAME, str(_FONT_DIR / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont(_FONT_NAME_BOLD, str(_FONT_DIR / "DejaVuSans-Bold.ttf")))
    _fonts_registered = True


def get_equipment_for_report(
    db: Session,
    department_id: int | None = None,
    status_filter: EquipmentStatus | None = None,
    category_id: int | None = None,
) -> list[Equipment]:
    query = select(Equipment).options(joinedload(Equipment.department), joinedload(Equipment.category))
    if department_id is not None:
        query = query.filter(Equipment.department_id == department_id)
    if status_filter is not None:
        query = query.filter(Equipment.status == status_filter)
    if category_id is not None:
        query = query.filter(Equipment.category_id == category_id)
    query = query.order_by(Equipment.code)
    return list(db.execute(query).unique().scalars().all())


def get_maintenance_for_report(
    db: Session,
    department_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    record_type: MaintenanceRecordType | None = None,
    status_filter: MaintenanceStatus | None = None,
) -> list[MaintenanceRecord]:
    query = select(MaintenanceRecord).options(joinedload(MaintenanceRecord.equipment))
    if department_id is not None:
        query = query.join(Equipment).filter(Equipment.department_id == department_id)
    if date_from is not None:
        query = query.filter(MaintenanceRecord.scheduled_date >= date_from)
    if date_to is not None:
        query = query.filter(MaintenanceRecord.scheduled_date <= date_to)
    if record_type is not None:
        query = query.filter(MaintenanceRecord.record_type == record_type)
    if status_filter is not None:
        query = query.filter(MaintenanceRecord.status == status_filter)
    query = query.order_by(MaintenanceRecord.scheduled_date.desc())
    return list(db.execute(query).unique().scalars().all())


def get_borrow_for_report(
    db: Session,
    department_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    status_filter: BorrowStatus | None = None,
) -> list[BorrowRecord]:
    query = select(BorrowRecord).options(
        joinedload(BorrowRecord.equipment),
        joinedload(BorrowRecord.borrower_department),
    )
    if department_id is not None:
        query = query.filter(BorrowRecord.borrower_department_id == department_id)
    if date_from is not None:
        query = query.filter(BorrowRecord.borrow_date >= date_from)
    if date_to is not None:
        query = query.filter(BorrowRecord.borrow_date <= date_to)
    if status_filter is not None:
        query = query.filter(BorrowRecord.status == status_filter)
    query = query.order_by(BorrowRecord.borrow_date.desc())
    return list(db.execute(query).unique().scalars().all())


_EQUIPMENT_STATUS_LABELS = {
    EquipmentStatus.active: "Đang hoạt động",
    EquipmentStatus.in_maintenance: "Đang bảo trì",
    EquipmentStatus.borrowed: "Đang được mượn",
    EquipmentStatus.broken: "Hỏng",
    EquipmentStatus.retired: "Ngừng sử dụng",
}
_MAINTENANCE_TYPE_LABELS = {
    MaintenanceRecordType.maintenance: "Bảo trì",
    MaintenanceRecordType.calibration: "Hiệu chuẩn",
}
_MAINTENANCE_STATUS_LABELS = {
    MaintenanceStatus.scheduled: "Sắp tới",
    MaintenanceStatus.completed: "Đã hoàn thành",
    MaintenanceStatus.overdue: "Quá hạn",
    MaintenanceStatus.cancelled: "Đã hủy",
}
_BORROW_STATUS_LABELS = {
    BorrowStatus.borrowed: "Đang mượn",
    BorrowStatus.returned: "Đã trả",
    BorrowStatus.overdue: "Quá hạn trả",
}


_EQUIPMENT_COLUMNS = [
    "Mã thiết bị",
    "Tên thiết bị",
    "Danh mục",
    "Nhà sản xuất",
    "Model",
    "Số seri",
    "Vị trí",
    "Phòng ban quản lý",
    "Trạng thái",
]
_MAINTENANCE_COLUMNS = [
    "Mã thiết bị",
    "Tên thiết bị",
    "Loại",
    "Ngày dự kiến",
    "Ngày hoàn thành",
    "Người thực hiện",
    "Trạng thái",
    "Ghi chú",
]
_BORROW_COLUMNS = [
    "Mã phiếu",
    "Mã thiết bị",
    "Tên thiết bị",
    "Phòng ban mượn",
    "Mục đích mượn",
    "Ngày mượn",
    "Ngày dự kiến trả",
    "Ngày trả thực tế",
    "Trạng thái",
]


def equipment_to_dataframe(items: list[Equipment]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=_EQUIPMENT_COLUMNS)
    return pd.DataFrame(
        [
            {
                "Mã thiết bị": e.code,
                "Tên thiết bị": e.name,
                "Danh mục": e.category.name if e.category else "",
                "Nhà sản xuất": e.manufacturer or "",
                "Model": e.model or "",
                "Số seri": e.serial_number or "",
                "Vị trí": e.location or "",
                "Phòng ban quản lý": e.department.name if e.department else "",
                "Trạng thái": _EQUIPMENT_STATUS_LABELS[e.status],
            }
            for e in items
        ]
    )


def maintenance_to_dataframe(items: list[MaintenanceRecord]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=_MAINTENANCE_COLUMNS)
    return pd.DataFrame(
        [
            {
                "Mã thiết bị": r.equipment.code,
                "Tên thiết bị": r.equipment.name,
                "Loại": _MAINTENANCE_TYPE_LABELS[r.record_type],
                "Ngày dự kiến": r.scheduled_date.isoformat(),
                "Ngày hoàn thành": r.completed_date.isoformat() if r.completed_date else "",
                "Người thực hiện": r.performed_by or "",
                "Trạng thái": _MAINTENANCE_STATUS_LABELS[r.status],
                "Ghi chú": r.notes or "",
            }
            for r in items
        ]
    )


def borrow_to_dataframe(items: list[BorrowRecord]) -> pd.DataFrame:
    if not items:
        return pd.DataFrame(columns=_BORROW_COLUMNS)
    return pd.DataFrame(
        [
            {
                "Mã phiếu": r.code,
                "Mã thiết bị": r.equipment.code,
                "Tên thiết bị": r.equipment.name,
                "Phòng ban mượn": r.borrower_department.name if r.borrower_department else "",
                "Mục đích mượn": r.purpose or "",
                "Ngày mượn": r.borrow_date.isoformat(),
                "Ngày dự kiến trả": r.expected_return_date.isoformat() if r.expected_return_date else "",
                "Ngày trả thực tế": r.actual_return_date.isoformat() if r.actual_return_date else "",
                "Trạng thái": _BORROW_STATUS_LABELS[r.status],
            }
            for r in items
        ]
    )


def export_to_excel(df: pd.DataFrame, sheet_name: str) -> io.BytesIO:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    buffer.seek(0)
    return buffer


def export_to_pdf(df: pd.DataFrame, title: str) -> io.BytesIO:
    _ensure_fonts_registered()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=1 * cm,
        rightMargin=1 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
    )
    title_style = ParagraphStyle("title", fontName=_FONT_NAME_BOLD, fontSize=14, spaceAfter=12)
    cell_style = ParagraphStyle("cell", fontName=_FONT_NAME, fontSize=8, leading=10)
    header_style = ParagraphStyle("header", fontName=_FONT_NAME_BOLD, fontSize=8, leading=10, textColor=colors.white)

    header_row = [Paragraph(str(c), header_style) for c in df.columns]
    data_rows = [[Paragraph(str(v), cell_style) for v in row] for row in df.itertuples(index=False)]
    table = Table([header_row] + data_rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1677ff")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ]
        )
    )

    doc.build([Paragraph(title, title_style), table])
    buffer.seek(0)
    return buffer
