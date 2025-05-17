def test_dashboard(client):
    token = get_auth_token(client)
    response = client.get(
        "/api/v1/dashboard/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "user" in response.json()
    assert "resume_count" in response.json()


def get_auth_token(client):
    client.post("/api/v1/auth/register", json={"email": "dash@example.com", "password": "123456"})
    res = client.post("/api/v1/auth/login", data={"username": "dash@example.com", "password": "123456"})
    return res.json()["access_token"]

