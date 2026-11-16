"""DB 파일을 통째로 삭제하고 다시 만듭니다.

APP_DB 환경 변수가 가리키는 DB를 지웁니다. 공용 서버에서 실행하면 그 서버의 데이터가 사라집니다.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db import db_path  # noqa: E402
from scripts.seed import seed  # noqa: E402

if __name__ == "__main__":
    path = db_path()
    if path.exists():
        path.unlink()
        print(f"deleted: {path}")
    seed()
    print(f"recreated: {path}")
