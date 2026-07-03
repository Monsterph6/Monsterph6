# Roadmap

## Phase 1 — done
Project scaffold, Docker Compose (db + backend + frontend), full DB schema (all 5 entities),
Auth + RBAC, Departments CRUD, Users CRUD, Equipment CRUD (API + UI), dashboard with a live
maintenance-alerts widget, and an Excel export smoke test.

## Phase 2 — done
CRUD for maintenance/calibration records (`/api/v1/maintenance`), restricted to `admin` +
`technician` (department_staff has read-only access). Marking a record complete
(`POST /maintenance/{id}/complete`) auto-creates the next scheduled record when
`interval_days` is set, using `completed_date + interval_days` — no cron/scheduler involved,
consistent with the computed-on-read philosophy from Phase 1. Dedicated `/maintenance` list
page with equipment/status/type filters, plus a "Lịch bảo trì/hiệu chuẩn" tab on the equipment
detail page scoped to that device. The dashboard alert widget now reuses the same
`get_upcoming_and_overdue` query with equipment names joined in.

## Phase 3 — Borrow/Return Workflow
- Borrow request creation, return confirmation, equipment status transitions while borrowed.
- Overdue-borrow detection reusing the same computed-on-read pattern as Phase 2.
- UI: borrow action from equipment detail, "equipment borrowed by my department" list.

## Phase 4 — Reporting & Polish
- Full report catalog: maintenance/calibration history export, borrow history export,
  filtered by department/date range, in Excel and PDF (`reportlab`).
- Evaluate whether push notifications (email/Zalo/SMS) for overdue maintenance are needed;
  if so, this is when a background scheduler (APScheduler/Celery) gets introduced — the
  pull-based alert query from Phase 2 is intentionally sufficient until then.
- Audit logging if required for compliance.
