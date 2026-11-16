#!/usr/bin/env bash
# Lab 5: 장기 실행 하네스 루프 (macOS / Linux / Git Bash)
# 세션마다 features.json에서 미완료 기능 하나만 구현 → 테스트 → 기록 → 커밋한다.
set -euo pipefail

RUNS="${1:-3}"
PROMPT='progress.md, features.json, `git log --oneline -10` 을 읽고 상태를 파악하라.
passes가 false인 기능 중 가장 앞의 것 하나만 구현하라. 테스트를 먼저 작성하라.
빠른 테스트가 통과하면 features.json에서 그 기능의 passes만 true로 바꾸고,
progress.md 맨 위에 세션 기록을 추가한 뒤 git commit 하라.
다른 기능은 건드리지 마라. features.json의 항목이나 기준은 수정하지 마라.'

mkdir -p logs
for i in $(seq 1 "$RUNS"); do
  echo "=== 세션 $i / $RUNS ==="
  claude -p "$PROMPT" \
    --allowedTools "Read,Edit,Write,Glob,Grep,Bash(python -m pytest:*),Bash(ruff:*),Bash(git add:*),Bash(git commit:*),Bash(git log:*),Bash(git status)" \
    --max-turns 40 \
    --output-format json > "logs/run-$i.json"
  if ! grep -q '"passes": false' features.json; then
    echo "모든 기능 완료"
    break
  fi
done
git log --oneline -5
