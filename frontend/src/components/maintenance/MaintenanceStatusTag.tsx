import { Tag } from "antd";

import type { MaintenanceRecord } from "../../types/maintenance";

export function MaintenanceStatusTag({ record }: { record: MaintenanceRecord }) {
  if (record.status === "scheduled" && record.scheduled_date < new Date().toISOString().slice(0, 10)) {
    return <Tag color="red">Quá hạn</Tag>;
  }
  switch (record.status) {
    case "scheduled":
      return <Tag color="blue">Sắp tới</Tag>;
    case "completed":
      return <Tag color="green">Đã hoàn thành</Tag>;
    case "cancelled":
      return <Tag color="default">Đã hủy</Tag>;
    default:
      return <Tag color="red">Quá hạn</Tag>;
  }
}
