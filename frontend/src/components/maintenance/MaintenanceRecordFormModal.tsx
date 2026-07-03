import { useQuery } from "@tanstack/react-query";
import { App, DatePicker, Form, Input, InputNumber, Modal, Select } from "antd";
import dayjs from "dayjs";

import { listEquipment } from "../../api/equipment";
import { createMaintenanceRecord } from "../../api/maintenance";

const TYPE_OPTIONS = [
  { value: "maintenance", label: "Bảo trì" },
  { value: "calibration", label: "Hiệu chuẩn" },
];

export function MaintenanceRecordFormModal({
  open,
  equipmentId,
  onClose,
  onCreated,
}: {
  open: boolean;
  equipmentId?: number;
  onClose: () => void;
  onCreated: () => void;
}) {
  const [form] = Form.useForm();
  const { message } = App.useApp();

  // Fetch a large page so the equipment picker covers the full catalog (~600 devices).
  const { data: equipmentData } = useQuery({
    queryKey: ["equipment", "all-for-select"],
    queryFn: () => listEquipment({ page: 1, page_size: 1000 }),
    enabled: open && equipmentId === undefined,
  });

  async function handleFinish(values: {
    equipment_id: number;
    record_type: "maintenance" | "calibration";
    scheduled_date: dayjs.Dayjs;
    interval_days?: number;
    notes?: string;
  }) {
    try {
      await createMaintenanceRecord({
        equipment_id: equipmentId ?? values.equipment_id,
        record_type: values.record_type,
        scheduled_date: values.scheduled_date.format("YYYY-MM-DD"),
        interval_days: values.interval_days,
        notes: values.notes,
      });
      message.success("Đã thêm lịch bảo trì/hiệu chuẩn");
      form.resetFields();
      onCreated();
    } catch {
      message.error("Không thể thêm lịch, vui lòng kiểm tra lại thông tin");
    }
  }

  return (
    <Modal
      title="Thêm lịch bảo trì/hiệu chuẩn"
      open={open}
      onCancel={onClose}
      onOk={() => form.submit()}
      destroyOnClose
    >
      <Form layout="vertical" form={form} onFinish={handleFinish}>
        {equipmentId === undefined && (
          <Form.Item name="equipment_id" label="Thiết bị" rules={[{ required: true }]}>
            <Select
              showSearch
              placeholder="Chọn thiết bị"
              optionFilterProp="label"
              options={equipmentData?.items.map((e) => ({ value: e.id, label: `${e.code} - ${e.name}` }))}
            />
          </Form.Item>
        )}
        <Form.Item name="record_type" label="Loại" rules={[{ required: true }]}>
          <Select options={TYPE_OPTIONS} />
        </Form.Item>
        <Form.Item name="scheduled_date" label="Ngày dự kiến" rules={[{ required: true }]}>
          <DatePicker style={{ width: "100%" }} format="DD/MM/YYYY" />
        </Form.Item>
        <Form.Item
          name="interval_days"
          label="Chu kỳ lặp lại (số ngày)"
          tooltip="Nếu đặt, khi ghi nhận hoàn thành hệ thống sẽ tự tạo lịch kế tiếp"
        >
          <InputNumber style={{ width: "100%" }} min={1} placeholder="Ví dụ: 180" />
        </Form.Item>
        <Form.Item name="notes" label="Ghi chú">
          <Input.TextArea rows={2} />
        </Form.Item>
      </Form>
    </Modal>
  );
}
