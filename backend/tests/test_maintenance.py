from datetime import date, timedelta


def test_create_maintenance_schedule(client, auth_headers, equipment):
    response = client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "record_type": "calibration",
            "scheduled_date": str(date.today() + timedelta(days=10)),
            "interval_days": 180,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "scheduled"
    assert body["equipment_code"] == "TB-001"


def test_complete_record_auto_creates_next_schedule(client, auth_headers, equipment):
    create_response = client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "record_type": "maintenance",
            "scheduled_date": str(date.today()),
            "interval_days": 90,
        },
    )
    record_id = create_response.json()["id"]

    complete_response = client.post(
        f"/api/v1/maintenance/{record_id}/complete",
        headers=auth_headers,
        json={"performed_by": "Nguyen Van A"},
    )
    assert complete_response.status_code == 200
    completed = complete_response.json()
    assert completed["status"] == "completed"
    assert completed["next_due_date"] == str(date.today() + timedelta(days=90))

    records = client.get(
        "/api/v1/maintenance", headers=auth_headers, params={"equipment_id": equipment.id}
    ).json()
    assert len(records) == 2
    scheduled = [r for r in records if r["status"] == "scheduled"]
    assert len(scheduled) == 1
    assert scheduled[0]["scheduled_date"] == str(date.today() + timedelta(days=90))
    assert scheduled[0]["interval_days"] == 90


def test_complete_without_interval_does_not_create_next(client, auth_headers, equipment):
    create_response = client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={"equipment_id": equipment.id, "record_type": "maintenance", "scheduled_date": str(date.today())},
    )
    record_id = create_response.json()["id"]
    client.post(f"/api/v1/maintenance/{record_id}/complete", headers=auth_headers, json={})

    records = client.get(
        "/api/v1/maintenance", headers=auth_headers, params={"equipment_id": equipment.id}
    ).json()
    assert len(records) == 1
    assert records[0]["status"] == "completed"


def test_cannot_complete_twice(client, auth_headers, equipment):
    create_response = client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={"equipment_id": equipment.id, "record_type": "maintenance", "scheduled_date": str(date.today())},
    )
    record_id = create_response.json()["id"]
    client.post(f"/api/v1/maintenance/{record_id}/complete", headers=auth_headers, json={})
    second = client.post(f"/api/v1/maintenance/{record_id}/complete", headers=auth_headers, json={})
    assert second.status_code == 400


def test_department_staff_cannot_create_schedule(client, auth_headers, equipment, department):
    client.post(
        "/api/v1/users",
        headers=auth_headers,
        json={
            "username": "canbo1",
            "email": "cb1@cdchaiphong.gov.vn",
            "full_name": "Can bo phong ban",
            "role": "department_staff",
            "department_id": department.id,
            "password": "matkhau123",
        },
    )
    login = client.post("/api/v1/auth/login", data={"username": "canbo1", "password": "matkhau123"})
    staff_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.post(
        "/api/v1/maintenance",
        headers=staff_headers,
        json={"equipment_id": equipment.id, "record_type": "maintenance", "scheduled_date": str(date.today())},
    )
    assert response.status_code == 403

    # but can still read
    response = client.get("/api/v1/maintenance", headers=staff_headers)
    assert response.status_code == 200


def test_alerts_only_include_scheduled_within_window(client, auth_headers, equipment):
    client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "record_type": "calibration",
            "scheduled_date": str(date.today() + timedelta(days=5)),
        },
    )
    client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "record_type": "calibration",
            "scheduled_date": str(date.today() + timedelta(days=200)),
        },
    )
    alerts = client.get("/api/v1/maintenance/alerts", headers=auth_headers).json()
    assert len(alerts) == 1
