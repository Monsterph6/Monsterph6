from datetime import date, timedelta


def test_create_borrow_marks_equipment_borrowed(client, auth_headers, equipment, department):
    response = client.post(
        "/api/v1/borrow",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "borrower_department_id": department.id,
            "purpose": "Xet nghiem luu dong",
            "expected_return_date": str(date.today() + timedelta(days=7)),
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "borrowed"
    assert body["code"].startswith("PM")
    assert body["equipment_code"] == "TB-001"
    assert body["borrower_department_name"] == "Khoa Xet nghiem"

    equipment_resp = client.get(f"/api/v1/equipment/{equipment.id}", headers=auth_headers)
    assert equipment_resp.json()["status"] == "borrowed"


def test_cannot_borrow_already_borrowed_equipment(client, auth_headers, equipment, department):
    payload = {"equipment_id": equipment.id, "borrower_department_id": department.id}
    client.post("/api/v1/borrow", headers=auth_headers, json=payload)
    second = client.post("/api/v1/borrow", headers=auth_headers, json=payload)
    assert second.status_code == 400


def test_create_borrow_requires_a_borrower(client, auth_headers, equipment):
    response = client.post(
        "/api/v1/borrow", headers=auth_headers, json={"equipment_id": equipment.id}
    )
    assert response.status_code == 422


def test_return_borrow_marks_equipment_active_again(client, auth_headers, equipment, department):
    create_response = client.post(
        "/api/v1/borrow",
        headers=auth_headers,
        json={"equipment_id": equipment.id, "borrower_department_id": department.id},
    )
    record_id = create_response.json()["id"]

    return_response = client.post(
        f"/api/v1/borrow/{record_id}/return",
        headers=auth_headers,
        json={"condition_on_return": "Binh thuong", "received_by": "Nguyen Van B"},
    )
    assert return_response.status_code == 200
    assert return_response.json()["status"] == "returned"

    equipment_resp = client.get(f"/api/v1/equipment/{equipment.id}", headers=auth_headers)
    assert equipment_resp.json()["status"] == "active"


def test_cannot_return_twice(client, auth_headers, equipment, department):
    create_response = client.post(
        "/api/v1/borrow",
        headers=auth_headers,
        json={"equipment_id": equipment.id, "borrower_department_id": department.id},
    )
    record_id = create_response.json()["id"]
    client.post(f"/api/v1/borrow/{record_id}/return", headers=auth_headers, json={})
    second = client.post(f"/api/v1/borrow/{record_id}/return", headers=auth_headers, json={})
    assert second.status_code == 400


def test_technician_cannot_create_borrow(client, auth_headers, equipment, department):
    client.post(
        "/api/v1/users",
        headers=auth_headers,
        json={
            "username": "kt1",
            "email": "kt1@cdchaiphong.gov.vn",
            "full_name": "Ky thuat vien 1",
            "role": "technician",
            "password": "matkhau123",
        },
    )
    login = client.post("/api/v1/auth/login", data={"username": "kt1", "password": "matkhau123"})
    tech_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.post(
        "/api/v1/borrow",
        headers=tech_headers,
        json={"equipment_id": equipment.id, "borrower_department_id": department.id},
    )
    assert response.status_code == 403

    # read access is still fine
    response = client.get("/api/v1/borrow", headers=tech_headers)
    assert response.status_code == 200


def test_overdue_borrow_detection(client, auth_headers, equipment, department):
    create_response = client.post(
        "/api/v1/borrow",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "borrower_department_id": department.id,
            "expected_return_date": str(date.today() - timedelta(days=2)),
        },
    )
    assert create_response.status_code == 201

    overdue = client.get("/api/v1/borrow/overdue", headers=auth_headers).json()
    assert len(overdue) == 1
    assert overdue[0]["equipment_id"] == equipment.id
