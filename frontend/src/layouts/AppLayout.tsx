import {
  DashboardOutlined,
  LogoutOutlined,
  ToolOutlined,
  ApartmentOutlined,
  TeamOutlined,
  ScheduleOutlined,
  SwapOutlined,
} from "@ant-design/icons";
import { Layout, Menu, Typography } from "antd";
import { Outlet, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

const { Header, Sider, Content } = Layout;

export function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const items = [
    { key: "/", icon: <DashboardOutlined />, label: "Tổng quan" },
    { key: "/equipment", icon: <ToolOutlined />, label: "Thiết bị" },
    { key: "/maintenance", icon: <ScheduleOutlined />, label: "Lịch bảo trì/hiệu chuẩn" },
    { key: "/borrow", icon: <SwapOutlined />, label: "Mượn/trả thiết bị" },
    ...(user?.role === "admin"
      ? [
          { key: "/departments", icon: <ApartmentOutlined />, label: "Phòng ban" },
          { key: "/users", icon: <TeamOutlined />, label: "Người dùng" },
        ]
      : []),
  ];

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div style={{ color: "#fff", padding: 16, fontWeight: 600 }}>CDC Hải Phòng</div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={items}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header style={{ background: "#fff", display: "flex", justifyContent: "flex-end", alignItems: "center", gap: 16 }}>
          <Typography.Text>{user?.full_name}</Typography.Text>
          <LogoutOutlined onClick={logout} style={{ cursor: "pointer" }} title="Đăng xuất" />
        </Header>
        <Content style={{ margin: 16 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
