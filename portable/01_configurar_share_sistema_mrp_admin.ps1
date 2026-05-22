$ErrorActionPreference = "Stop"

$OfficialRoot = "C:\Users\carlo\Desktop\PCP SERVIDOR\SISTEMA_MRP"
$ForbiddenTargets = @(
    "C:\system_jpl",
    "C:\MRP_REDE_FAKE",
    "C:\SISTEMA_MRP",
    "C:\Users\carlo\Desktop\PCP SERVIDOR\PCP"
)
$ShareName = "system_jpl"

function Normalize-PathText {
    param([Parameter(Mandatory = $true)][string]$Path)
    return ([System.IO.Path]::GetFullPath($Path).TrimEnd("\"))
}

function Test-Admin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

function Test-DirectCRoot {
    param([Parameter(Mandatory = $true)][string]$Path)
    return ((Normalize-PathText -Path $Path) -match '^[cC]:\\[^\\]+$')
}

if (-not (Test-Admin)) {
    Write-Host "[ERRO] Execute este script como Administrador."
    exit 1
}

if (-not (Test-Path -LiteralPath $OfficialRoot -PathType Container)) {
    Write-Host "[ERRO] Raiz oficial nao encontrada: $OfficialRoot"
    exit 1
}

$officialNorm = Normalize-PathText -Path $OfficialRoot
$forbiddenNorm = @($ForbiddenTargets | ForEach-Object { Normalize-PathText -Path $_ })

if ($forbiddenNorm -contains $officialNorm) {
    Write-Host "[ERRO] Destino oficial e proibido: $OfficialRoot"
    exit 1
}

if (Test-DirectCRoot -Path $OfficialRoot) {
    Write-Host "[ERRO] Raiz direta em C:\ e proibida: $OfficialRoot"
    exit 1
}

try {
    $existing = Get-SmbShare -Name $ShareName -ErrorAction SilentlyContinue
    if ($existing) {
        $existingPath = Normalize-PathText -Path ([string]$existing.Path)
        if ($existingPath -ne $officialNorm) {
            if ($forbiddenNorm -contains $existingPath -or (Test-DirectCRoot -Path $existingPath)) {
                Write-Host "[INFO] Share existente aponta para destino bloqueado e sera corrigido: $($existing.Path)"
            } else {
                Write-Host "[INFO] Share existente aponta para outro destino e sera corrigido: $($existing.Path)"
            }
            Remove-SmbShare -Name $ShareName -Force
            New-SmbShare -Name $ShareName -Path $OfficialRoot -FullAccess "Everyone" | Out-Null
        } else {
            Write-Host "[OK] Share ja aponta para a raiz oficial."
        }
    } else {
        New-SmbShare -Name $ShareName -Path $OfficialRoot -FullAccess "Everyone" | Out-Null
        Write-Host "[OK] Share criado: \\$env:COMPUTERNAME\$ShareName -> $OfficialRoot"
    }

    Write-Host "[OK] Share system_jpl configurado para: $OfficialRoot"
    exit 0
} catch {
    Write-Host "[ERRO] Falha ao configurar share: $($_.Exception.Message)"
    exit 1
}
