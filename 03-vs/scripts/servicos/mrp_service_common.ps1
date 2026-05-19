$ErrorActionPreference = "Stop"
$script:MrpServiceCommonDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }

function Resolve-MrpNativePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop

    if ($resolved.ProviderPath) {
        return $resolved.ProviderPath
    }

    $text = [string]$resolved.Path
    $prefix = "Microsoft.PowerShell.Core\FileSystem::"

    if ($text.StartsWith($prefix)) {
        return $text.Substring($prefix.Length)
    }

    return $text
}

function Normalize-MrpPathForDotNet {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $normalizedPath = [string]$Path
    $prefix = "Microsoft.PowerShell.Core\FileSystem::"

    if ($normalizedPath.StartsWith($prefix)) {
        $normalizedPath = $normalizedPath.Substring($prefix.Length)
    }

    return $normalizedPath
}

function Get-MrpRepoRoot {
    if ($env:MRP_LOCAL_ROOT -and (Test-Path -LiteralPath $env:MRP_LOCAL_ROOT)) {
        return (Resolve-MrpNativePath -Path $env:MRP_LOCAL_ROOT)
    }

    $serviceDir = $script:MrpServiceCommonDir
    $candidate = Join-Path $serviceDir "..\..\.."

    if (Test-Path -LiteralPath $candidate) {
        return (Resolve-MrpNativePath -Path $candidate)
    }

    throw "Nao foi possivel resolver a raiz do MRP_LOCAL. Defina MRP_LOCAL_ROOT ou execute o script dentro do projeto."
}

function Read-MrpConfig {
    $root = Get-MrpRepoRoot
    $configPath = Join-Path $root "01-mrp\config\mrp_local.env.json"

    if (-not (Test-Path -LiteralPath $configPath)) {
        throw "Config nao encontrada: $configPath"
    }

    $json = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json

    return [pscustomobject]@{
        Root = $root
        Path = $configPath
        Data = $json
    }
}

function Join-MrpPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Root,

        [Parameter(Mandatory = $true)]
        [string]$RelativePath
    )

    return (Join-Path $Root ($RelativePath -replace "/", "\"))
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Text,

        [switch]$Append
    )

    $filePath = Normalize-MrpPathForDotNet -Path $Path
    $dir = Split-Path -Parent $filePath

    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)

    if ($Append -and (Test-Path -LiteralPath $filePath)) {
        [System.IO.File]::AppendAllText($filePath, $Text, $encoding)
    } else {
        [System.IO.File]::WriteAllText($filePath, $Text, $encoding)
    }
}

function Add-MrpLogLine {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LogFile,

        [Parameter(Mandatory = $true)]
        [string]$Origem,

        [Parameter(Mandatory = $true)]
        [string]$Status,

        [string]$Detalhe = ""
    )

    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Origem=$Origem | Status=$Status | Detalhe=$Detalhe`n"
    Write-Utf8NoBomFile -Path $LogFile -Text $line -Append
}

function Get-MrpServiceContext {
    $cfg = Read-MrpConfig
    $root = $cfg.Root
    $data = $cfg.Data

    $frontendDir = Join-MrpPath -Root $root -RelativePath $data.frontend.relative_dir
    $indexFile = Join-Path $frontendDir $data.frontend.index_file
    $logsDir = Join-MrpPath -Root $root -RelativePath $data.logs.relative_dir
    $scriptsDir = Join-Path $root "03-vs\scripts\servicos"

    New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

    return [pscustomobject]@{
        Root = $root
        Config = $data
        ConfigPath = $cfg.Path
        FrontendDir = $frontendDir
        IndexFile = $indexFile
        LogsDir = $logsDir
        ScriptsDir = $scriptsDir
        Port = [int]$data.frontend.port
        Bind = [string]$data.frontend.bind
        HealthUrl = "http://127.0.0.1:$([int]$data.frontend.port)$([string]$data.frontend.health_path)"
        TaskName = [string]$data.windows_task.name
        StartupWaitSeconds = [int]$data.frontend.startup_wait_seconds
    }
}

function Get-MrpPortListenerPids {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Port
    )

    $listenerProcessIds = New-Object 'System.Collections.Generic.List[int]'

    try {
        $connections = @(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction Stop)

        foreach ($connection in $connections) {
            if ($connection.OwningProcess -and -not $listenerProcessIds.Contains([int]$connection.OwningProcess)) {
                $listenerProcessIds.Add([int]$connection.OwningProcess)
            }
        }
    } catch {
        $lines = @(netstat -ano | Select-String ":$Port" | Select-String "LISTENING")

        foreach ($line in $lines) {
            $parts = (($line.ToString()).Trim() -split "\s+")

            if ($parts.Count -ge 5) {
                $parsedProcessId = 0

                if ([int]::TryParse($parts[-1], [ref]$parsedProcessId) -and -not $listenerProcessIds.Contains($parsedProcessId)) {
                    $listenerProcessIds.Add($parsedProcessId)
                }
            }
        }
    }

    return @($listenerProcessIds.ToArray())
}

function Test-PortListening {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Port
    )

    return ((Get-MrpPortListenerPids -Port $Port).Count -gt 0)
}

function Get-MrpProcessInfo {
    param(
        [Parameter(Mandatory = $true)]
        [int]$ProcessId
    )

    try {
        return Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction Stop
    } catch {
        return $null
    }
}

function Test-MrpHttpOk {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Url,

        [int]$TimeoutSec = 2
    )

    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec $TimeoutSec
        return ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400)
    } catch {
        return $false
    }
}

function Resolve-MrpPython {
    param(
        [Parameter(Mandatory = $true)]
        $Context
    )

    $candidates = @()

    if ($Context.Config.python.preferred_relative_exe) {
        $candidates += (Join-MrpPath -Root $Context.Root -RelativePath ([string]$Context.Config.python.preferred_relative_exe))
    }

    if ($env:MRP_PYTHON_EXE) {
        $candidates += $env:MRP_PYTHON_EXE
    }

    if ($Context.Config.python.allow_py_launcher) {
        $candidates += "py.exe"
    }

    if ($Context.Config.python.allow_python_path) {
        $candidates += "python.exe"
    }

    foreach ($command in $candidates) {
        if (-not $command) {
            continue
        }

        if ($command -match "[\\/]") {
            if (Test-Path -LiteralPath $command) {
                return (Normalize-MrpPathForDotNet -Path $command)
            }
        } else {
            $found = Get-Command $command -ErrorAction SilentlyContinue

            if ($found) {
                return $found.Source
            }
        }
    }

    throw "Python nao encontrado. Configure MRP_PYTHON_EXE, instale Python ou forneca runtime portable em 01-mrp/runtime/python/python.exe."
}

function Stop-MrpHttpServerOnPort {
    param(
        [Parameter(Mandatory = $true)]
        [int]$Port,

        [string]$LogFile = "",

        [switch]$ForceAll
    )

    $currentProcessId = [System.Diagnostics.Process]::GetCurrentProcess().Id
    $killed = 0

    foreach ($listenerProcessId in (Get-MrpPortListenerPids -Port $Port)) {
        if ($listenerProcessId -eq 0 -or $listenerProcessId -eq $currentProcessId) {
            continue
        }

        $proc = Get-MrpProcessInfo -ProcessId $listenerProcessId
        $cmd = if ($proc) { [string]$proc.CommandLine } else { "" }
        $name = if ($proc) { [string]$proc.Name } else { "" }

        $isMrpHttp = $false

        if ($ForceAll) {
            $isMrpHttp = $true
        } elseif ($cmd -like "*http.server*" -or $cmd -like "*mrp_frontend_start*" -or $cmd -like "*MRP_LOCAL*") {
            $isMrpHttp = $true
        }

        if ($isMrpHttp) {
            try {
                Stop-Process -Id $listenerProcessId -Force -ErrorAction Stop
                $killed++

                if ($LogFile) {
                    Add-MrpLogLine -LogFile $LogFile -Origem "stop_port" -Status "PROCESSO_ENCERRADO" -Detalhe "PID=$listenerProcessId Name=$name"
                }
            } catch {
                if ($LogFile) {
                    Add-MrpLogLine -LogFile $LogFile -Origem "stop_port" -Status "FALHA_ENCERRAR_PROCESSO" -Detalhe "PID=$listenerProcessId Erro=$($_.Exception.Message)"
                }
            }
        }
    }

    return $killed
}

function Stop-MrpRelatedWatchdogs {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ProjectRoot,

        [string]$LogFile = ""
    )

    $currentProcessId = [System.Diagnostics.Process]::GetCurrentProcess().Id
    $rootEscaped = [Regex]::Escape($ProjectRoot)
    $killed = 0

    try {
        $watchdogProcesses = Get-CimInstance Win32_Process | Where-Object {
            $_.ProcessId -ne $currentProcessId -and
            $_.Name -match "^(powershell|pwsh)(\.exe)?$" -and
            $_.CommandLine -like "*mrp_frontend_watchdog.ps1*" -and
            $_.CommandLine -match $rootEscaped
        }

        foreach ($processInfo in $watchdogProcesses) {
            try {
                Stop-Process -Id $processInfo.ProcessId -Force -ErrorAction Stop
                $killed++

                if ($LogFile) {
                    Add-MrpLogLine -LogFile $LogFile -Origem "stop_watchdog" -Status "WATCHDOG_ENCERRADO" -Detalhe "PID=$($processInfo.ProcessId)"
                }
            } catch {
                if ($LogFile) {
                    Add-MrpLogLine -LogFile $LogFile -Origem "stop_watchdog" -Status "FALHA_ENCERRAR_WATCHDOG" -Detalhe "PID=$($processInfo.ProcessId) Erro=$($_.Exception.Message)"
                }
            }
        }
    } catch {
        if ($LogFile) {
            Add-MrpLogLine -LogFile $LogFile -Origem "stop_watchdog" -Status "FALHA_CONSULTA" -Detalhe $_.Exception.Message
        }
    }

    return $killed
}
