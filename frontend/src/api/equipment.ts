import { apiClient } from "./client";
import type { Equipment, EquipmentListResponse, EquipmentStatus } from "../types/equipment";

export interface EquipmentFilters {
  page?: number;
  page_size?: number;
  department_id?: number;
  status?: EquipmentStatus;
  search?: string;
}

export async function listEquipment(filters: EquipmentFilters): Promise<EquipmentListResponse> {
  const { data } = await apiClient.get<EquipmentListResponse>("/equipment", { params: filters });
  return data;
}

export async function getEquipment(id: number): Promise<Equipment> {
  const { data } = await apiClient.get<Equipment>(`/equipment/${id}`);
  return data;
}

export type EquipmentCreatePayload = Omit<Equipment, "id">;

export async function createEquipment(payload: EquipmentCreatePayload): Promise<Equipment> {
  const { data } = await apiClient.post<Equipment>("/equipment", payload);
  return data;
}

export async function updateEquipment(id: number, payload: Partial<EquipmentCreatePayload>): Promise<Equipment> {
  const { data } = await apiClient.put<Equipment>(`/equipment/${id}`, payload);
  return data;
}

export async function retireEquipment(id: number): Promise<void> {
  await apiClient.delete(`/equipment/${id}`);
}
