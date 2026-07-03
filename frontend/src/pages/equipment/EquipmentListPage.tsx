import { useQuery } from "@tanstack/react-query";
import { Button, Input, Space, Table } from "antd";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { listEquipment } from "../../api/equipment";
import { EquipmentStatusTag } from "../../components/EquipmentStatusTag";
import type { Equipment } from "../../types/equipment";

export function EquipmentListPage() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const pageSize = 20;

  const { data, isLoading } = useQuery({
    queryKey: ["equipment", { page, search }],
    queryFn: () => listEquipment({ page, page_size: pageSize, search: search || undefined }),
  });

  const columns = [
    { title: "Mã thiết bị", dataIndex: "code" },
    { title: "Tên thiết bị", dataIndex: "name" },
    { title: "Nhà sản xuất", dataIndex: "manufacturer" },
    { title: "Vị trí", dataIndex: "location" },
    {
      title: "Trạng thái",
      dataIndex: "status",
      render: (status: Equipment["status"]) => <EquipmentStatusTag status={status} />,
    },
    {
      title: "",
      key: "actions",
      render: (_: unknown, record: Equipment) => (
        <a onClick={() => navigate(`/equipment/${record.id}/edit`)}>Sửa</a>
      ),
    },
  ];

  return (
    <Space direction="vertical" style={{ width: "100%" }} size="middle">
      <Space style={{ justifyContent: "space-between", width: "100%" }}>
        <Input.Search
          placeholder="Tìm theo mã hoặc tên thiết bị"
          onSearch={(value) => {
            setPage(1);
            setSearch(value);
          }}
          style={{ width: 320 }}
          allowClear
        />
        <Button type="primary" onClick={() => navigate("/equipment/new")}>
          Thêm thiết bị
        </Button>
      </Space>
      <Table
        rowKey="id"
        loading={isLoading}
        columns={columns}
        dataSource={data?.items ?? []}
        pagination={{
          current: page,
          pageSize,
          total: data?.total ?? 0,
          onChange: setPage,
        }}
      />
    </Space>
  );
}
