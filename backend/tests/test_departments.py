def test_department_code_is_normalized(client, auth_headers):
    response = client.post(
        "/api/v1/departments",
        headers=auth_headers,
        json={"code": "Khoa Xét Nghiệm", "name": "Khoa Xét nghiệm"},
    )
    assert response.status_code == 201
    assert response.json()["code"] == "KHOA-XET-NGHIEM"
    assert response.json()["name"] == "Khoa Xét nghiệm"


def test_equipment_code_is_normalized(client, auth_headers, department):
    response = client.post(
        "/api/v1/equipment",
        headers=auth_headers,
        json={"code": "Máy Đo Huyết Áp", "name": "May do huyet ap", "department_id": department.id},
    )
    assert response.status_code == 201
    assert response.json()["code"] == "MAY-DO-HUYET-AP"
