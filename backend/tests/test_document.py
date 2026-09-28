
def test_list_documents_require_api_key(client, auth_headers):
    response = client.get("/documents")

    assert response.status_code == 401

def test_get_by_id_not_found(client, auth_headers):
    response = client.get("/documents/9999", headers=auth_headers)

    assert response.status_code == 404

def test_get_by_id_found(client, auth_headers):
    response = client.get("/documents/1", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_list_stale_documents(client, auth_headers):
    response = client.get("/documents/stale", headers=auth_headers)
    assert response.status_code == 200

def test_list_documents_returns_paginated_envelope(client, auth_headers):
    response = client.get("/documents", headers=auth_headers)

    assert response.status_code == 200

    body = response.json()

    assert body["skip"] == 0
    assert body["limit"] == 10
    assert body["total"] == 4
    assert len(body["items"]) == 4