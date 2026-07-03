import { App, DatePicker, Form, Input, Modal } from "antd";
import dayjs from "dayjs";

import { returnBorrowRecord } from "../../api/borrow";
import type { BorrowRecord } from "../../types/borrow";

export function ReturnBorrowModal({
  record,
  onClose,
  onReturned,
}: {
  record: BorrowRecord | null;
  onClose: () => void;
  onReturned: () => void;
}) {
  const [form] = Form.useForm();
  const { message } = App.useApp();

  async function handleFinish(values: {
    actual_return_date: dayjs.Dayjs;
    condition_on_return?: string;
    received_by?: string;
    notes?: string;
  }) {
    if (!record) return;
    try {
      await returnBorrowRecord(record.id, {
        actual_return_date: values.actual_return_date.format("YYYY-MM-DD"),
        condition_on_return: values.condition_on_return,
        received_by: values.received_by,
        notes: values.notes,
      });
      message.success("Đã ghi nhận trả thiết bị");
      form.resetFields();
      onReturned();
    } catch {
      message.error("Không thể ghi nhận trả thiết bị");
    }
  }

  return (
    <Modal
      title="Ghi nhận trả thiết bị"
      open={record !== null}
      onCancel={onClose}
      onOk={() => form.submit()}
      destroyOnClose
    >
      <Form
        layout="vertical"
        form={form}
        onFinish={handleFinish}
        initialValues={{ actual_return_date: dayjs() }}
      >
        <Form.Item name="actual_return_date" label="Ngày trả" rules={[{ required: true }]}>
          <DatePicker style={{ width: "100%" }} format="DD/MM/YYYY" />
        </Form.Item>
        <Form.Item name="condition_on_return" label="Tình trạng thiết bị khi nhận trả">
          <Input placeholder="Bình thường / Có hư hỏng..." />
        </Form.Item>
        <Form.Item name="received_by" label="Người nhận trả">
          <Input />
        </Form.Item>
        <Form.Item name="notes" label="Ghi chú">
          <Input.TextArea rows={2} />
        </Form.Item>
      </Form>
    </Modal>
  );
}
