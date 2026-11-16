"""PreToolUse Hook: 위험 명령과 보호 파일 접근을 차단한다.

차단 시 stderr에 이유와 대안을 쓰고 종료 코드 2를 반환한다.
Claude Code는 이 메시지를 에이전트에게 전달하고, 에이전트는 다른 방법을 찾는다.
"""

import json
import re
import sys
from pathlib import Path

DANGEROUS_COMMANDS = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r", "재귀 강제 삭제(rm -rf)"),
    (r"\bgit\s+push\b.*(--force|\s-f\b)", "강제 푸시"),
    (r"\bgit\s+reset\s+--hard", "작업 내용을 지우는 git reset --hard"),
    (r"reset_db\.py", "DB 전체 삭제 스크립트"),
    (r"\bDROP\s+TABLE\b", "테이블 삭제"),
    (r"(^|[\s/\\])\.env(\b|$)", ".env 비밀 파일 접근"),
]

FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit"}


def block(reason: str, alternative: str) -> None:
    print(f"차단됨: {reason}. {alternative}", file=sys.stderr)
    sys.exit(2)


def main() -> None:
    data = json.load(sys.stdin)
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}

    if tool == "Bash":
        command = tool_input.get("command", "")
        for pattern, label in DANGEROUS_COMMANDS:
            if re.search(pattern, command, flags=re.IGNORECASE):
                block(label, "안전한 대안을 제안하거나, 꼭 필요하면 사람에게 직접 실행을 요청하라.")

    if tool in FILE_TOOLS:
        path = Path(tool_input.get("file_path", ""))
        if path.name == ".env" or path.name.startswith(".env."):
            block(".env 비밀 파일 접근", "설정 값이 필요하면 사람에게 물어라.")
        if tool != "Read" and path.parent.name == "migrations" and path.exists():
            block(
                f"이미 적용된 마이그레이션 수정({path.name})",
                "스키마 변경은 migrations/에 새 번호 파일(예: 002_xxx.sql)로 추가하라.",
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
