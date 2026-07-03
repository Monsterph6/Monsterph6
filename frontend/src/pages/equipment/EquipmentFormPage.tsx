import { App, Button, Card, Form, Input, Select, Space, Tabs } from "antd";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { createEquipment, getEquipment, updateEquipment } from "../../api/equipment";
import { listDepartments } from "../../api/departments";
import { listBorrowRecords } from "../../api/borrow";
import { listMaintenanceRecords } from "../../api/maintenance";
import { BorrowRecordFormModal } from "../../components/borrow/BorrowRecordFormModal";
import { BorrowRecordTable } from "../../components/borrow/BorrowRecordTable";
import { MaintenanceRecordFormModal } from "../../components/maintenance/MaintenanceRecordFormModal";
import { MaintenanceRecordTable } from "../../components/maintenance/MaintenanceRecordTable";
import { useAuth } from "../../auth/AuthContext";

// "borrowed" is not listed here deliberately: it's system-managed by the borrow
// workflow (set/cleared automatically), not something a user picks by hand.
const STATUS_OPTIONS = [
  { value: "active", label: "Đang hoạt động" },
  { value: "in_maintenance", label: "Đang bảo trì" },
  { value: "broken", label: "Hỏng" },
  { value: "retired", label: "Ngừng sử dụng" },
];

function EquipmentInfoTab({ id, isEdit }: { id: string | undefined; isEdit: boolean }) {
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
        <Select allowClear options={departments?.map((d) => ({ value: d.id, label: d.name }))} />
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
  );
}

function EquipmentMaintenanceTab({ equipmentId }: { equipmentId: number }) {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "technician";
  const [formOpen, setFormOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: records, isLoading } = useQuery({
    queryKey: ["maintenance", { equipment_id: equipmentId }],
    queryFn: () => listMaintenanceRecords({ equipment_id: equipmentId }),
  });

  function refresh() {
    queryClient.invalidateQueries({ queryKey: ["maintenance"] });
    queryClient.invalidateQueries({ queryKey: ["maintenance-alerts"] });
  }

  return (
    <Space direction="vertical" style={{ width: "100%" }}>
      {canManage && (
        <Button type="primary" onClick={() => setFormOpen(true)}>
          Thêm lịch mới
        </Button>
      )}
      <MaintenanceRecordTable records={records ?? []} isLoading={isLoading} onChanged={refresh} />
      <MaintenanceRecordFormModal
        open={formOpen}
        equipmentId={equipmentId}
        onClose={() => setFormOpen(false)}
        onCreated={() => {
          setFormOpen(false);
          refresh();
        }}
      />
    </Space>
  );
}

function EquipmentBorrowTab({ equipmentId }: { equipmentId: number }) {
  const { user } = useAuth();
  const canManage = user?.role === "admin" || user?.role === "department_staff";
  const [formOpen, setFormOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: records, isLoading } = useQuery({
    queryKey: ["borrow", { equipment_id: equipmentId }],
    queryFn: () => listBorrowRecords({ equipment_id: equipmentId }),
  });

  function refresh() {
    queryClient.invalidateQueries({ queryKey: ["borrow"] });
    queryClient.invalidateQueries({ queryKey: ["borrow-overdue"] });
    queryClient.invalidateQueries({ queryKey: ["equipment"] });
  }

  return (
    <Space direction="vertical" style={{ width: "100%" }}>
      {canManage && (
        <Button type="primary" onClick={() => setFormOpen(true)}>
          Thêm phiếu mượn
        </Button>
      )}
      <BorrowRecordTable records={records ?? []} isLoading={isLoading} onChanged={refresh} />
      <BorrowRecordFormModal
        open={formOpen}
        equipmentId={equipmentId}
        onClose={() => setFormOpen(false)}
        onCreated={() => {
          setFormOpen(false);
          refresh();
        }}
      />
    </Space>
  );
}

export function EquipmentFormPage() {
  const { id } = useParams();
  const isEdit = Boolean(id);

  if (!isEdit) {
    return (
      <Card title="Thêm thiết bị mới" style={{ maxWidth: 640 }}>
        <EquipmentInfoTab id={id} isEdit={isEdit} />
      </Card>
    );
  }

  return (
    <Card style={{ maxWidth: 800 }}>
      <Tabs
        items={[
          { key: "info", label: "Thông tin", children: <EquipmentInfoTab id={id} isEdit={isEdit} /> },
          {
            key: "maintenance",
            label: "Lịch bảo trì/hiệu chuẩn",
            children: <EquipmentMaintenanceTab equipmentId={Number(id)} />,
          },
          {
            key: "borrow",
            label: "Lịch sử mượn/trả",
            children: <EquipmentBorrowTab equipmentId={Number(id)} />,
          },
        ]}
      />
    </Card>
  );
}
