import { App, DatePicker, Form, Input, Modal } from "antd";
import dayjs from "dayjs";

import { completeMaintenanceRecord } from "../../api/maintenance";
import type { MaintenanceRecord } from "../../types/maintenance";

export function CompleteRecordModal({
  record,
  onClose,
  onCompleted,
}: {
  record: MaintenanceRecord | null;
  onClose: () => void;
  onCompleted: () => void;
}) {
  const [form] = Form.useForm();
  const { message } = App.useApp();

  async function handleFinish(values: { completed_date: dayjs.Dayjs; performed_by?: string; notes?: string }) {
    if (!record) return;
    try {
      await completeMaintenanceRecord(record.id, {
        completed_date: values.completed_date.format("YYYY-MM-DD"),
        performed_by: values.performed_by,
        notes: values.notes,
      });
      message.success("Đã ghi nhận hoàn thành");
      form.resetFields();
      onCompleted();
    } catch {
      message.error("Không thể ghi nhận hoàn thành");
    }
  }

  return (
    <Modal
      title="Ghi nhận hoàn thành"
      open={record !== null}
      onCancel={onClose}
      onOk={() => form.submit()}
      destroyOnClose
    >
      <Form layout="vertical" form={form} onFinish={handleFinish} initialValues={{ completed_date: dayjs() }}>
        <Form.Item name="completed_date" label="Ngày hoàn thành" rules={[{ required: true }]}>
          <DatePicker style={{ width: "100%" }} format="DD/MM/YYYY" />
        </Form.Item>
        <Form.Item name="performed_by" label="Người thực hiện">
          <Input />
        </Form.Item>
        <Form.Item name="notes" label="Ghi chú">
          <Input.TextArea rows={2} />
        </Form.Item>
      </Form>
    </Modal>
  );
}
