def get_auth_token(client):
    client.post("/api/v1/auth/register", json={"email": "test2@example.com", "password": "123456"})
    res = client.post("/api/v1/auth/login", data={"username": "test2@example.com", "password": "123456"})
    return res.json()["access_token"]

def test_create_resume(client):
    token = get_auth_token(client)
    response = client.post(
        "/api/v1/resume/",
        json={"content": "Sample resume content"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Sample resume content"
