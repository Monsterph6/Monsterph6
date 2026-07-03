# CLAUDE.md

This file guides Claude Code when working in this repository.

## Overview

Web app for managing specialized medical/lab equipment for CDC Hải Phòng (Trung tâm Kiểm soát
bệnh tật Hải Phòng): equipment catalog, maintenance/calibration scheduling, borrow/return
tracking, user management with RBAC, and Excel/PDF reporting. See `docs/phase-plan.md` for the
full feature roadmap. Phase 1 shipped the DB schema for all entities plus full business
logic/UI for Auth, Users, Departments, and Equipment CRUD. Phase 2 (maintenance/calibration
scheduling), Phase 3 (borrow/return), and Phase 4 (Excel/PDF reporting) are also done — all
four planned phases are complete; `docs/phase-plan.md`'s "Future ideas" section lists
unscheduled follow-ups (push notifications, audit logging, category management UI).

## Repository Structure

```
backend/            FastAPI + SQLAlchemy + Alembic + PostgreSQL
  app/
    core/            config.py (Settings), database.py (engine/session), security.py (JWT/bcrypt)
    models/          SQLAlchemy ORM models, one file per aggregate
    schemas/         Pydantic request/response models, mirrors models/
    api/
      deps.py         get_current_user, require_role(*roles) RBAC guard
      v1/             one router file per resource, aggregated in router.py
    services/        business logic (keeps routers thin)
    seed/            seed_data.py creates the initial admin user + sample departments
    assets/fonts/    bundled DejaVu Sans TTF for Vietnamese-capable PDF export (reportlab)
  migrations/        Alembic; migrations/versions/0001_initial_schema.py creates ALL tables
  tests/             pytest, SQLite in-memory DB via dependency override (see tests/conftest.py)
frontend/            React + TypeScript + Vite + Ant Design (antd), separate SPA
  src/
    api/             axios client (client.ts) + one thin wrapper module per resource
    auth/            AuthContext (token in localStorage) + ProtectedRoute (role-gated)
    layouts/         AppLayout (sidebar nav, gated by user.role)
    pages/           one folder per domain, mirrors backend routers 1:1
    types/           TS interfaces hand-mirrored from Pydantic schemas
docs/phase-plan.md   Feature roadmap, all 4 phases done; "Future ideas" section for unscheduled
                     follow-ups — keep this updated as new work lands
docker-compose.yml            production-shaped: db + backend + frontend(nginx)
docker-compose.override.yml   local dev: hot reload, mounted source, exposed ports
```

## Development Setup

See `README.md` for full setup instructions (Docker and manual). Quick reference:

```bash
# Backend
cd backend && pip install -r requirements.txt
alembic upgrade head && python -m app.seed.seed_data
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

Vite proxies `/api` to `localhost:8000` in dev (`frontend/vite.config.ts`); nginx does the same
in production (`frontend/nginx.conf`) so the frontend always calls a same-origin `/api/v1/...`.

## Testing

```bash
cd backend && pytest                  # uses SQLite in-memory, no Postgres needed
cd frontend && npx tsc -b && npm run build
```

When adding a backend endpoint, add a corresponding test in `backend/tests/` using the
`client`/`auth_headers`/`department` fixtures in `tests/conftest.py` — don't stand up a real
Postgres for tests, the SQLite-in-memory + `get_db` dependency override pattern there is the
established convention.

## Code Conventions

- **Backend**: sync SQLAlchemy (not async) — deliberate choice for this scale (~600 devices,
  dozens of users); don't introduce async session handling. Routers stay thin; business logic
  (uniqueness checks, filtering/pagination, computed queries) lives in `app/services/`.
- **RBAC**: enforce with `Depends(require_role(UserRole.admin, ...))` in the router's `@router.get(...)`
  decorator (`dependencies=[...]`) or via `router = APIRouter(..., dependencies=[...])` when an
  entire resource is role-restricted (see `app/api/v1/users.py`). Don't reinvent role checks inline.
- **Migrations**: one Alembic migration per schema change, hand-write revisions (no live Postgres
  in most dev/CI environments to autogenerate against) — mirror the exact column types/constraints
  already defined in `app/models/`.
- **Maintenance/borrow "alerts"**: computed on read via a plain SQL query (see
  `app/services/maintenance_service.get_upcoming_and_overdue` and the equivalent in
  `borrow_service.get_overdue_borrows`), not a background job/cron. Don't add
  Celery/APScheduler unless the requirement changes to push notifications (see
  `docs/phase-plan.md` "Future ideas").
- **PDF export**: always render through the bundled DejaVu Sans font (`app/assets/fonts/`,
  registered in `app/services/report_service._ensure_fonts_registered`), never reportlab's
  built-in base14 fonts — they don't cover Vietnamese diacritics and would silently mangle
  output text. Reuse `report_service.export_to_excel`/`export_to_pdf` for any new report
  rather than hand-rolling `pd.ExcelWriter`/`SimpleDocTemplate` calls elsewhere.
- **Frontend**: Ant Design components + `@tanstack/react-query` for all server state (no manual
  loading-state booleans). New pages go under `src/pages/<domain>/`, gated in `src/App.tsx` via
  `<ProtectedRoute allowedRoles={[...]}>` when role-restricted.
- **Vietnamese UI text, English code**: all user-facing strings (labels, messages, page titles)
  are in Vietnamese; identifiers, comments, commit messages stay in English.
- **Code-field standardization**: any "mã"/identifier field (equipment code, department code,
  borrow slip code) must go through `app/core/text_utils.normalize_code` (a Pydantic
  `field_validator` on the schema) so it ends up unaccented, uppercase, hyphen-separated —
  e.g. "Khoa Xét Nghiệm" → "KHOA-XET-NGHIEM". Apply this to new code-style fields as they're
  added. Do NOT apply it to descriptive/free-text fields (names, notes, purpose, condition) —
  those keep full Vietnamese diacritics since they're for display, not identification.

## Git Workflow

- Branch naming: `claude/<slug>` (e.g. this branch, `claude/claude-md-docs-rw1io9`).
- Don't create a PR unless explicitly asked.
