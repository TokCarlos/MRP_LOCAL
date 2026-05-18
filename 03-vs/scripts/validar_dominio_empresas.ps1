$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
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

function Get-PropText {
    param([object]$Obj, [string]$Name)
    if ($null -eq $Obj) { return "" }
    if ($Obj.PSObject.Properties.Name -contains $Name) { return [string]$Obj.$Name }
    return ""
}

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) { return "" }
    $formD = $Value.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($c in $formD.ToCharArray()) {
        $cat = [Globalization.CharUnicodeInfo]::GetUnicodeCategory($c)
        if ($cat -ne [Globalization.UnicodeCategory]::NonSpacingMark) { [void]$sb.Append($c) }
    }
    return $sb.ToString().ToUpperInvariant().Trim()
}

$Produtos = Read-JsonUtf8Safe -Path $ProdutosPath

$EmpresaKeysValidas = @("jpl", "aco", "tcr")
$AtaCanonica = "SEHIS - GOV. RIO 114443801/2025"
$AtaCanonicaNorm = Normalize-Text $AtaCanonica
$AtaKeyCanonica = "sehis_gov_rio"

$Erros = New-Object System.Collections.Generic.List[string]
$PorEmpresa = @{}
$PorAta = @{}
$Total = 0
$ComImagemReal = 0

foreach ($p in $Produtos) {
    $Total++

    $id = Get-PropText $p "id"
    if ([string]::IsNullOrWhiteSpace($id)) { $id = "SEM_ID_$Total" }

    $empresa = Get-PropText $p "empresa"
    $empresaKey = Get-PropText $p "empresa_key"
    $empresaNorm = Normalize-Text $empresa

    if (-not $EmpresaKeysValidas.Contains($empresaKey)) {
        $Erros.Add("Produto ID=$id com empresa_key invalida: '$empresaKey'")
    }

    if ($empresaNorm -match "GOV|SEHIS" -or $empresaKey -match "gov|sehis") {
        $Erros.Add("Produto ID=$id trata GOV/SEHIS como empresa: empresa='$empresa' empresa_key='$empresaKey'")
    }

    if ($empresaNorm -eq "TCR" -or $empresaKey -eq "tcr") {
        $Erros.Add("Produto ID=$id esta usando TCR, mas TCR ainda nao possui dados operacionais nesta fase.")
    }

    if (-not $PorEmpresa.ContainsKey($empresa)) { $PorEmpresa[$empresa] = 0 }
    $PorEmpresa[$empresa]++

    $origemAta = Get-PropText $p "origem_ata"
    $origemAtaKey = Get-PropText $p "origem_ata_key"
    $ataOrigem = Get-PropText $p "ata_origem"
    $ataOrigemKey = Get-PropText $p "ata_origem_key"
    $arp = Get-PropText $p "arp"
    $arpKey = Get-PropText $p "arp_key"

    $isGovAta = ($origemAtaKey -eq $AtaKeyCanonica -or $ataOrigemKey -eq $AtaKeyCanonica -or $arpKey -eq $AtaKeyCanonica)

    if ($isGovAta) {
        if ((Normalize-Text $origemAta) -ne $AtaCanonicaNorm) { $Erros.Add("Produto ID=$id com origem_ata incorreta: '$origemAta'. Esperado '$AtaCanonica'.") }
        if ($origemAtaKey -ne $AtaKeyCanonica) { $Erros.Add("Produto ID=$id com origem_ata_key incorreta: '$origemAtaKey'.") }
        if ((Normalize-Text $ataOrigem) -ne $AtaCanonicaNorm) { $Erros.Add("Produto ID=$id com ata_origem incorreta: '$ataOrigem'. Esperado '$AtaCanonica'.") }
        if ($ataOrigemKey -ne $AtaKeyCanonica) { $Erros.Add("Produto ID=$id com ata_origem_key incorreta: '$ataOrigemKey'.") }
        if ((Normalize-Text $arp) -ne $AtaCanonicaNorm) { $Erros.Add("Produto ID=$id com arp incorreto: '$arp'. Esperado '$AtaCanonica'.") }
        if ($arpKey -ne $AtaKeyCanonica) { $Erros.Add("Produto ID=$id com arp_key incorreto: '$arpKey'.") }
    }

    $ataResumo = if ($arp) { $arp } elseif ($origemAta) { $origemAta } else { "_SEM_ATA_" }
    if (-not $PorAta.ContainsKey($ataResumo)) { $PorAta[$ataResumo] = 0 }
    $PorAta[$ataResumo]++

    if ($p.PSObject.Properties.Name -contains "imagem") {
        $imgStatus = Get-PropText $p.imagem "status"
        if ($imgStatus -eq "REAL_ATA") { $ComImagemReal++ }
    }
}

Write-Host ""
Write-Host "VALIDACAO DE DOMINIO - EMPRESA / ATA / ORIGEM" -ForegroundColor Cyan
Write-Host "Arquivo: $ProdutosPath"
Write-Host "Total de produtos: $Total"
Write-Host "Produtos com imagem real: $ComImagemReal"
Write-Host ""
Write-Host "Produtos por empresa:"
foreach ($k in ($PorEmpresa.Keys | Sort-Object)) { Write-Host " - $k : $($PorEmpresa[$k])" }
Write-Host ""
Write-Host "Produtos por ATA/origem:"
foreach ($k in ($PorAta.Keys | Sort-Object)) { Write-Host " - $k : $($PorAta[$k])" }

if ($Erros.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROS ENCONTRADOS:" -ForegroundColor Red
    foreach ($e in $Erros) { Write-Host " - $e" -ForegroundColor Red }
    exit 1
}

Write-Host ""
Write-Host "OK: dominio valido. GOV/SEHIS nao esta como empresa. ATA normalizada como '$AtaCanonica'." -ForegroundColor Green
exit 0
