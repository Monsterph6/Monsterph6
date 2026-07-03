import { useQuery } from "@tanstack/react-query";
import { App, DatePicker, Form, Input, Modal, Select } from "antd";
import dayjs from "dayjs";

import { createBorrowRecord } from "../../api/borrow";
import { listDepartments } from "../../api/departments";
import { listEquipment } from "../../api/equipment";

export function BorrowRecordFormModal({
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

  const { data: equipmentData } = useQuery({
    queryKey: ["equipment", "active-for-select"],
    queryFn: () => listEquipment({ page: 1, page_size: 1000, status: "active" }),
    enabled: open && equipmentId === undefined,
  });
  const { data: departments } = useQuery({
    queryKey: ["departments"],
    queryFn: listDepartments,
    enabled: open,
  });

  async function handleFinish(values: {
    equipment_id: number;
    borrower_department_id: number;
    purpose?: string;
    approved_by?: string;
    expected_return_date?: dayjs.Dayjs;
    condition_on_borrow?: string;
    notes?: string;
  }) {
    try {
      await createBorrowRecord({
        equipment_id: equipmentId ?? values.equipment_id,
        borrower_department_id: values.borrower_department_id,
        purpose: values.purpose,
        approved_by: values.approved_by,
        expected_return_date: values.expected_return_date?.format("YYYY-MM-DD"),
        condition_on_borrow: values.condition_on_borrow,
        notes: values.notes,
      });
      message.success("Đã tạo phiếu mượn");
      form.resetFields();
      onCreated();
    } catch {
      message.error("Không thể tạo phiếu mượn, vui lòng kiểm tra lại thông tin (thiết bị có thể đang không sẵn sàng)");
    }
  }

  return (
    <Modal title="Thêm phiếu mượn thiết bị" open={open} onCancel={onClose} onOk={() => form.submit()} destroyOnClose>
      <Form layout="vertical" form={form} onFinish={handleFinish}>
        {equipmentId === undefined && (
          <Form.Item name="equipment_id" label="Thiết bị" rules={[{ required: true }]}>
            <Select
              showSearch
              placeholder="Chọn thiết bị (chỉ hiện thiết bị đang sẵn sàng)"
              optionFilterProp="label"
              options={equipmentData?.items.map((e) => ({ value: e.id, label: `${e.code} - ${e.name}` }))}
            />
          </Form.Item>
        )}
        <Form.Item name="borrower_department_id" label="Phòng ban mượn" rules={[{ required: true }]}>
          <Select
            showSearch
            optionFilterProp="label"
            options={departments?.map((d) => ({ value: d.id, label: d.name }))}
          />
        </Form.Item>
        <Form.Item name="purpose" label="Mục đích mượn">
          <Input.TextArea rows={2} />
        </Form.Item>
        <Form.Item name="approved_by" label="Người phê duyệt">
          <Input />
        </Form.Item>
        <Form.Item name="expected_return_date" label="Ngày dự kiến trả">
          <DatePicker style={{ width: "100%" }} format="DD/MM/YYYY" />
        </Form.Item>
        <Form.Item name="condition_on_borrow" label="Tình trạng thiết bị khi giao">
          <Input placeholder="Bình thường..." />
        </Form.Item>
        <Form.Item name="notes" label="Ghi chú">
          <Input.TextArea rows={2} />
        </Form.Item>
      </Form>
    </Modal>
  );
}
