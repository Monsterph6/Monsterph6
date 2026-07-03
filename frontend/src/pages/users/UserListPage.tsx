import { useQuery, useQueryClient } from "@tanstack/react-query";
import { App, Button, Form, Input, Modal, Select, Table, Tag } from "antd";
import { useState } from "react";

import { createUser, listUsers } from "../../api/users";
import { listDepartments } from "../../api/departments";
import type { UserRole } from "../../types/user";

const ROLE_LABELS: Record<UserRole, string> = {
  admin: "Quản trị viên",
  department_staff: "Cán bộ phòng ban",
  technician: "Kỹ thuật viên",
};

export function UserListPage() {
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();
  const { message } = App.useApp();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ["users"], queryFn: listUsers });
  const { data: departments } = useQuery({ queryKey: ["departments"], queryFn: listDepartments });

  async function handleCreate(values: Parameters<typeof createUser>[0]) {
    try {
      await createUser(values);
      message.success("Đã tạo người dùng");
      setOpen(false);
      form.resetFields();
      queryClient.invalidateQueries({ queryKey: ["users"] });
    } catch {
      message.error("Không thể tạo người dùng (tên đăng nhập/email có thể đã tồn tại)");
    }
  }

  return (
    <>
      <Button type="primary" style={{ marginBottom: 16 }} onClick={() => setOpen(true)}>
        Thêm người dùng
      </Button>
      <Table
        rowKey="id"
        loading={isLoading}
        dataSource={data}
        columns={[
          { title: "Tên đăng nhập", dataIndex: "username" },
          { title: "Họ tên", dataIndex: "full_name" },
          { title: "Email", dataIndex: "email" },
          { title: "Vai trò", dataIndex: "role", render: (role: UserRole) => <Tag>{ROLE_LABELS[role]}</Tag> },
        ]}
      />
      <Modal title="Thêm người dùng" open={open} onCancel={() => setOpen(false)} onOk={() => form.submit()}>
        <Form layout="vertical" form={form} onFinish={handleCreate} initialValues={{ role: "department_staff" }}>
          <Form.Item name="username" label="Tên đăng nhập" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="full_name" label="Họ tên" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="email" label="Email" rules={[{ required: true, type: "email" }]}>
            <Input />
          </Form.Item>
          <Form.Item name="password" label="Mật khẩu" rules={[{ required: true, min: 8 }]}>
            <Input.Password />
          </Form.Item>
          <Form.Item name="role" label="Vai trò" rules={[{ required: true }]}>
            <Select
              options={Object.entries(ROLE_LABELS).map(([value, label]) => ({ value, label }))}
            />
          </Form.Item>
          <Form.Item name="department_id" label="Phòng ban">
            <Select allowClear options={departments?.map((d) => ({ value: d.id, label: d.name }))} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
