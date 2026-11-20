<#
Overnight run: main study -> sensitivity sweep -> secondary studies (models, distillation, convex,
systematic noise, transfer) -> plots. Resumable: just start it again after an interruption,
finished (study, dataset, method, seed) runs are skipped.

  powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1
  powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1 -Workers 6 -ThreadsPerWorker 2
  powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1 -Workers 1 -NJobs 6 -Threads 2 -SkipSweep
  powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1 -SkipMain -Sections models,transfer

Skip flags: -SkipMain, -SkipExt (all secondary studies), -SkipSweep, -SkipPlots;
-Sections <list> runs only these secondary sections (models, distill, convex, noise, transfer).
Transfer reads the values of the main study (noise10) and of models / distill, so run it after them.

Optional environment variables (webhook after every finished block, at the end and on a crash;
if DIPLOMA_WEBHOOK_URL is not set nothing is sent; a failing webhook never stops the run, timeout 10 s):
  $env:DIPLOMA_WEBHOOK_URL    = "https://..."     # POST target (JSON body)
  $env:DIPLOMA_WEBHOOK_KEY    = "<secret>"        # sent as a header
  $env:DIPLOMA_WEBHOOK_HEADER = "Authorization"   # header name; default "Authorization: Bearer <key>",
                                                  # any other name gets the raw key as its value
Parallel mode [AUDIT-FIX P12]: -Workers N worker processes x -ThreadsPerWorker M threads (pyDVL n_jobs = torch/BLAS
threads = M per worker). Default 6 x 2 for an i7-12700H (14 cores / 20 threads, 16 GB); -Workers 1 = the old
sequential run with -NJobs / -Threads. [P13] Memory-aware: a unit starts only if its expected peak (+ the
expected growth of the running units + -MinFreeMB) fits into the free RAM; heavy units (DirectInfluence with the
explicit Hessian, ~7.6 GB on covertype) run in their own process, at most -MaxHeavy (default 1) at a time.
Worker logs: results\_logs\worker-<pid>.log (lines also prefixed [w<pid>] in the main log).
Other knobs: -NJobs (parallel pyDVL refits), -Threads (torch/BLAS threads per process), -Device cpu|cuda.
Logs: run_logs\overnight-<timestamp>.log (+ results\_logs\*.log written by run_study.py).
#>
param(
    [int]$Workers = 6,
    [int]$ThreadsPerWorker = 2,
    [int]$MinFreeMB = 1500,
    [int]$MaxHeavy = 1,
    [int]$NJobs = 8,
    [int]$Threads = 2,
    [string]$Device = "cpu",
    [switch]$SkipMain,
    [switch]$SkipExt,
    [switch]$SkipSweep,
    [switch]$SkipPlots,
    [string[]]$Sections = @()
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

if ($Workers -gt 1) {
    $common = @("--workers", "$Workers", "--n-jobs", "$ThreadsPerWorker", "--threads", "$ThreadsPerWorker",
                "--min-free-mb", "$MinFreeMB", "--max-heavy", "$MaxHeavy", "--device", $Device)
} else {
    $common = @("--n-jobs", "$NJobs", "--threads", "$Threads", "--device", $Device)
}
if (-not $SkipMain)  { Step "main study" (@("run_study.py", "main") + $common) }
if (-not $SkipSweep) { Step "sensitivity sweep" (@("run_study.py", "sweep") + $common) }
if (-not $SkipExt) {
    $extArgs = @("run_study.py", "ext") + $common
    $secs = @($Sections | ForEach-Object { $_ -split "," } | Where-Object { $_ })
    if ($secs.Count -gt 0) { $extArgs += @("--sections") + $secs }
    Step "secondary studies" $extArgs
}
if (-not $SkipPlots) {
    Step "plots" @("plot_results.py", "--root", "results", "--out", "assets")
    Step "paired stats" @("paired_stats.py", "--root", "results", "--out", "assets")
}
Step "status" @("run_study.py", "status")
[void][Win32.Power]::SetThreadExecutionState([uint32]"0x80000000")
"done. log: $log" | Tee-Object -FilePath $log -Append
