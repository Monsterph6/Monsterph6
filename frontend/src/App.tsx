import { Navigate, Route, Routes } from "react-router-dom";

import { ProtectedRoute } from "./auth/ProtectedRoute";
import { AppLayout } from "./layouts/AppLayout";
import { DashboardPage } from "./pages/DashboardPage";
import { LoginPage } from "./pages/LoginPage";
import { DepartmentListPage } from "./pages/departments/DepartmentListPage";
import { EquipmentFormPage } from "./pages/equipment/EquipmentFormPage";
import { EquipmentListPage } from "./pages/equipment/EquipmentListPage";
import { MaintenanceListPage } from "./pages/maintenance/MaintenanceListPage";
import { UserListPage } from "./pages/users/UserListPage";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<DashboardPage />} />
        <Route path="/equipment" element={<EquipmentListPage />} />
        <Route path="/equipment/new" element={<EquipmentFormPage />} />
        <Route path="/equipment/:id/edit" element={<EquipmentFormPage />} />
        <Route path="/maintenance" element={<MaintenanceListPage />} />
        <Route
          path="/departments"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <DepartmentListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/users"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <UserListPage />
            </ProtectedRoute>
          }
        />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
