import { apiClient } from "./client";

export type ReportFormat = "xlsx" | "pdf";

async function downloadReport(path: string, params: { format: ReportFormat }, filenamePrefix: string) {
  const response = await apiClient.get(path, { params, responseType: "blob" });
  const disposition = response.headers["content-disposition"] as string | undefined;
  const match = disposition?.match(/filename=(.+)$/);
  const filename = match ? match[1] : `${filenamePrefix}.${params.format}`;

  const url = URL.createObjectURL(response.data as Blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export interface EquipmentReportFilters {
  format: ReportFormat;
  department_id?: number;
  status?: string;
  category_id?: number;
}

export function downloadEquipmentReport(filters: EquipmentReportFilters) {
  return downloadReport("/reports/equipment", filters, "danh_muc_thiet_bi");
}

export interface MaintenanceReportFilters {
  format: ReportFormat;
  department_id?: number;
  date_from?: string;
  date_to?: string;
  record_type?: string;
  status?: string;
}

export function downloadMaintenanceReport(filters: MaintenanceReportFilters) {
  return downloadReport("/reports/maintenance", filters, "lich_su_bao_tri");
}

export interface BorrowReportFilters {
  format: ReportFormat;
  department_id?: number;
  date_from?: string;
  date_to?: string;
  status?: string;
}

export function downloadBorrowReport(filters: BorrowReportFilters) {
  return downloadReport("/reports/borrow", filters, "lich_su_muon_tra");
}
