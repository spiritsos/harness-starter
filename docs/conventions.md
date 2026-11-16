# Order Service 컨벤션

## 계층
| 계층 | 역할 | 의존 가능 |
|---|---|---|
| `app/api` | HTTP 입출력, 검증, 상태 코드 | services, models, pagination |
| `app/services` | 비즈니스 규칙 | repositories, models, pagination |
| `app/repositories` | SQL | db |

API 계층에서 `sqlite3`, `app.db`, `app.repositories`를 import하지 않는다.

## 금액
- 필드명은 `amount_krw`, 타입은 `int` (원 단위).
- 합계·집계도 int로 유지한다. 반올림 문제가 생기는 float를 쓰지 않는다.

## 페이지네이션
- 팀 표준은 커서 방식이다. 참고 구현: `GET /customers`, `app/services/customer_service.py`.
- 요청: `?cursor=<opaque>&limit=<1..100>` (기본 20).
- 응답 meta: `{"next_cursor": str | null, "limit": int}`.
- 이유: 주문은 계속 추가되므로 offset 방식은 페이지 사이에 중복·누락이 생기고, 데이터가 많을수록 느리다.

## 응답 형태
- 성공: `{"data": ..., "meta": {...}}`
- 오류: FastAPI `HTTPException` (`{"detail": "..."}`)

## 마이그레이션
- `migrations/NNN_name.sql` 순서대로 적용된다.
- 이미 적용된 파일은 수정하지 않는다. 새 번호로 추가한다.

## 테스트
- 엔드포인트마다 정상·경계·오류 케이스를 둔다.
- `@pytest.mark.slow`는 외부 시스템 대조 등 오래 걸리는 테스트에만 붙인다.
