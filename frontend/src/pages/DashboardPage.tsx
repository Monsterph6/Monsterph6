import { useQuery } from "@tanstack/react-query";
import { Alert, Card, Col, Row, Statistic } from "antd";

import { apiClient } from "../api/client";
import { listEquipment } from "../api/equipment";

interface MaintenanceAlert {
  id: number;
  equipment_id: number;
  record_type: string;
  scheduled_date: string;
  status: string;
}

export function DashboardPage() {
  const { data: equipmentData } = useQuery({
    queryKey: ["equipment", "dashboard-count"],
    queryFn: () => listEquipment({ page: 1, page_size: 1 }),
  });

  const { data: alerts } = useQuery({
    queryKey: ["maintenance-alerts"],
    queryFn: async () => {
      const { data } = await apiClient.get<MaintenanceAlert[]>("/maintenance/alerts");
      return data;
    },
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
      </Row>
      {alerts && alerts.length > 0 && (
        <Alert
          style={{ marginTop: 16 }}
          type="warning"
          showIcon
          message={`Có ${alerts.length} lịch bảo trì/hiệu chuẩn cần chú ý trong 30 ngày tới`}
          description="Chi tiết đầy đủ và quản lý lịch sẽ có ở giai đoạn tiếp theo (Phase 2)."
        />
      )}
    </>
  );
}
