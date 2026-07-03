export type EquipmentStatus = "active" | "in_maintenance" | "broken" | "retired";

export interface Equipment {
  id: number;
  code: string;
  name: string;
  category_id: number | null;
  manufacturer: string | null;
  model: string | null;
  serial_number: string | null;
  purchase_date: string | null;
  warranty_expiry_date: string | null;
  location: string | null;
  department_id: number | null;
  status: EquipmentStatus;
  specs_notes: string | null;
}

export interface EquipmentListResponse {
  items: Equipment[];
  total: number;
  page: number;
  page_size: number;
}
