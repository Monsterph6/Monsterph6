import { Table } from "antd";
import { useState } from "react";

import { useAuth } from "../../auth/AuthContext";
import type { BorrowRecord } from "../../types/borrow";
import { BorrowStatusTag } from "./BorrowStatusTag";
import { ReturnBorrowModal } from "./ReturnBorrowModal";

export function BorrowRecordTable({
  records,
  isLoading,
  showEquipmentColumn,
  onChanged,
}: {
  records: BorrowRecord[];
  isLoading: boolean;
  showEquipmentColumn?: boolean;
  onChanged: () => void;
}) {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "department_staff";
  const [returningRecord, setReturningRecord] = useState<BorrowRecord | null>(null);

  const columns = [
    { title: "Mã phiếu", dataIndex: "code" },
    ...(showEquipmentColumn
      ? [
          {
            title: "Thiết bị",
            key: "equipment",
            render: (_: unknown, record: BorrowRecord) => `${record.equipment_code} - ${record.equipment_name}`,
          },
        ]
      : []),
    {
      title: "Phòng ban mượn",
      dataIndex: "borrower_department_name",
      render: (v: string | null) => v ?? "-",
    },
    { title: "Ngày mượn", dataIndex: "borrow_date" },
    { title: "Ngày dự kiến trả", dataIndex: "expected_return_date", render: (d: string | null) => d ?? "-" },
    { title: "Ngày trả thực tế", dataIndex: "actual_return_date", render: (d: string | null) => d ?? "-" },
    {
      title: "Trạng thái",
      key: "status",
      render: (_: unknown, record: BorrowRecord) => <BorrowStatusTag record={record} />,
    },
    ...(canManage
      ? [
          {
            title: "",
            key: "actions",
            render: (_: unknown, record: BorrowRecord) =>
              record.status === "borrowed" ? (
                <a onClick={() => setReturningRecord(record)}>Ghi nhận trả</a>
              ) : null,
          },
        ]
      : []),
  ];

  return (
    <>
      <Table rowKey="id" loading={isLoading} columns={columns} dataSource={records} />
      <ReturnBorrowModal
        record={returningRecord}
        onClose={() => setReturningRecord(null)}
        onReturned={() => {
          setReturningRecord(null);
          onChanged();
        }}
      />
    </>
  );
}
