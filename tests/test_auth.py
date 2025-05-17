def test_dashboard(client, get_auth_token):
    token = get_auth_token()
    response = client.get(
        "/api/v1/dashboard/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "user" in json_data
    assert "resume_count" in json_data
