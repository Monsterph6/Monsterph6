import { useQuery, useQueryClient } from "@tanstack/react-query";
import { App, Button, Form, Input, Modal, Table } from "antd";
import { useState } from "react";

import { createDepartment, listDepartments } from "../../api/departments";

export function DepartmentListPage() {
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();
  const { message } = App.useApp();
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({ queryKey: ["departments"], queryFn: listDepartments });

  async function handleCreate(values: { code: string; name: string }) {
    try {
      await createDepartment(values);
      message.success("Đã thêm phòng ban");
      setOpen(false);
      form.resetFields();
      queryClient.invalidateQueries({ queryKey: ["departments"] });
    } catch {
      message.error("Không thể thêm phòng ban (mã có thể đã tồn tại)");
    }
  }

  return (
    <>
      <Button type="primary" style={{ marginBottom: 16 }} onClick={() => setOpen(true)}>
        Thêm phòng ban
      </Button>
      <Table
        rowKey="id"
        loading={isLoading}
        dataSource={data}
        columns={[
          { title: "Mã", dataIndex: "code" },
          { title: "Tên phòng ban", dataIndex: "name" },
        ]}
      />
      <Modal
        title="Thêm phòng ban"
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => form.submit()}
      >
        <Form layout="vertical" form={form} onFinish={handleCreate}>
          <Form.Item name="code" label="Mã phòng ban" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="name" label="Tên phòng ban" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
