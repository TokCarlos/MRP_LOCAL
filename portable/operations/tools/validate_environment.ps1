$ErrorActionPreference = "Stop"

$portableRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$requiredDirs = @(
    "app\frontend",
    "infrastructure\config",
    "operations\health",
    "operations\scripts",
    "operations\tools",
    "assets",
    "data",
    "runtime",
    "logs",
    "tmp"
)

$failed = $false
foreach ($dir in $requiredDirs) {
    $path = Join-Path $portableRoot $dir
    if (Test-Path -LiteralPath $path -PathType Container) {
        Write-Host "[OK] DIR $dir"
    } else {
        Write-Host "[ERRO] DIR ausente: $dir"
        $failed = $true
    }
}

$frontendIndex = Join-Path $portableRoot "app\frontend\index.html"
if (Test-Path -LiteralPath $frontendIndex -PathType Leaf) {
    Write-Host "[OK] Frontend detectado"
} else {
    Write-Host "[ERRO] Frontend sem index.html"
    $failed = $true
}

if ($failed) { exit 1 }
exit 0
