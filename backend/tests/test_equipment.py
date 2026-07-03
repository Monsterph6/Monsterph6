def test_create_and_get_equipment(client, auth_headers, department):
    response = client.post(
        "/api/v1/equipment",
        headers=auth_headers,
        json={"code": "TB-001", "name": "May xet nghiem PCR", "department_id": department.id},
    )
    assert response.status_code == 201
    equipment_id = response.json()["id"]

    response = client.get(f"/api/v1/equipment/{equipment_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["code"] == "TB-001"


def test_duplicate_equipment_code_rejected(client, auth_headers, department):
    payload = {"code": "TB-002", "name": "May do", "department_id": department.id}
    client.post("/api/v1/equipment", headers=auth_headers, json=payload)
    response = client.post("/api/v1/equipment", headers=auth_headers, json=payload)
    assert response.status_code == 400


def test_list_equipment_pagination(client, auth_headers, department):
    for i in range(3):
        client.post(
            "/api/v1/equipment",
            headers=auth_headers,
            json={"code": f"TB-{i}", "name": "Thiet bi", "department_id": department.id},
        )
    response = client.get("/api/v1/equipment", headers=auth_headers, params={"page": 1, "page_size": 2})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    assert len(body["items"]) == 2


def test_equipment_requires_auth(client):
    response = client.get("/api/v1/equipment")
    assert response.status_code == 401
