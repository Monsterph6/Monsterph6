import { apiClient } from "./client";
import type { User } from "../types/user";

export async function login(username: string, password: string): Promise<string> {
  const form = new URLSearchParams();
  form.set("username", username);
  form.set("password", password);
  const { data } = await apiClient.post("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return data.access_token as string;
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>("/auth/me");
  return data;
}
