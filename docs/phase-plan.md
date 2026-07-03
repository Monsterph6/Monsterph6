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

## Phase 3 — done
Borrow/return workflow (`/api/v1/borrow`), restricted to `admin` + `department_staff`
(`technician` has read-only access). Creating a borrow record requires the equipment to be
`active`, auto-generates a slip code (`PM######`), and flips the equipment to the new
`borrowed` status; returning it (`POST /borrow/{id}/return`) flips it back to `active`.
Overdue-borrow detection reuses the same computed-on-read pattern as Phase 2 (no scheduler).
Dedicated `/borrow` list page with equipment/department/status filters, plus a "Lịch sử
mượn/trả" tab on the equipment detail page. Dashboard gained an overdue-borrow count/alert.

Borrow records follow a standard public-asset borrow-slip shape: `purpose`, `approved_by`,
`condition_on_borrow`, `condition_on_return`, `received_by`, in addition to the borrower
(department, and optionally a specific user) and dates. The UI only exposes department-level
borrowing (not per-user) since listing individual users requires `admin` — see
`app/api/v1/users.py` — which `department_staff` doesn't have; `borrower_user_id` still exists
on the API/model for future use.

**Data-field standardization**: all "mã"/code-style fields (equipment code, department code,
borrow slip code) are normalized to unaccented-uppercase-hyphenated Vietnamese via
`app/core/text_utils.normalize_code`, applied as a Pydantic validator on `Equipment.code` and
`Department.code` (borrow codes are server-generated, already in that shape). Descriptive
free-text fields (names, notes, purpose, condition) intentionally keep full Vietnamese
diacritics for display — normalization only applies to identifiers, not prose.

## Phase 4 — done
Full report catalog covering all three domains, each in both Excel and PDF, gated behind
`GET /reports/{equipment,maintenance,borrow}?format=xlsx|pdf` (any authenticated role — export
is read-only, mirrors the RBAC of the underlying list endpoints):
- **Equipment** (`/reports/equipment`): filter by department/status/category.
- **Maintenance/calibration** (`/reports/maintenance`): filter by department (via equipment),
  date range (`scheduled_date`), record type, status.
- **Borrow/return** (`/reports/borrow`): filter by department (`borrower_department_id`), date
  range (`borrow_date`), status.

`app/services/report_service.py` builds a `pandas.DataFrame` per report (Vietnamese column
headers, empty-list-safe via explicit `columns=`) and hands it to `export_to_excel` (openpyxl)
or `export_to_pdf` (reportlab, landscape A4, `SimpleDocTemplate` + `Table`). PDF text renders
via a bundled DejaVu Sans TTF (`app/assets/fonts/`), registered once with
`pdfmetrics.registerFont` — required because reportlab's built-in fonts don't cover Vietnamese
diacritics and the `python:3.12-slim` Docker base has no system fonts installed. Do not switch
back to a base14 font for Vietnamese-facing PDF output.

Frontend: single `/reports` page with one filter card per report type, "Xuất Excel"/"Xuất PDF"
buttons that fetch as a blob (`responseType: "blob"`) and trigger a browser download via an
`<a download>` element — see `frontend/src/api/reports.ts`. The equipment-report UI only
exposes department/status filters (no category), since equipment categories have no
CRUD/UI anywhere in the app yet — extend that lookup table's UI first if category filtering
becomes a requirement.

## Future ideas (not scheduled)
- Push notifications (email/Zalo/SMS) for overdue maintenance/borrow — would introduce a
  background scheduler (APScheduler/Celery) for the first time; the pull-based alert queries
  from Phase 2/3 are intentionally sufficient until this is explicitly requested.
- Audit logging (who changed what), if required for compliance.
- Equipment category management UI (currently a lookup table with no CRUD surface).
