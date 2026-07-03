import { apiClient } from "./client";
import type { Department } from "../types/department";

export async function listDepartments(): Promise<Department[]> {
  const { data } = await apiClient.get<Department[]>("/departments");
  return data;
}

export async function createDepartment(payload: { code: string; name: string }): Promise<Department> {
  const { data } = await apiClient.post<Department>("/departments", payload);
  return data;
}
