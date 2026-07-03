from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.maintenance import MaintenanceRecord, MaintenanceStatus


def get_upcoming_and_overdue(db: Session, window_days: int = 30) -> list[MaintenanceRecord]:
    """Computed on read: no scheduler needed for Phase 1/2.

    Rows with scheduled_date in the past are overdue; rows within window_days
    are upcoming. Wired into a live endpoint in Phase 2.
    """
    today = date.today()
    query = (
        select(MaintenanceRecord)
        .filter(MaintenanceRecord.status == MaintenanceStatus.scheduled)
        .filter(MaintenanceRecord.scheduled_date <= today + timedelta(days=window_days))
        .order_by(MaintenanceRecord.scheduled_date.asc())
    )
    return list(db.execute(query).scalars().all())
