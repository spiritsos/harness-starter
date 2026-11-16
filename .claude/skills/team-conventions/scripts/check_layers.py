"""Order Service 컨벤션 정적 검사.

- app/api 에서 sqlite3 · app.db · app.repositories import 금지
- amount 가 들어간 필드는 int 여야 함
- app/api 의 핸들러에 offset · page 파라미터 금지 (커서 페이지네이션만 허용)

위반이 있으면 목록을 출력하고 종료 코드 1을 반환합니다.
"""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FORBIDDEN_IN_API = ("sqlite3", "app.db", "app.repositories")
FORBIDDEN_PARAMS = {"offset", "page", "page_size"}


def imported_modules(tree: ast.AST) -> list[tuple[int, str]]:
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found += [(node.lineno, alias.name) for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.append((node.lineno, node.module))
            found += [(node.lineno, f"{node.module}.{a.name}") for a in node.names]
    return found


def check_api(path: Path, tree: ast.AST) -> list[str]:
    errors = []
    for lineno, module in imported_modules(tree):
        if any(module == f or module.startswith(f + ".") for f in FORBIDDEN_IN_API):
            errors.append(f"{path}:{lineno} API 계층에서 '{module}' import 금지 (services 경유)")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in node.args.args + node.args.kwonlyargs:
                if arg.arg in FORBIDDEN_PARAMS:
                    errors.append(
                        f"{path}:{node.lineno} '{node.name}'의 '{arg.arg}' 파라미터: "
                        "offset/page 방식 금지, 커서 페이지네이션 사용"
                    )
    return errors


def check_amounts(path: Path, tree: ast.AST) -> list[str]:
    errors = []
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
            annotation = ast.unparse(node.annotation)
            if "amount" in name and annotation != "int":
                errors.append(f"{path}:{node.lineno} '{name}: {annotation}' 금액은 int(원 단위)")
    return errors


def main() -> int:
    errors: list[str] = []
    for path in sorted((ROOT / "app").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        rel = path.relative_to(ROOT)
        if rel.parts[:2] == ("app", "api"):
            errors += check_api(rel, tree)
        errors += check_amounts(rel, tree)
    if errors:
        print("컨벤션 위반:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print("컨벤션 위반 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
