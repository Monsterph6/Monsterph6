import { useQuery } from "@tanstack/react-query";
import { App, Button, Card, DatePicker, Select, Space, Typography } from "antd";
import { FileExcelOutlined, FilePdfOutlined } from "@ant-design/icons";
import { useState } from "react";
import type { Dayjs } from "dayjs";

import { listDepartments } from "../../api/departments";
import {
  downloadBorrowReport,
  downloadEquipmentReport,
  downloadMaintenanceReport,
} from "../../api/reports";

const EQUIPMENT_STATUS_OPTIONS = [
  { value: "active", label: "Đang hoạt động" },
  { value: "in_maintenance", label: "Đang bảo trì" },
  { value: "borrowed", label: "Đang được mượn" },
  { value: "broken", label: "Hỏng" },
  { value: "retired", label: "Ngừng sử dụng" },
];

const MAINTENANCE_TYPE_OPTIONS = [
  { value: "maintenance", label: "Bảo trì" },
  { value: "calibration", label: "Hiệu chuẩn" },
];

const MAINTENANCE_STATUS_OPTIONS = [
  { value: "scheduled", label: "Sắp tới / Quá hạn" },
  { value: "completed", label: "Đã hoàn thành" },
  { value: "cancelled", label: "Đã hủy" },
];

const BORROW_STATUS_OPTIONS = [
  { value: "borrowed", label: "Đang mượn / Quá hạn" },
  { value: "returned", label: "Đã trả" },
];

function EquipmentReportCard({ departments }: { departments: { id: number; name: string }[] | undefined }) {
  const { message } = App.useApp();
  const [departmentId, setDepartmentId] = useState<number>();
  const [status, setStatus] = useState<string>();
  const [loading, setLoading] = useState(false);

  async function handleDownload(format: "xlsx" | "pdf") {
    setLoading(true);
    try {
      await downloadEquipmentReport({ format, department_id: departmentId, status });
    } catch {
      message.error("Không thể xuất báo cáo");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card title="Danh mục thiết bị">
      <Space direction="vertical" style={{ width: "100%" }}>
        <Space wrap>
          <Select
            allowClear
            placeholder="Phòng ban"
            style={{ width: 220 }}
            options={departments?.map((d) => ({ value: d.id, label: d.name }))}
            onChange={setDepartmentId}
          />
          <Select
            allowClear
            placeholder="Trạng thái"
            style={{ width: 200 }}
            options={EQUIPMENT_STATUS_OPTIONS}
            onChange={setStatus}
          />
        </Space>
        <Space>
          <Button icon={<FileExcelOutlined />} loading={loading} onClick={() => handleDownload("xlsx")}>
            Xuất Excel
          </Button>
          <Button icon={<FilePdfOutlined />} loading={loading} onClick={() => handleDownload("pdf")}>
            Xuất PDF
          </Button>
        </Space>
      </Space>
    </Card>
  );
}

function MaintenanceReportCard({ departments }: { departments: { id: number; name: string }[] | undefined }) {
  const { message } = App.useApp();
  const [departmentId, setDepartmentId] = useState<number>();
  const [recordType, setRecordType] = useState<string>();
  const [status, setStatus] = useState<string>();
  const [dateRange, setDateRange] = useState<[Dayjs, Dayjs] | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleDownload(format: "xlsx" | "pdf") {
    setLoading(true);
    try {
      await downloadMaintenanceReport({
        format,
        department_id: departmentId,
        record_type: recordType,
        status,
        date_from: dateRange?.[0].format("YYYY-MM-DD"),
        date_to: dateRange?.[1].format("YYYY-MM-DD"),
      });
    } catch {
      message.error("Không thể xuất báo cáo");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card title="Lịch sử bảo trì/hiệu chuẩn">
      <Space direction="vertical" style={{ width: "100%" }}>
        <Space wrap>
          <Select
            allowClear
            placeholder="Phòng ban"
            style={{ width: 220 }}
            options={departments?.map((d) => ({ value: d.id, label: d.name }))}
            onChange={setDepartmentId}
          />
          <Select
            allowClear
            placeholder="Loại"
            style={{ width: 160 }}
            options={MAINTENANCE_TYPE_OPTIONS}
            onChange={setRecordType}
          />
          <Select
            allowClear
            placeholder="Trạng thái"
            style={{ width: 200 }}
            options={MAINTENANCE_STATUS_OPTIONS}
            onChange={setStatus}
          />
          <DatePicker.RangePicker
            format="DD/MM/YYYY"
            onChange={(v) => setDateRange(v as [Dayjs, Dayjs] | null)}
          />
        </Space>
        <Space>
          <Button icon={<FileExcelOutlined />} loading={loading} onClick={() => handleDownload("xlsx")}>
            Xuất Excel
          </Button>
          <Button icon={<FilePdfOutlined />} loading={loading} onClick={() => handleDownload("pdf")}>
            Xuất PDF
          </Button>
        </Space>
      </Space>
    </Card>
  );
}

function BorrowReportCard({ departments }: { departments: { id: number; name: string }[] | undefined }) {
  const { message } = App.useApp();
  const [departmentId, setDepartmentId] = useState<number>();
  const [status, setStatus] = useState<string>();
  const [dateRange, setDateRange] = useState<[Dayjs, Dayjs] | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleDownload(format: "xlsx" | "pdf") {
    setLoading(true);
    try {
      await downloadBorrowReport({
        format,
        department_id: departmentId,
        status,
        date_from: dateRange?.[0].format("YYYY-MM-DD"),
        date_to: dateRange?.[1].format("YYYY-MM-DD"),
      });
    } catch {
      message.error("Không thể xuất báo cáo");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card title="Lịch sử mượn/trả thiết bị">
      <Space direction="vertical" style={{ width: "100%" }}>
        <Space wrap>
          <Select
            allowClear
            placeholder="Phòng ban"
            style={{ width: 220 }}
            options={departments?.map((d) => ({ value: d.id, label: d.name }))}
            onChange={setDepartmentId}
          />
          <Select
            allowClear
            placeholder="Trạng thái"
            style={{ width: 200 }}
            options={BORROW_STATUS_OPTIONS}
            onChange={setStatus}
          />
          <DatePicker.RangePicker
            format="DD/MM/YYYY"
            onChange={(v) => setDateRange(v as [Dayjs, Dayjs] | null)}
          />
        </Space>
        <Space>
          <Button icon={<FileExcelOutlined />} loading={loading} onClick={() => handleDownload("xlsx")}>
            Xuất Excel
          </Button>
          <Button icon={<FilePdfOutlined />} loading={loading} onClick={() => handleDownload("pdf")}>
            Xuất PDF
          </Button>
        </Space>
      </Space>
    </Card>
  );
}

export function ReportsPage() {
  const { data: departments } = useQuery({ queryKey: ["departments"], queryFn: listDepartments });

  return (
    <Space direction="vertical" style={{ width: "100%" }} size="middle">
      <Typography.Title level={4}>Báo cáo</Typography.Title>
      <EquipmentReportCard departments={departments} />
      <MaintenanceReportCard departments={departments} />
      <BorrowReportCard departments={departments} />
    </Space>
  );
}
