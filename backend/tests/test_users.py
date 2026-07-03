def test_admin_can_create_user(client, auth_headers):
    response = client.post(
        "/api/v1/users",
        headers=auth_headers,
        json={
            "username": "kythuatvien1",
            "email": "kt1@cdchaiphong.gov.vn",
            "full_name": "Ky thuat vien 1",
            "role": "technician",
            "password": "matkhau123",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "technician"


def test_non_admin_cannot_list_users(client, auth_headers):
    client.post(
        "/api/v1/users",
        headers=auth_headers,
        json={
            "username": "canbo1",
            "email": "cb1@cdchaiphong.gov.vn",
            "full_name": "Can bo phong ban",
            "role": "department_staff",
            "password": "matkhau123",
        },
    )
    login = client.post("/api/v1/auth/login", data={"username": "canbo1", "password": "matkhau123"})
    token = login.json()["access_token"]

    response = client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_duplicate_username_rejected(client, auth_headers):
    payload = {
        "username": "dup",
        "email": "dup@cdchaiphong.gov.vn",
        "full_name": "Dup",
        "role": "technician",
        "password": "matkhau123",
    }
    client.post("/api/v1/users", headers=auth_headers, json=payload)
    response = client.post("/api/v1/users", headers=auth_headers, json=payload)
    assert response.status_code == 400
