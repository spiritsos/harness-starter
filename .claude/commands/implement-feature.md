---
description: 스펙을 받아 계획 → 테스트 → 구현 → 검증 → 리뷰 순으로 기능을 구현한다
---

다음 기능을 구현하라: $ARGUMENTS

1. 관련 코드와 docs/conventions.md를 읽고, 변경할 파일과 접근 방식을 계획으로 먼저 제시한 뒤 승인을 기다린다.
2. 승인되면 tests/에 실패하는 테스트를 먼저 작성한다.
3. 계층 규칙(api → services → repositories)을 지켜 구현한다.
4. `python -m pytest -m "not slow" -q` 와 `ruff check .` 를 통과시킨다.
5. code-reviewer 서브에이전트로 리뷰를 받고, 높음·중간 지적을 반영한다.
6. 변경 요약, 테스트 결과, 남은 위험을 보고한다.
