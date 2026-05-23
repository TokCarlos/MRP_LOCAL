$ErrorActionPreference = "Stop"

function Add-Issue {
    param(
        [System.Collections.Generic.List[object]]$Issues,
        [string]$Id,
        [string]$Level,
        [string]$Title,
        [bool]$BlocksExecution,
        [string]$Message
    )
    $Issues.Add([pscustomobject]@{
        id = $Id
        level = $Level
        title = $Title
        blocks_execution = $BlocksExecution
        message = $Message
    }) | Out-Null
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$mrpRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir ".."))
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $mrpRoot ".."))

$issues = New-Object 'System.Collections.Generic.List[object]'

$requiredDirs = @(
    "config","runtime","tools","data","db","logs","tmp","backups",
    "front_end","back_end","engine","adapters","install","health","docs_runtime"
)

foreach ($dir in $requiredDirs) {
    $full = Join-Path $mrpRoot $dir
    if (!(Test-Path -LiteralPath $full -PathType Container)) {
        Add-Issue -Issues $issues -Id ("dir_missing_" + $dir) -Level "CRITICO" -Title ("Diretorio ausente: " + $dir) -BlocksExecution $true -Message ("Diretorio obrigatorio nao encontrado em " + $full)
    }
}

$configFile = Join-Path $mrpRoot "config\mrp_local.env.json"
if (!(Test-Path -LiteralPath $configFile -PathType Leaf)) {
    Add-Issue -Issues $issues -Id "config_missing" -Level "CRITICO" -Title "Configuracao principal ausente" -BlocksExecution $true -Message "Arquivo config/mrp_local.env.json nao encontrado."
}

$indexFile = Join-Path $mrpRoot "front_end\index.html"
if (!(Test-Path -LiteralPath $indexFile -PathType Leaf)) {
    Add-Issue -Issues $issues -Id "frontend_index_missing" -Level "CRITICO" -Title "Frontend ausente" -BlocksExecution $true -Message "Arquivo front_end/index.html nao encontrado."
}

$portInUse = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
if ($portInUse) {
    Add-Issue -Issues $issues -Id "port_8765_in_use" -Level "OPCIONAL" -Title "Porta 8765 em uso" -BlocksExecution $false -Message "A porta principal ja esta ocupada. Validar se o processo e o frontend esperado."
}

$writableTargets = @("logs","tmp","backups")
foreach ($target in $writableTargets) {
    $targetPath = Join-Path $mrpRoot $target
    if (Test-Path -LiteralPath $targetPath -PathType Container) {
        $probe = Join-Path $targetPath ".precheck_write_test.tmp"
        try {
            Set-Content -Path $probe -Value "ok" -Encoding UTF8
            Remove-Item -LiteralPath $probe -Force -ErrorAction SilentlyContinue
        } catch {
            Add-Issue -Issues $issues -Id ("write_denied_" + $target) -Level "CRITICO" -Title ("Sem permissao de escrita em " + $target) -BlocksExecution $true -Message ("Nao foi possivel escrever em " + $targetPath)
        }
    }
}

$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Add-Issue -Issues $issues -Id "python_not_detected" -Level "RECOMENDADO" -Title "Python nao detectado" -BlocksExecution $false -Message "Backend FastAPI ja existe para Produtos; Python e recomendado para operacao completa do backend DEV."
}

$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Add-Issue -Issues $issues -Id "node_not_detected" -Level "RECOMENDADO" -Title "Node nao detectado" -BlocksExecution $false -Message "Node e util para scripts auxiliares, mas nao e critico para operacao atual do frontend."
}

$criticalCount = @($issues | Where-Object { $_.level -eq "CRITICO" }).Count
$optionalCount = @($issues | Where-Object { $_.level -eq "OPCIONAL" }).Count
$recommendedCount = @($issues | Where-Object { $_.level -eq "RECOMENDADO" }).Count

Write-Host "PRECHECK_INSTALACAO_PASSIVO"
Write-Host "MRP_ROOT=$mrpRoot"
Write-Host "REPO_ROOT=$repoRoot"
Write-Host ("PENDENCIAS: CRITICO={0} OPCIONAL={1} RECOMENDADO={2}" -f $criticalCount, $optionalCount, $recommendedCount)

if ($issues.Count -gt 0) {
    $issues | ForEach-Object {
        Write-Host ("[{0}] {1} - {2}" -f $_.level, $_.id, $_.message)
    }
}

if ($criticalCount -gt 0) {
    Write-Host "PRECHECK=FALHA_CRITICA"
    exit 1
}

Write-Host "PRECHECK=OK_SEM_BLOQUEIO_CRITICO"
exit 0
