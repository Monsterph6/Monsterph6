import { apiClient } from "./client";
import type { BorrowRecord, BorrowStatus } from "../types/borrow";

export interface BorrowFilters {
  equipment_id?: number;
  department_id?: number;
  status_filter?: BorrowStatus;
}

export async function listBorrowRecords(filters: BorrowFilters = {}): Promise<BorrowRecord[]> {
  const { data } = await apiClient.get<BorrowRecord[]>("/borrow", { params: filters });
  return data;
}

export async function listOverdueBorrows(): Promise<BorrowRecord[]> {
  const { data } = await apiClient.get<BorrowRecord[]>("/borrow/overdue");
  return data;
}

export interface CreateBorrowPayload {
  equipment_id: number;
  borrower_user_id?: number | null;
  borrower_department_id?: number | null;
  purpose?: string | null;
  approved_by?: string | null;
  expected_return_date?: string | null;
  condition_on_borrow?: string | null;
  notes?: string | null;
}

export async function createBorrowRecord(payload: CreateBorrowPayload): Promise<BorrowRecord> {
  const { data } = await apiClient.post<BorrowRecord>("/borrow", payload);
  return data;
}

export interface ReturnBorrowPayload {
  actual_return_date?: string;
  condition_on_return?: string | null;
  received_by?: string | null;
  notes?: string | null;
}

export async function returnBorrowRecord(id: number, payload: ReturnBorrowPayload): Promise<BorrowRecord> {
  const { data } = await apiClient.post<BorrowRecord>(`/borrow/${id}/return`, payload);
  return data;
}
