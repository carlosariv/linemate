
def test_list_tickets_require_api_key(client, auth_headers):
    response = client.get("/tickets")

    assert response.status_code == 401

def test_get_by_id_not_found(client, auth_headers):
    response = client.get("/tickets/9999", headers=auth_headers)

    assert response.status_code == 404

def test_get_by_id_found(client, auth_headers):
    response = client.get("/tickets/1", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_list_mismatches_endpoint_available(client, auth_headers):
    response = client.get("/tickets/mismatches", headers=auth_headers)
    assert response.status_code == 200

def test_list_tickets_returns_page_envelope(client, auth_headers):
    response = client.get("/tickets", headers=auth_headers)

    assert response.status_code == 200

    body = response.json()

    assert body["skip"] == 0
    assert body["limit"] == 10
    assert body["total"] == 3
    assert len(body["items"]) == 3