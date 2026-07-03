import { App, Button, Card, Form, Input, Typography } from "antd";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const { message } = App.useApp();
  const [submitting, setSubmitting] = useState(false);

  async function handleFinish(values: { username: string; password: string }) {
    setSubmitting(true);
    try {
      await login(values.username, values.password);
      navigate("/");
    } catch {
      message.error("Sai tên đăng nhập hoặc mật khẩu");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh" }}>
      <Card style={{ width: 360 }}>
        <Typography.Title level={4} style={{ textAlign: "center" }}>
          Quản lý trang thiết bị
          <br />
          CDC Hải Phòng
        </Typography.Title>
        <Form layout="vertical" onFinish={handleFinish}>
          <Form.Item name="username" label="Tên đăng nhập" rules={[{ required: true }]}>
            <Input autoFocus />
          </Form.Item>
          <Form.Item name="password" label="Mật khẩu" rules={[{ required: true }]}>
            <Input.Password />
          </Form.Item>
          <Button type="primary" htmlType="submit" block loading={submitting}>
            Đăng nhập
          </Button>
        </Form>
      </Card>
    </div>
  );
}
