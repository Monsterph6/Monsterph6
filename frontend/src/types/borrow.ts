export type BorrowStatus = "borrowed" | "returned" | "overdue";

export interface BorrowRecord {
  id: number;
  code: string;
  equipment_id: number;
  equipment_code: string | null;
  equipment_name: string | null;
  borrower_user_id: number | null;
  borrower_user_name: string | null;
  borrower_department_id: number | null;
  borrower_department_name: string | null;
  purpose: string | null;
  approved_by: string | null;
  borrow_date: string;
  expected_return_date: string | null;
  actual_return_date: string | null;
  condition_on_borrow: string | null;
  condition_on_return: string | null;
  received_by: string | null;
  status: BorrowStatus;
  notes: string | null;
}
