from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.borrow import BorrowStatus
from app.models.equipment import EquipmentStatus
from app.models.maintenance import MaintenanceRecordType, MaintenanceStatus
from app.services.report_service import (
    borrow_to_dataframe,
    equipment_to_dataframe,
    export_to_excel,
    export_to_pdf,
    get_borrow_for_report,
    get_equipment_for_report,
    get_maintenance_for_report,
    maintenance_to_dataframe,
)

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(get_current_user)])

ReportFormat = Literal["xlsx", "pdf"]


def _respond(df, sheet_name: str, title: str, filename_stem: str, format: ReportFormat) -> StreamingResponse:
    if format == "pdf":
        buffer = export_to_pdf(df, title)
        media_type = "application/pdf"
        filename = f"{filename_stem}_{date.today().isoformat()}.pdf"
    else:
        buffer = export_to_excel(df, sheet_name)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"{filename_stem}_{date.today().isoformat()}.xlsx"
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/equipment")
def export_equipment_report(
    db: Session = Depends(get_db),
    format: ReportFormat = "xlsx",
    department_id: int | None = None,
    status_filter: EquipmentStatus | None = Query(None, alias="status"),
    category_id: int | None = None,
):
    items = get_equipment_for_report(db, department_id, status_filter, category_id)
    df = equipment_to_dataframe(items)
    return _respond(df, "Thiết bị", "Danh mục thiết bị", "danh_muc_thiet_bi", format)


@router.get("/maintenance")
def export_maintenance_report(
    db: Session = Depends(get_db),
    format: ReportFormat = "xlsx",
    department_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    record_type: MaintenanceRecordType | None = None,
    status_filter: MaintenanceStatus | None = Query(None, alias="status"),
):
    items = get_maintenance_for_report(db, department_id, date_from, date_to, record_type, status_filter)
    df = maintenance_to_dataframe(items)
    return _respond(df, "Bảo trì - Hiệu chuẩn", "Lịch sử bảo trì/hiệu chuẩn", "lich_su_bao_tri", format)


@router.get("/borrow")
def export_borrow_report(
    db: Session = Depends(get_db),
    format: ReportFormat = "xlsx",
    department_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    status_filter: BorrowStatus | None = Query(None, alias="status"),
):
    items = get_borrow_for_report(db, department_id, date_from, date_to, status_filter)
    df = borrow_to_dataframe(items)
    return _respond(df, "Mượn - Trả", "Lịch sử mượn/trả thiết bị", "lich_su_muon_tra", format)
