import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIGRATIONS = ROOT / "migrations"


def db_path() -> Path:
    return Path(os.environ.get("APP_DB", ROOT / "data" / "app.db"))


def get_connection() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def apply_migrations(conn: sqlite3.Connection) -> None:
    for sql_file in sorted(MIGRATIONS.glob("*.sql")):
        conn.executescript(sql_file.read_text(encoding="utf-8"))
    conn.commit()
