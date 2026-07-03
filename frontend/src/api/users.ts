import { apiClient } from "./client";
import type { User, UserRole } from "../types/user";

export async function listUsers(): Promise<User[]> {
  const { data } = await apiClient.get<User[]>("/users");
  return data;
}

export interface CreateUserPayload {
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  department_id?: number | null;
  password: string;
}

export async function createUser(payload: CreateUserPayload): Promise<User> {
  const { data } = await apiClient.post<User>("/users", payload);
  return data;
}
