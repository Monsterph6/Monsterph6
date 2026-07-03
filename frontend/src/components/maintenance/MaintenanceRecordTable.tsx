import { Table } from "antd";
import { useState } from "react";

import { useAuth } from "../../auth/AuthContext";
import type { MaintenanceRecord } from "../../types/maintenance";
import { CompleteRecordModal } from "./CompleteRecordModal";
import { MaintenanceStatusTag } from "./MaintenanceStatusTag";

const TYPE_LABELS = { maintenance: "Bảo trì", calibration: "Hiệu chuẩn" };

export function MaintenanceRecordTable({
  records,
  isLoading,
  showEquipmentColumn,
  onChanged,
}: {
  records: MaintenanceRecord[];
  isLoading: boolean;
  showEquipmentColumn?: boolean;
  onChanged: () => void;
}) {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "technician";
  const [completingRecord, setCompletingRecord] = useState<MaintenanceRecord | null>(null);

  const columns = [
    ...(showEquipmentColumn
      ? [
          {
            title: "Thiết bị",
            key: "equipment",
            render: (_: unknown, record: MaintenanceRecord) => `${record.equipment_code} - ${record.equipment_name}`,
          },
        ]
      : []),
    {
      title: "Loại",
      dataIndex: "record_type",
      render: (type: MaintenanceRecord["record_type"]) => TYPE_LABELS[type],
    },
    { title: "Ngày dự kiến", dataIndex: "scheduled_date" },
    { title: "Ngày hoàn thành", dataIndex: "completed_date", render: (d: string | null) => d ?? "-" },
    { title: "Người thực hiện", dataIndex: "performed_by", render: (v: string | null) => v ?? "-" },
    {
      title: "Trạng thái",
      key: "status",
      render: (_: unknown, record: MaintenanceRecord) => <MaintenanceStatusTag record={record} />,
    },
    ...(canManage
      ? [
          {
            title: "",
            key: "actions",
            render: (_: unknown, record: MaintenanceRecord) =>
              record.status === "scheduled" ? (
                <a onClick={() => setCompletingRecord(record)}>Ghi nhận hoàn thành</a>
              ) : null,
          },
        ]
      : []),
  ];

  return (
    <>
      <Table rowKey="id" loading={isLoading} columns={columns} dataSource={records} />
      <CompleteRecordModal
        record={completingRecord}
        onClose={() => setCompletingRecord(null)}
        onCompleted={() => {
          setCompletingRecord(null);
          onChanged();
        }}
      />
    </>
  );
}
