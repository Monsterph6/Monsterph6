# Quản lý trang thiết bị chuyên dụng - CDC Hải Phòng

Ứng dụng web quản lý trang thiết bị chuyên dụng: danh mục thiết bị, lịch bảo trì/hiệu chuẩn,
mượn/trả, người dùng & phân quyền, báo cáo.

- Backend: FastAPI + PostgreSQL (SQLAlchemy + Alembic)
- Frontend: React + TypeScript + Vite + Ant Design
- Triển khai: Docker Compose

See `docs/phase-plan.md` for the feature roadmap and `CLAUDE.md` for codebase conventions.

## Chạy bằng Docker (khuyến nghị)

```bash
cp .env.example .env   # sửa mật khẩu/secret trước khi dùng thật
docker compose up --build
```

- Frontend: http://localhost (dev: http://localhost:5173 nhờ `docker-compose.override.yml`)
- Backend API docs: http://localhost:8000/docs (dev only, exposed via override)
- Tài khoản admin khởi tạo: giá trị `SEED_ADMIN_USERNAME` / `SEED_ADMIN_PASSWORD` trong `.env`

## Chạy thủ công (không Docker)

Backend:
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # điền DATABASE_URL trỏ tới Postgres cục bộ
alembic upgrade head
python -m app.seed.seed_data
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Kiểm thử nhanh

```bash
cd backend && pytest
cd frontend && npm run lint && npx tsc -b
```
