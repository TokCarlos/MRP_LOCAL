$ErrorActionPreference = "Stop"

$portableRoot = $PSScriptRoot
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

$requiredFiles = @(
    "start_mrp.bat",
    "stop_mrp.bat",
    "status_mrp.bat",
    "healthcheck_mrp.bat",
    "README_PORTABLE.txt",
    "MANIFEST_PORTABLE.txt"
)

$failed = $false
foreach ($dir in $requiredDirs) {
    $target = Join-Path $portableRoot $dir
    if (Test-Path -LiteralPath $target -PathType Container) {
        Write-Host "[OK] DIR $dir"
    } else {
        Write-Host "[ERRO] DIR ausente: $dir"
        $failed = $true
    }
}

foreach ($file in $requiredFiles) {
    $target = Join-Path $portableRoot $file
    if (Test-Path -LiteralPath $target -PathType Leaf) {
        Write-Host "[OK] FILE $file"
    } else {
        Write-Host "[ERRO] FILE ausente: $file"
        $failed = $true
    }
}

$frontIndex = Join-Path $portableRoot "app\frontend\index.html"
if (Test-Path -LiteralPath $frontIndex -PathType Leaf) {
    Write-Host "[OK] Frontend funcional detectado"
} else {
    Write-Host "[ERRO] Frontend sem index.html"
    $failed = $true
}

if ($failed) { exit 1 }
exit 0
