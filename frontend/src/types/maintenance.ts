export type MaintenanceRecordType = "maintenance" | "calibration";
export type MaintenanceStatus = "scheduled" | "completed" | "overdue" | "cancelled";

export interface MaintenanceRecord {
  id: number;
  equipment_id: number;
  equipment_code: string | null;
  equipment_name: string | null;
  record_type: MaintenanceRecordType;
  scheduled_date: string;
  completed_date: string | null;
  status: MaintenanceStatus;
  performed_by: string | null;
  next_due_date: string | null;
  interval_days: number | null;
  notes: string | null;
}
