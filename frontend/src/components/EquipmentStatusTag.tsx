import { Tag } from "antd";

import type { EquipmentStatus } from "../types/equipment";

const LABELS: Record<EquipmentStatus, { text: string; color: string }> = {
  active: { text: "Đang hoạt động", color: "green" },
  in_maintenance: { text: "Đang bảo trì", color: "gold" },
  borrowed: { text: "Đang được mượn", color: "blue" },
  broken: { text: "Hỏng", color: "red" },
  retired: { text: "Ngừng sử dụng", color: "default" },
};

export function EquipmentStatusTag({ status }: { status: EquipmentStatus }) {
  const { text, color } = LABELS[status];
  return <Tag color={color}>{text}</Tag>;
}
