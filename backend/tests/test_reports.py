from datetime import date, timedelta


def test_equipment_report_excel(client, auth_headers, equipment):
    response = client.get("/api/v1/reports/equipment", headers=auth_headers, params={"format": "xlsx"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/vnd.openxmlformats")
    assert len(response.content) > 0


def test_equipment_report_pdf(client, auth_headers, equipment):
    response = client.get("/api/v1/reports/equipment", headers=auth_headers, params={"format": "pdf"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_equipment_report_empty_pdf_still_works(client, auth_headers):
    response = client.get(
        "/api/v1/reports/equipment", headers=auth_headers, params={"format": "pdf", "status": "retired"}
    )
    assert response.status_code == 200
    assert response.content.startswith(b"%PDF")


def test_maintenance_report_with_date_range(client, auth_headers, equipment):
    client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "record_type": "calibration",
            "scheduled_date": str(date.today()),
        },
    )
    client.post(
        "/api/v1/maintenance",
        headers=auth_headers,
        json={
            "equipment_id": equipment.id,
            "record_type": "calibration",
            "scheduled_date": str(date.today() + timedelta(days=100)),
        },
    )

    response = client.get(
        "/api/v1/reports/maintenance",
        headers=auth_headers,
        params={
            "format": "xlsx",
            "date_from": str(date.today() - timedelta(days=1)),
            "date_to": str(date.today() + timedelta(days=1)),
        },
    )
    assert response.status_code == 200
    assert len(response.content) > 0


def test_borrow_report_pdf(client, auth_headers, equipment, department):
    client.post(
        "/api/v1/borrow",
        headers=auth_headers,
        json={"equipment_id": equipment.id, "borrower_department_id": department.id},
    )
    response = client.get(
        "/api/v1/reports/borrow",
        headers=auth_headers,
        params={"format": "pdf", "department_id": department.id},
    )
    assert response.status_code == 200
    assert response.content.startswith(b"%PDF")


def test_reports_require_auth(client):
    response = client.get("/api/v1/reports/equipment")
    assert response.status_code == 401
