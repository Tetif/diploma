# Ночная очередь: все 4 influence-метода (Influence, Arnoldi, Lissa, Nystroem).
# Запуск из корня репо: .\.venv\Scripts\python.exe не нужен — скрипт сам вызывает runner.
# ВАЖНО: не редактировать код репозитория во время прогона (uvicorn reload).

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot\..

$log = "docs\overnight_run_log.txt"
function Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
    Add-Content -Path $log -Value $line
    Write-Host $line
}

$py = ".\.venv\Scripts\python.exe"
$runner = "scripts\influence_investigation_runner.py"

Log "=== Overnight multi-method queue start ==="

$jobs = @(
    # wine-multi (WM1) уже выполнен вручную 2026-05-19 ~02:56
    @{ cmd = "housing-multi"; desc = "housing 100% all methods" },
    @{ cmd = "adult-multi"; desc = "adult 100% all methods" },
    @{ cmd = "zillow-multi"; desc = "zillow 15% all methods" },
    @{ cmd = "zillow-full-multi"; desc = "zillow 100% Influence+Lissa+Nystroem+Arnoldi" }
)

foreach ($j in $jobs) {
    Log "START $($j.desc)"
    & $py $runner $j.cmd 2>&1 | Tee-Object -FilePath $log -Append
    if ($LASTEXITCODE -ne 0) {
        Log "FAILED $($j.cmd) exit=$LASTEXITCODE"
    } else {
        Log "OK $($j.cmd)"
    }
}

$heavy = @("covertype", "electric", "imdb", "mnist", "cifar10")
foreach ($ds in $heavy) {
    Log "START heavy-multi $ds"
    & $py $runner heavy-multi --dataset $ds 2>&1 | Tee-Object -FilePath $log -Append
    if ($LASTEXITCODE -ne 0) { Log "FAILED heavy-multi $ds" } else { Log "OK heavy-multi $ds" }
}

Log "=== Queue finished ==="
