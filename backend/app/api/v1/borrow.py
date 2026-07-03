from fastapi import APIRouter

router = APIRouter(prefix="/borrow", tags=["borrow"])

# Phase 3: borrow/return workflow. The BorrowRecord table already exists
# (see app/models/borrow.py) so this phase is pure business-logic + UI work.
