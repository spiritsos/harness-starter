import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_DB", str(tmp_path / "test.db"))
    from scripts.seed import seed

    seed(customers=30, orders=150)
    from app.main import app

    return TestClient(app)
