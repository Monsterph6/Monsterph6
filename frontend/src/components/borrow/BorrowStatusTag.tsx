import { Tag } from "antd";

import type { BorrowRecord } from "../../types/borrow";

export function BorrowStatusTag({ record }: { record: BorrowRecord }) {
  if (
    record.status === "borrowed" &&
    record.expected_return_date &&
    record.expected_return_date < new Date().toISOString().slice(0, 10)
  ) {
    return <Tag color="red">Quá hạn trả</Tag>;
  }
  switch (record.status) {
    case "borrowed":
      return <Tag color="blue">Đang mượn</Tag>;
    case "returned":
      return <Tag color="green">Đã trả</Tag>;
    default:
      return <Tag color="red">Quá hạn trả</Tag>;
  }
}
