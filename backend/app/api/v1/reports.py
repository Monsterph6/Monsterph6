import io
from datetime import date

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.equipment import Equipment

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/equipment/excel", dependencies=[Depends(get_current_user)])
def export_equipment_excel(db: Session = Depends(get_db)):
    """Phase 1 smoke test for the export pipeline; full report catalog
    (maintenance/borrow history, PDF, date-range filters) lands in Phase 4."""
    equipment = db.query(Equipment).order_by(Equipment.id).all()
    df = pd.DataFrame(
        [
            {
                "Mã thiết bị": e.code,
                "Tên thiết bị": e.name,
                "Nhà sản xuất": e.manufacturer,
                "Model": e.model,
                "Vị trí": e.location,
                "Trạng thái": e.status.value,
            }
            for e in equipment
        ]
    )
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Thiết bị")
    buffer.seek(0)

    filename = f"danh_muc_thiet_bi_{date.today().isoformat()}.xlsx"
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
