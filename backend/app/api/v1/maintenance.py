from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.database import get_db
from app.services.maintenance_service import get_upcoming_and_overdue
from sqlalchemy.orm import Session

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get("/alerts", dependencies=[Depends(get_current_user)])
def get_alerts(db: Session = Depends(get_db), window_days: int = 30):
    """Phase 2: full scheduling UI/CRUD lands later; the alert query is live now."""
    records = get_upcoming_and_overdue(db, window_days)
    return [
        {
            "id": r.id,
            "equipment_id": r.equipment_id,
            "record_type": r.record_type,
            "scheduled_date": r.scheduled_date,
            "status": r.status,
        }
        for r in records
    ]
