"""Run once after migrations: python -m app.seed.seed_data"""
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.department import Department
from app.models.user import User, UserRole


def run():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == settings.SEED_ADMIN_USERNAME).first():
            admin = User(
                username=settings.SEED_ADMIN_USERNAME,
                email=settings.SEED_ADMIN_EMAIL,
                full_name="Quản trị viên hệ thống",
                role=UserRole.admin,
                hashed_password=hash_password(settings.SEED_ADMIN_PASSWORD),
            )
            db.add(admin)
            print(f"Created admin user '{settings.SEED_ADMIN_USERNAME}'")

        default_departments = [
            ("KXN", "Khoa Xét nghiệm"),
            ("KDT", "Khoa Dược - Trang thiết bị y tế"),
            ("KKSDB", "Khoa Kiểm soát dịch bệnh"),
        ]
        for code, name in default_departments:
            if not db.query(Department).filter(Department.code == code).first():
                db.add(Department(code=code, name=name))
                print(f"Created department '{code}'")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
