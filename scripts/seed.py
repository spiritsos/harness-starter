"""DB가 없으면 스키마를 만들고 샘플 데이터를 넣습니다.

이미 데이터가 있으면 아무것도 하지 않습니다.
"""

import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import apply_migrations, db_path, get_connection  # noqa: E402

STATUSES = ["PENDING", "PAID", "PAID", "SHIPPED", "SHIPPED", "CANCELLED"]


def seed(customers: int = 30, orders: int = 150, rng_seed: int = 42) -> None:
    rng = random.Random(rng_seed)
    start = datetime(2026, 5, 1)
    with get_connection() as conn:
        apply_migrations(conn)
        if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]:
            return
        for i in range(1, customers + 1):
            created = start + timedelta(days=rng.randint(0, 30))
            conn.execute(
                "INSERT INTO customers (id, name, email, created_at) VALUES (?, ?, ?, ?)",
                (i, f"고객{i:03d}", f"customer{i:03d}@example.com", created.isoformat()),
            )
        for i in range(1, orders + 1):
            created = start + timedelta(days=rng.randint(0, 180), minutes=rng.randint(0, 1440))
            conn.execute(
                "INSERT INTO orders (id, customer_id, status, amount_krw, created_at)"
                " VALUES (?, ?, ?, ?, ?)",
                (
                    i,
                    rng.randint(1, customers),
                    rng.choice(STATUSES),
                    rng.randrange(5_000, 500_000, 100),
                    created.isoformat(),
                ),
            )
        conn.commit()


if __name__ == "__main__":
    seed()
    print(f"seeded: {db_path()}")
