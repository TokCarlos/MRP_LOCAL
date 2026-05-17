$ErrorActionPreference = "Stop"

$RepoRoot = "X:\"
$ProdutosPath = Join-Path $RepoRoot "01-mrp\front_end\data\produtos_seed.json"

if (!(Test-Path $ProdutosPath)) {
    Write-Host "ERRO: produtos_seed.json nao encontrado em: $ProdutosPath" -ForegroundColor Red
    exit 1
}

function Read-JsonUtf8Safe {
    param([string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes($Path)

    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        $text = [System.Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
    } else {
        $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    }

    return $text | ConvertFrom-Json
}

$Produtos = Read-JsonUtf8Safe -Path $ProdutosPath

$EmpresaKeysValidas = @("jpl", "aco", "tcr")

$Erros = New-Object System.Collections.Generic.List[string]

$Total = 0
$PorEmpresa = @{}
$PorOrigem = @{}
$GovRioOrigemCount = 0

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return "" }
    $formD = $Value.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($c in $formD.ToCharArray()) {
        $cat = [Globalization.CharUnicodeInfo]::GetUnicodeCategory($c)
        if ($cat -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($c)
        }
    }
    return $sb.ToString().ToUpperInvariant().Trim()
}

foreach ($p in $Produtos) {
    $Total++

    $empresa = [string]$p.empresa
    $empresaKey = [string]$p.empresa_key

    if (-not $EmpresaKeysValidas.Contains($empresaKey)) {
        $Erros.Add("Produto ID=$($p.id) com empresa_key invalida: '$empresaKey'")
    }

    # Se a chave estiver valida, o nome pode variar por encoding em arquivo legado.
    if ($empresaKey -eq "jpl" -and (Normalize-Text $empresa) -notmatch "^JPL$") {
        $Erros.Add("Produto ID=$($p.id) com divergencia empresa/empresa_key: empresa='$empresa' empresa_key='$empresaKey'")
    }
    if ($empresaKey -eq "tcr" -and (Normalize-Text $empresa) -notmatch "^TCR$") {
        $Erros.Add("Produto ID=$($p.id) com divergencia empresa/empresa_key: empresa='$empresa' empresa_key='$empresaKey'")
    }

    if ($empresa -match "GOV" -or $empresaKey -eq "gov_rio") {
        $Erros.Add("Produto ID=$($p.id) trata GOV como empresa: empresa='$empresa' empresa_key='$empresaKey'")
    }

    if ($empresa -eq "TCR" -or $empresaKey -eq "tcr") {
        $Erros.Add("Produto ID=$($p.id) usa TCR, mas TCR ainda nao possui dados operacionais nesta fase.")
    }

    if (-not $PorEmpresa.ContainsKey($empresa)) {
        $PorEmpresa[$empresa] = 0
    }
    $PorEmpresa[$empresa]++

    $origem = $null
    if ($p.PSObject.Properties.Name -contains "origem_ata") {
        $origem = [string]$p.origem_ata
    } elseif ($p.PSObject.Properties.Name -contains "ata_origem") {
        $origem = [string]$p.ata_origem
    } elseif ($p.PSObject.Properties.Name -contains "cliente") {
        $origem = [string]$p.cliente
    } elseif ($p.PSObject.Properties.Name -contains "arp") {
        $origem = [string]$p.arp
    } else {
        $origem = "_SEM_ORIGEM_"
    }

    if (([string]$origem) -match "GOV") {
        $GovRioOrigemCount++
    }

    if (-not $PorOrigem.ContainsKey($origem)) {
        $PorOrigem[$origem] = 0
    }
    $PorOrigem[$origem]++
}

Write-Host ""
Write-Host "VALIDACAO DE DOMINIO - EMPRESAS" -ForegroundColor Cyan
Write-Host "Total de produtos: $Total"
Write-Host "Produtos GOV. RIO como ATA/origem/cliente: $GovRioOrigemCount"
Write-Host ""
Write-Host "Produtos por empresa:"
foreach ($k in ($PorEmpresa.Keys | Sort-Object)) {
    Write-Host " - $k : $($PorEmpresa[$k])"
}

Write-Host ""
Write-Host "Produtos por origem/ATA/cliente:"
foreach ($k in ($PorOrigem.Keys | Sort-Object)) {
    Write-Host " - $k : $($PorOrigem[$k])"
}

if ($Erros.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROS ENCONTRADOS:" -ForegroundColor Red
    foreach ($e in $Erros) {
        Write-Host " - $e" -ForegroundColor Red
    }
    exit 1
}

Write-Host ""
Write-Host "OK: dominio de empresas valido. GOV. RIO nao esta sendo tratado como empresa. TCR esta reservado sem dados operacionais." -ForegroundColor Green
exit 0
