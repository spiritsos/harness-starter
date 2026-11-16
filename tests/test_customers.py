def test_first_page_has_next_cursor(client):
    res = client.get("/customers", params={"limit": 10})
    assert res.status_code == 200
    body = res.json()
    assert len(body["data"]) == 10
    assert body["meta"]["next_cursor"]


def test_cursor_walks_all_customers_without_duplicates(client):
    seen, cursor = [], None
    while True:
        params = {"limit": 7}
        if cursor:
            params["cursor"] = cursor
        body = client.get("/customers", params=params).json()
        seen += [c["id"] for c in body["data"]]
        cursor = body["meta"]["next_cursor"]
        if not cursor:
            break
    assert seen == list(range(1, 31))


def test_invalid_cursor_returns_400(client):
    assert client.get("/customers", params={"cursor": "not-a-cursor"}).status_code == 400


def test_get_customer_not_found(client):
    assert client.get("/customers/9999").status_code == 404
