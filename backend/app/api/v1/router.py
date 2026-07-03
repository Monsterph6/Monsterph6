from fastapi import APIRouter

from app.api.v1 import auth, borrow, departments, equipment, maintenance, reports, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(departments.router)
api_router.include_router(equipment.router)
api_router.include_router(maintenance.router)
api_router.include_router(borrow.router)
api_router.include_router(reports.router)
