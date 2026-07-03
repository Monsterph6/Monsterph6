export type UserRole = "admin" | "department_staff" | "technician";

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: UserRole;
  department_id: number | null;
  is_active: boolean;
}
