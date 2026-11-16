# Lab 5: 장기 실행 하네스 루프 (Windows PowerShell)
# 세션마다 features.json에서 미완료 기능 하나만 구현 -> 테스트 -> 기록 -> 커밋한다.
# 실행: powershell -ExecutionPolicy Bypass -File .\run_agent.ps1 [-Runs 3]
param([int]$Runs = 3)

$Prompt = @"
progress.md, features.json, git log --oneline -10 을 읽고 상태를 파악하라.
passes가 false인 기능 중 가장 앞의 것 하나만 구현하라. 테스트를 먼저 작성하라.
빠른 테스트가 통과하면 features.json에서 그 기능의 passes만 true로 바꾸고,
progress.md 맨 위에 세션 기록을 추가한 뒤 git commit 하라.
다른 기능은 건드리지 마라. features.json의 항목이나 기준은 수정하지 마라.
"@

$Tools = "Read,Edit,Write,Glob,Grep,Bash(python -m pytest:*),Bash(ruff:*),Bash(git add:*),Bash(git commit:*),Bash(git log:*),Bash(git status)"

New-Item -ItemType Directory -Force logs | Out-Null
for ($i = 1; $i -le $Runs; $i++) {
    Write-Host "=== 세션 $i / $Runs ==="
    claude -p $Prompt --allowedTools $Tools --max-turns 40 --output-format json |
        Out-File -Encoding utf8 "logs/run-$i.json"
    if (-not (Select-String -Path features.json -Pattern '"passes": false' -Quiet)) {
        Write-Host "모든 기능 완료"
        break
    }
}
git log --oneline -5
