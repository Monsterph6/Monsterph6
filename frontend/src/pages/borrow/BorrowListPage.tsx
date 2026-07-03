import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Button, Select, Space } from "antd";
import { useState } from "react";

import { listBorrowRecords, type BorrowFilters } from "../../api/borrow";
import { listDepartments } from "../../api/departments";
import { listEquipment } from "../../api/equipment";
import { useAuth } from "../../auth/AuthContext";
import { BorrowRecordFormModal } from "../../components/borrow/BorrowRecordFormModal";
import { BorrowRecordTable } from "../../components/borrow/BorrowRecordTable";

const STATUS_OPTIONS = [
  { value: "borrowed", label: "Đang mượn / Quá hạn" },
  { value: "returned", label: "Đã trả" },
];

export function BorrowListPage() {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "department_staff";
  const [filters, setFilters] = useState<BorrowFilters>({});
  const [formOpen, setFormOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: equipmentData } = useQuery({
    queryKey: ["equipment", "all-for-select"],
    queryFn: () => listEquipment({ page: 1, page_size: 1000 }),
  });
  const { data: departments } = useQuery({ queryKey: ["departments"], queryFn: listDepartments });

  const { data: records, isLoading } = useQuery({
    queryKey: ["borrow", filters],
    queryFn: () => listBorrowRecords(filters),
  });

  function refresh() {
    queryClient.invalidateQueries({ queryKey: ["borrow"] });
    queryClient.invalidateQueries({ queryKey: ["borrow-overdue"] });
    queryClient.invalidateQueries({ queryKey: ["equipment"] });
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
            placeholder="Lọc theo phòng ban"
            style={{ width: 220 }}
            showSearch
            optionFilterProp="label"
            options={departments?.map((d) => ({ value: d.id, label: d.name }))}
            onChange={(value) => setFilters((f) => ({ ...f, department_id: value }))}
          />
          <Select
            allowClear
            placeholder="Trạng thái"
            style={{ width: 200 }}
            options={STATUS_OPTIONS}
            onChange={(value) => setFilters((f) => ({ ...f, status_filter: value }))}
          />
        </Space>
        {canManage && (
          <Button type="primary" onClick={() => setFormOpen(true)}>
            Thêm phiếu mượn
          </Button>
        )}
      </Space>
      <BorrowRecordTable records={records ?? []} isLoading={isLoading} showEquipmentColumn onChanged={refresh} />
      <BorrowRecordFormModal
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
