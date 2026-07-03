# Roadmap

## Phase 1 — done
Project scaffold, Docker Compose (db + backend + frontend), full DB schema (all 5 entities),
Auth + RBAC, Departments CRUD, Users CRUD, Equipment CRUD (API + UI), dashboard with a live
maintenance-alerts widget, and an Excel export smoke test.

## Phase 2 — Maintenance & Calibration Scheduling
- CRUD for maintenance/calibration records (create schedule, mark complete, auto-compute
  `next_due_date` from `interval_days`).
- Wire `app.services.maintenance_service.get_upcoming_and_overdue` into a full alerts page
  (not just the dashboard count).
- UI: maintenance history per device, "record maintenance/calibration event" flow for the
  `technician` role.

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
