import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Button, Select, Space } from "antd";
import { useState } from "react";

import { listEquipment } from "../../api/equipment";
import { listMaintenanceRecords, type MaintenanceFilters } from "../../api/maintenance";
import { useAuth } from "../../auth/AuthContext";
import { MaintenanceRecordFormModal } from "../../components/maintenance/MaintenanceRecordFormModal";
import { MaintenanceRecordTable } from "../../components/maintenance/MaintenanceRecordTable";

const STATUS_OPTIONS = [
  { value: "scheduled", label: "Sắp tới / Quá hạn" },
  { value: "completed", label: "Đã hoàn thành" },
  { value: "cancelled", label: "Đã hủy" },
];

const TYPE_OPTIONS = [
  { value: "maintenance", label: "Bảo trì" },
  { value: "calibration", label: "Hiệu chuẩn" },
];

export function MaintenanceListPage() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "technician";
  const [filters, setFilters] = useState<MaintenanceFilters>({});
  const [formOpen, setFormOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: equipmentData } = useQuery({
    queryKey: ["equipment", "all-for-select"],
    queryFn: () => listEquipment({ page: 1, page_size: 1000 }),
  });

  const { data: records, isLoading } = useQuery({
    queryKey: ["maintenance", filters],
    queryFn: () => listMaintenanceRecords(filters),
  });

  function refresh() {
    queryClient.invalidateQueries({ queryKey: ["maintenance"] });
    queryClient.invalidateQueries({ queryKey: ["maintenance-alerts"] });
  }

  return (
    <Space direction="vertical" style={{ width: "100%" }} size="middle">
      <Space style={{ justifyContent: "space-between", width: "100%" }} wrap>
        <Space wrap>
          <Select
            allowClear
            placeholder="Lọc theo thiết bị"
            style={{ width: 260 }}
            showSearch
            optionFilterProp="label"
            options={equipmentData?.items.map((e) => ({ value: e.id, label: `${e.code} - ${e.name}` }))}
            onChange={(value) => setFilters((f) => ({ ...f, equipment_id: value }))}
          />
          <Select
            allowClear
            placeholder="Trạng thái"
            style={{ width: 200 }}
            options={STATUS_OPTIONS}
            onChange={(value) => setFilters((f) => ({ ...f, status_filter: value }))}
          />
          <Select
            allowClear
            placeholder="Loại"
            style={{ width: 160 }}
            options={TYPE_OPTIONS}
            onChange={(value) => setFilters((f) => ({ ...f, record_type: value }))}
          />
        </Space>
        {canManage && (
          <Button type="primary" onClick={() => setFormOpen(true)}>
            Thêm lịch mới
          </Button>
        )}
      </Space>
      <MaintenanceRecordTable records={records ?? []} isLoading={isLoading} showEquipmentColumn onChanged={refresh} />
      <MaintenanceRecordFormModal
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onCreated={() => {
          setFormOpen(false);
          refresh();
        }}
      />
    </Space>
  );
}
