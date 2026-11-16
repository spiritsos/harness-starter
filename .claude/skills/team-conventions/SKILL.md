---
name: team-conventions
description: Order Service의 API·서비스·모델 코드를 새로 작성하거나 수정·리뷰할 때 팀 컨벤션(계층 의존성, 금액 int, 커서 페이지네이션, 응답 형태) 위반을 검사한다. 엔드포인트 추가, 목록 API 변경, 금액 필드 변경 작업에서 사용한다.
---

# 팀 컨벤션 검사

1. 저장소 루트에서 검사 스크립트를 실행한다.
   `python .claude/skills/team-conventions/scripts/check_layers.py`
2. 스크립트가 보고한 위반을 파일·줄 단위로 정리한다.
3. 스크립트가 잡지 못하는 항목은 직접 확인한다.
   - 응답이 `{"data": ..., "meta": {...}}` 형태인가
   - 목록 API의 meta에 `next_cursor`, `limit`이 있는가
   - 새 엔드포인트에 tests/ 테스트가 있는가
4. 위반마다 수정안을 제시한다. 근거는 docs/conventions.md의 해당 절을 인용한다.

위반이 없으면 "컨벤션 위반 없음"과 확인한 항목 목록만 보고한다.
