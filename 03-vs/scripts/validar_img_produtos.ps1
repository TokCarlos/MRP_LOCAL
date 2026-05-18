$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")

$FrontEnd = Join-Path $RepoRoot "01-mrp\front_end"
$ImgProdutosDir = Join-Path $FrontEnd "img\produtos"
$SeedPath = Join-Path $FrontEnd "data\produtos_seed.json"

if (!(Test-Path $ImgProdutosDir)) {
    Write-Host "ERRO: diretorio nao encontrado: $ImgProdutosDir" -ForegroundColor Red
    exit 1
}
if (!(Test-Path $SeedPath)) {
    Write-Host "ERRO: seed nao encontrado: $SeedPath" -ForegroundColor Red
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

$produtos = Read-JsonUtf8Safe -Path $SeedPath
$erros = New-Object System.Collections.Generic.List[string]

$ataCanonica = "SEHIS - GOV. RIO 114443801/2025"
$ataKeyCanonica = "sehis_gov_rio"

$allowedRootDirs = @("jpl", "aco", "tcr")
$blockedRootDirs = @("gov_rio", "sehis", "ata_gov_rio", "sehis_gov_rio")

$dirs = Get-ChildItem -Path $ImgProdutosDir -Directory | Select-Object -ExpandProperty Name
foreach ($d in $dirs) {
    if ($d -notin $allowedRootDirs) { $erros.Add("Pasta direta invalida em img/produtos: '$d'") }
}
foreach ($b in $blockedRootDirs) {
    if (Test-Path (Join-Path $ImgProdutosDir $b)) { $erros.Add("Pasta bloqueada encontrada em img/produtos: '$b'") }
}

$total = 0
$realAta = 0
$porEmpresa = @{}
$porOrigem = @{}
$idsOficiais = @{}
for ($i=128; $i -le 147; $i++) { $idsOficiais[$i] = $false }

$dupProdutoKey = $produtos | Group-Object produto_key | Where-Object { $_.Count -gt 1 }
foreach ($d in $dupProdutoKey) { $erros.Add("produto_key duplicada: '$($d.Name)' ($($d.Count)x)") }

$dupAtaItem = $produtos | Group-Object { "$($_.arp_key)|$($_.ata_numero)|$($_.item_ata)" } | Where-Object { $_.Count -gt 1 }
foreach ($d in $dupAtaItem) { $erros.Add("duplicidade ata_numero+item_ata: '$($d.Name)' ($($d.Count)x)") }

foreach ($p in $produtos) {
    $total++
    $id = [int](Get-PropText $p "id")
    $empresa = Get-PropText $p "empresa"
    $empresaKey = Get-PropText $p "empresa_key"
    $empresaNorm = Normalize-Text $empresa
    $origem = Get-PropText $p "origem_ata"
    $origemKey = Get-PropText $p "origem_ata_key"
    $ataOrigem = Get-PropText $p "ata_origem"
    $ataOrigemKey = Get-PropText $p "ata_origem_key"
    $arp = Get-PropText $p "arp"
    $arpKey = Get-PropText $p "arp_key"
    $itemAta = Get-PropText $p "item_ata"
    $preview = Get-PropText $p.imagem "preview"
    $imgStatus = Get-PropText $p.imagem "status"

    if ($empresaKey -notin @("jpl", "aco", "tcr")) { $erros.Add("Produto ID=$id com empresa_key invalida: '$empresaKey'") }
    if ($empresa -match "GOV|SEHIS" -or $empresaKey -match "gov|sehis") { $erros.Add("Produto ID=$id usando GOV/SEHIS como empresa") }
    if ($empresaKey -eq "tcr") { $erros.Add("Produto ID=$id usando TCR com dados operacionais nesta fase") }

    if ([string]::IsNullOrWhiteSpace($preview)) {
        $erros.Add("Produto ID=$id sem imagem.preview")
    } else {
        if ($preview -match "^assets/produtos") { $erros.Add("Produto ID=$id ainda referencia assets/produtos") }
        if ($preview -match "^img/produtos/(gov_rio|sehis)/") { $erros.Add("Produto ID=$id usa pasta proibida em img/produtos") }
        $previewAbs = Join-Path $FrontEnd ($preview -replace '/', '\\')
        if (!(Test-Path $previewAbs)) { $erros.Add("Produto ID=$id com imagem.preview sem arquivo fisico: '$preview'") }
    }

    if ($imgStatus -eq "REAL_ATA") { $realAta++ }

    if (-not $porEmpresa.ContainsKey($empresa)) { $porEmpresa[$empresa] = 0 }
    $porEmpresa[$empresa]++
    if (-not $porOrigem.ContainsKey($origem)) { $porOrigem[$origem] = 0 }
    $porOrigem[$origem]++

    if ($id -ge 128 -and $id -le 147) {
        $idsOficiais[$id] = $true
        if ($imgStatus -ne "REAL_ATA") { $erros.Add("ID $id com status '$imgStatus' (esperado REAL_ATA)") }
        if ($preview -notmatch "\.png$") { $erros.Add("ID $id deve apontar para PNG real") }
        if ($preview -match "\.svg$") { $erros.Add("ID $id ainda aponta para SVG demo") }
        if ($preview -notmatch "^img/produtos/(aco|jpl)/atas/sehis_gov_rio/") { $erros.Add("ID $id com caminho fora do padrao oficial") }
        if ($arp -ne $ataCanonica -or $origem -ne $ataCanonica -or $ataOrigem -ne $ataCanonica) { $erros.Add("ID $id com nome de ATA fora do canonico") }
        if ($arpKey -ne $ataKeyCanonica -or $origemKey -ne $ataKeyCanonica -or $ataOrigemKey -ne $ataKeyCanonica) { $erros.Add("ID $id com key de ATA fora do canonico") }
    }

    if ($id -ge 148 -and $id -le 167) {
        $erros.Add("ID duplicado legado ainda ativo no seed: $id")
    }
}

foreach ($id in 128..147) {
    if (-not $idsOficiais[$id]) { $erros.Add("Produto oficial ausente no seed: ID $id") }
}

$tcrDir = Join-Path $ImgProdutosDir "tcr"
if (Test-Path $tcrDir) {
    $tcrFiles = Get-ChildItem -Path $tcrDir -Recurse -File | Where-Object { $_.Name -ne ".keep" }
    if ($tcrFiles.Count -gt 0) { $erros.Add("TCR possui imagens reais, mas deve estar vazio nesta fase") }
}

Write-Host ""
Write-Host "VALIDACAO DE IMAGENS DE PRODUTOS" -ForegroundColor Cyan
Write-Host "Total de produtos: $total"
Write-Host "Total REAL_ATA: $realAta"
Write-Host ""
Write-Host "Total por empresa:"
foreach ($k in ($porEmpresa.Keys | Sort-Object)) { Write-Host " - $k : $($porEmpresa[$k])" }
Write-Host ""
Write-Host "Total por origem_ata:"
foreach ($k in ($porOrigem.Keys | Sort-Object)) { Write-Host " - $k : $($porOrigem[$k])" }

if ($erros.Count -gt 0) {
    Write-Host ""
    Write-Host "ERROS ENCONTRADOS:" -ForegroundColor Red
    foreach ($e in $erros) { Write-Host " - $e" -ForegroundColor Red }
    exit 1
}

Write-Host ""
Write-Host "OK: imagens oficiais validadas, IDs 128-147 com PNG real, sem duplicidade ativa 148-167." -ForegroundColor Green
exit 0
