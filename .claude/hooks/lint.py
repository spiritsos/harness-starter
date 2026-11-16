"""PostToolUse Hook: Python 파일 편집 직후 포맷·린트·컨벤션 검사를 실행한다.

자동으로 고칠 수 없는 문제가 남으면 stderr로 알려 주고 종료 코드 2를 반환한다.
에이전트는 이 피드백을 받아 바로 수정한다.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))
CHECKER = ROOT / ".claude" / "skills" / "team-conventions" / "scripts" / "check_layers.py"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def main() -> None:
    data = json.load(sys.stdin)
    file_path = (data.get("tool_input") or {}).get("file_path", "")
    if not file_path.endswith(".py"):
        sys.exit(0)

    problems = []
    try:
        run(["ruff", "format", file_path])
        result = run(["ruff", "check", "--fix", file_path])
        if result.returncode != 0:
            problems.append("ruff 린트 오류:\n" + result.stdout.strip()[-2000:])
    except FileNotFoundError:
        pass  # ruff가 설치되지 않은 환경에서는 건너뛴다

    if CHECKER.exists() and "app" in Path(file_path).parts:
        result = run([sys.executable, str(CHECKER)])
        if result.returncode != 0:
            problems.append(result.stdout.strip())

    if problems:
        print("\n\n".join(problems) + "\n\n위 문제를 고친 뒤 계속하라.", file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
