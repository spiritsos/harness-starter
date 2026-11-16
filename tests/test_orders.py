def test_list_orders_returns_envelope(client):
    body = client.get("/orders").json()
    assert set(body) == {"data", "meta"}
    assert body["meta"]["count"] == len(body["data"]) == 150


def test_amount_is_integer_krw(client):
    order = client.get("/orders/1").json()["data"]
    assert isinstance(order["amount_krw"], int)


def test_get_order_not_found(client):
    assert client.get("/orders/99999").status_code == 404
