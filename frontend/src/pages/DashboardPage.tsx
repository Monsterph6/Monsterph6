import { useQuery } from "@tanstack/react-query";
import { Alert, Card, Col, Row, Space, Statistic } from "antd";

import { listOverdueBorrows } from "../api/borrow";
import { listEquipment } from "../api/equipment";
import { listMaintenanceAlerts } from "../api/maintenance";

export function DashboardPage() {
  const { data: equipmentData } = useQuery({
    queryKey: ["equipment", "dashboard-count"],
    queryFn: () => listEquipment({ page: 1, page_size: 1 }),
  });

  const { data: alerts } = useQuery({
    queryKey: ["maintenance-alerts"],
    queryFn: listMaintenanceAlerts,
  });

  const { data: overdueBorrows } = useQuery({
    queryKey: ["borrow-overdue"],
    queryFn: listOverdueBorrows,
  });

  return (
    <>
      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <Statistic title="Tổng số thiết bị" value={equipmentData?.total ?? 0} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Lịch bảo trì/hiệu chuẩn sắp tới (30 ngày)" value={alerts?.length ?? 0} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Thiết bị quá hạn trả" value={overdueBorrows?.length ?? 0} />
          </Card>
        </Col>
      </Row>
      <Space direction="vertical" style={{ width: "100%", marginTop: 16 }}>
        {alerts && alerts.length > 0 && (
          <Alert
            type="warning"
            showIcon
            message={`Có ${alerts.length} lịch bảo trì/hiệu chuẩn cần chú ý trong 30 ngày tới`}
          />
        )}
        {overdueBorrows && overdueBorrows.length > 0 && (
          <Alert
            type="error"
            showIcon
            message={`Có ${overdueBorrows.length} thiết bị đang mượn đã quá hạn trả`}
          />
        )}
      </Space>
    </>
  );
}
