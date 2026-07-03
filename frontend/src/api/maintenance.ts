import { apiClient } from "./client";
import type { MaintenanceRecord, MaintenanceRecordType, MaintenanceStatus } from "../types/maintenance";

export interface MaintenanceFilters {
  equipment_id?: number;
  status_filter?: MaintenanceStatus;
  record_type?: MaintenanceRecordType;
}

export async function listMaintenanceRecords(filters: MaintenanceFilters = {}): Promise<MaintenanceRecord[]> {
  const { data } = await apiClient.get<MaintenanceRecord[]>("/maintenance", { params: filters });
  return data;
}

export async function listMaintenanceAlerts(): Promise<MaintenanceRecord[]> {
  const { data } = await apiClient.get<MaintenanceRecord[]>("/maintenance/alerts");
  return data;
}

export interface CreateMaintenancePayload {
  equipment_id: number;
  record_type: MaintenanceRecordType;
  scheduled_date: string;
  interval_days?: number | null;
  notes?: string | null;
}

export async function createMaintenanceRecord(payload: CreateMaintenancePayload): Promise<MaintenanceRecord> {
  const { data } = await apiClient.post<MaintenanceRecord>("/maintenance", payload);
  return data;
}

export interface CompleteMaintenancePayload {
  completed_date?: string;
  performed_by?: string | null;
  notes?: string | null;
}

export async function completeMaintenanceRecord(
  id: number,
  payload: CompleteMaintenancePayload,
): Promise<MaintenanceRecord> {
  const { data } = await apiClient.post<MaintenanceRecord>(`/maintenance/${id}/complete`, payload);
  return data;
}
