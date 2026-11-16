# Order Service

FastAPI + SQLite 주문 관리 API. 계층 구조: `app/api` → `app/services` → `app/repositories` → DB.
상세 컨벤션은 docs/conventions.md 참고.

## 명령
- 빠른 테스트: `python -m pytest -m "not slow" -q` — 작업 완료 전 반드시 통과
- 전체 테스트: `python -m pytest` — slow 테스트는 20초 이상 걸림. CI에서만 실행
- 린트·포맷: `ruff check . --fix` 와 `ruff format .`
- 로컬 DB 준비: `python scripts/seed.py`

## 규칙
- `app/api`에서 DB·repositories 직접 사용 금지. 반드시 services를 거친다
- 금액은 `amount_krw: int` (원 단위). float·Decimal 금지
- 목록 API는 커서 페이지네이션(`app/pagination.py`)만 사용. offset/page 방식 금지
- 응답은 항상 `{"data": ..., "meta": {...}}` 형태
- `migrations/`의 기존 파일 수정 금지. 스키마 변경은 새 번호 파일로
- 새 엔드포인트에는 tests/에 테스트 필수
- `scripts/reset_db.py` 실행 금지. `.env` 열람 금지

## 장기 실행 작업 (features.json)
- 시작 시 progress.md, features.json, `git log --oneline -10`을 먼저 읽는다
- 한 세션에 기능 하나만. features.json은 `passes` 값만 바꾼다 (항목·기준 수정 금지)
- 테스트 통과 후에만 passes: true → progress.md 기록 → git commit

## 완료의 정의
빠른 테스트 통과 + ruff 통과 + 변경 요약과 남은 위험 보고
