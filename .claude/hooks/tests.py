"""Stop Hook: 코드가 바뀌었으면 빠른 테스트가 통과해야만 작업을 끝낼 수 있게 한다 (백프레셔).

- 변경 사항이 없으면(질문·설명만 한 경우) 그냥 통과한다.
- stop_hook_active가 true면 이미 한 번 되돌려 보낸 상태이므로 무한 루프를 막기 위해 통과한다.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def main() -> None:
    data = json.load(sys.stdin)
    if data.get("stop_hook_active"):
        sys.exit(0)

    status = run(["git", "status", "--porcelain"])
    if status.returncode == 0 and not status.stdout.strip():
        sys.exit(0)

    result = run([sys.executable, "-m", "pytest", "-m", "not slow", "-q", "-x"])
    if result.returncode != 0:
        tail = "\n".join((result.stdout + result.stderr).strip().splitlines()[-30:])
        print("테스트 실패. 원인을 고친 뒤 다시 완료하라:\n" + tail, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
