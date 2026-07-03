import { App, Button, Card, Form, Input, Select } from "antd";
import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { createEquipment, getEquipment, updateEquipment } from "../../api/equipment";
import { listDepartments } from "../../api/departments";

const STATUS_OPTIONS = [
  { value: "active", label: "Đang hoạt động" },
  { value: "in_maintenance", label: "Đang bảo trì" },
  { value: "broken", label: "Hỏng" },
  { value: "retired", label: "Ngừng sử dụng" },
];

export function EquipmentFormPage() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const { message } = App.useApp();

  const { data: departments } = useQuery({ queryKey: ["departments"], queryFn: listDepartments });
  const { data: equipment } = useQuery({
    queryKey: ["equipment", id],
    queryFn: () => getEquipment(Number(id)),
    enabled: isEdit,
  });

  useEffect(() => {
    if (equipment) form.setFieldsValue(equipment);
  }, [equipment, form]);

  async function handleFinish(values: Record<string, unknown>) {
    try {
      if (isEdit) {
        await updateEquipment(Number(id), values);
        message.success("Đã cập nhật thiết bị");
      } else {
        await createEquipment(values as Parameters<typeof createEquipment>[0]);
        message.success("Đã thêm thiết bị mới");
      }
      navigate("/equipment");
    } catch {
      message.error("Có lỗi xảy ra, vui lòng kiểm tra lại thông tin");
    }
  }

  return (
    <Card title={isEdit ? "Sửa thiết bị" : "Thêm thiết bị mới"} style={{ maxWidth: 640 }}>
      <Form layout="vertical" form={form} onFinish={handleFinish} initialValues={{ status: "active" }}>
        <Form.Item name="code" label="Mã thiết bị" rules={[{ required: true }]}>
          <Input disabled={isEdit} />
        </Form.Item>
        <Form.Item name="name" label="Tên thiết bị" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item name="manufacturer" label="Nhà sản xuất">
          <Input />
        </Form.Item>
        <Form.Item name="model" label="Model">
          <Input />
        </Form.Item>
        <Form.Item name="serial_number" label="Số seri">
          <Input />
        </Form.Item>
        <Form.Item name="location" label="Vị trí">
          <Input />
        </Form.Item>
        <Form.Item name="department_id" label="Phòng ban quản lý">
          <Select
            allowClear
            options={departments?.map((d) => ({ value: d.id, label: d.name }))}
          />
        </Form.Item>
        <Form.Item name="status" label="Trạng thái" rules={[{ required: true }]}>
          <Select options={STATUS_OPTIONS} />
        </Form.Item>
        <Form.Item name="specs_notes" label="Ghi chú/thông số">
          <Input.TextArea rows={3} />
        </Form.Item>
        <Button type="primary" htmlType="submit">
          Lưu
        </Button>
      </Form>
    </Card>
  );
}
