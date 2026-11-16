import time

import pytest

from app.services import order_service


@pytest.mark.slow
def test_monthly_revenue_report_full_scan(client):
    # 실제 서비스에서는 외부 정산 시스템과 대조하느라 오래 걸리는 테스트입니다.
    time.sleep(20)
    orders = order_service.list_orders()
    totals = order_service.monthly_revenue_krw(orders)
    assert all(isinstance(v, int) for v in totals.values())
    assert sum(totals.values()) > 0
