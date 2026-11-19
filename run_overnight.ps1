<#
Overnight run: main study -> sensitivity sweep -> plots. Resumable: just start it again after an
interruption, finished (study, dataset, method, seed) runs are skipped.

  powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1
  powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1 -NJobs 6 -Threads 2 -SkipSweep

Optional environment variables (webhook after every finished block, at the end and on a crash;
if DIPLOMA_WEBHOOK_URL is not set nothing is sent; a failing webhook never stops the run, timeout 10 s):
  $env:DIPLOMA_WEBHOOK_URL    = "https://..."     # POST target (JSON body)
  $env:DIPLOMA_WEBHOOK_KEY    = "<secret>"        # sent as a header
  $env:DIPLOMA_WEBHOOK_HEADER = "Authorization"   # header name; default "Authorization: Bearer <key>",
                                                  # any other name gets the raw key as its value
Other knobs: -NJobs (parallel pyDVL refits), -Threads (torch/BLAS threads per process), -Device cpu|cuda.
Logs: run_logs\overnight-<timestamp>.log (+ results\_logs\*.log written by run_study.py).
#>
param(
    [int]$NJobs = 8,
    [int]$Threads = 2,
    [string]$Device = "cpu",
    [switch]$SkipMain,
    [switch]$SkipSweep
)
$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot
$py = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "python" }
New-Item -ItemType Directory -Force -Path "run_logs" | Out-Null
$log = Join-Path "run_logs" ("overnight-{0:yyyyMMdd-HHmmss}.log" -f (Get-Date))
$env:TQDM_DISABLE = "1"
$env:PYTHONIOENCODING = "utf-8"

# keep the laptop awake while this script runs (reverts automatically when the process exits)
Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
[void][Win32.Power]::SetThreadExecutionState([uint32]"0x80000001")   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED

function Step([string]$name, [string[]]$cmdArgs) {
    $t0 = Get-Date
    "[$($t0.ToString('HH:mm:ss'))] === $name : $py $($cmdArgs -join ' ')" | Tee-Object -FilePath $log -Append
    & $py @cmdArgs 2>&1 | Tee-Object -FilePath $log -Append
    $code = $LASTEXITCODE
    "[$((Get-Date).ToString('HH:mm:ss'))] === $name finished, exit=$code, {0:N1} min" -f ((Get-Date) - $t0).TotalMinutes |
        Tee-Object -FilePath $log -Append
}

$common = @("--n-jobs", "$NJobs", "--threads", "$Threads", "--device", $Device)
if (-not $SkipMain)  { Step "main study" (@("run_study.py", "main") + $common) }
if (-not $SkipSweep) { Step "sensitivity sweep" (@("run_study.py", "sweep") + $common) }
Step "plots" @("plot_results.py", "--root", "results", "--out", "assets")
Step "paired stats" @("paired_stats.py", "--root", "results", "--out", "assets")
Step "status" @("run_study.py", "status")
[void][Win32.Power]::SetThreadExecutionState([uint32]"0x80000000")
"done. log: $log" | Tee-Object -FilePath $log -Append
