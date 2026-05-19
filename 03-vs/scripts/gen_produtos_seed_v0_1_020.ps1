param(
    [string]$PromptPath = "",
    [switch]$LegadoConfirmado
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $ScriptDir "..\.."))
if ($env:MRP_LOCAL_ROOT) {
    $RepoRoot = [System.IO.Path]::GetFullPath($env:MRP_LOCAL_ROOT)
}

if (-not $LegadoConfirmado) {
    throw "Script legado. Use -LegadoConfirmado apenas para reproducao historica controlada."
}

if ([string]::IsNullOrWhiteSpace($PromptPath)) {
    throw "Informe -PromptPath para execucao legada controlada."
}

function Normalize-Key([string]$value) {
    $v = $value.Trim()
    $map = @{
        "AÇO" = "aco"
        "JPL" = "jpl"
        "CIMASP" = "cimasp"
        "CIM-JEQUI" = "cim_jequi"
        "SOMAR-MARICÁ" = "somar_marica"
        "SEHIS - GOV. RJ" = "gov_rio"
    }
    if ($map.ContainsKey($v)) { return $map[$v] }

    $v = $v.ToLowerInvariant()
    $norm = $v.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $norm.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($ch) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($ch)
        }
    }
    $out = $sb.ToString().Normalize([Text.NormalizationForm]::FormC)
    $out = $out -replace "[^a-z0-9]+", "_"
    return $out.Trim("_")
}

function Normalize-Ata([string]$ata) {
    return ($ata.Trim() -replace "\s+", "" -replace "/", "_")
}

function Normalize-ItemKey([string]$itemAta) {
    $v = $itemAta.Trim()
    if ($v -match "^\d+$") {
        return "item_{0}" -f ([int]$v).ToString("000")
    }
    return "item_" + (($v -replace "\.", "_") -replace "[^0-9_]", "")
}

function Infer-Categoria([string]$nome) {
    $u = $nome.ToUpperInvariant()
    $ati = @("SIMULADOR","ALONGAMENTO","EQUILÍBRIO","EQUILIBRIO","CALISTÊNICA","CALISTENICA","EXERCICIOS","GINASTICA","PRANCHA ABDOMINAL","ESQUI","CAMINHADA","FORTALECIMENTO","THAI CHI","ABDOMINAL")
    foreach ($k in $ati) { if ($u.Contains($k)) { return "ATI" } }

    $play = @("BALANÇO","BALANCO","ARTEFATO RECREATIVO","MULTI KIDS","MULTIKIDS","PLAYGROUND","GAIOLA","LABIRINTO","TEA","ACESSÍVEL","ACESSIVEL","INCLUSIVO","KIDS")
    foreach ($k in $play) { if ($u.Contains($k)) { return "PLAYGROUND" } }

    $mob = @("ASSENTO","BANCO","PAPELEIRA","COLETOR","GUARDA CORPO","PARACICLO","PARACICLOS","TABLADO","MESA","FUTMESA","REFÚGIO","REFUGIO","ESTRUTURA","PLACA","PISO","BICICLETÁRIO","BICICLETARIO","ABRIGO","GRADIL","TOTEM")
    foreach ($k in $mob) { if ($u.Contains($k)) { return "MOBILIARIO" } }

    return "PENDENTE_CLASSIFICACAO"
}

function Escape-Xml([string]$value) {
    return [Security.SecurityElement]::Escape($value)
}

$text = Get-Content -Path $PromptPath -Raw -Encoding UTF8
$regex = [regex]'(?s)```tsv\s*(.*?)\s*```'
$match = $regex.Match($text)
if (-not $match.Success) { throw "Bloco TSV nao encontrado no prompt." }

$tsvBlock = $match.Groups[1].Value.Trim()
$lines = $tsvBlock -split "`r?`n" | Where-Object { $_.Trim() -ne "" }
if ($lines.Count -lt 2) { throw "TSV sem dados." }

$dataLines = $lines[1..($lines.Count - 1)]
$baseDir = Join-Path $RepoRoot "01-mrp\front_end"
$assetsBase = Join-Path $baseDir "assets\produtos"
New-Item -ItemType Directory -Path $assetsBase -Force | Out-Null

$placeholderPath = Join-Path $assetsBase "_placeholder.svg"
$placeholderSvg = @"
<svg xmlns='http://www.w3.org/2000/svg' width='320' height='180' viewBox='0 0 320 180'>
  <rect width='320' height='180' fill='#1f1f23'/>
  <rect x='8' y='8' width='304' height='164' rx='8' fill='none' stroke='#ed1c24' stroke-width='2'/>
  <text x='16' y='34' font-size='20' fill='#ffffff' font-family='Arial, sans-serif'>DEMO</text>
  <text x='16' y='62' font-size='14' fill='#cccccc' font-family='Arial, sans-serif'>PREVIEW INDISPONIVEL</text>
</svg>
"@
Set-Content -Path $placeholderPath -Value $placeholderSvg -Encoding UTF8

$seed = @()
$id = 1
foreach ($line in $dataLines) {
    $cols = $line -split "`t"
    if ($cols.Count -lt 5) { continue }

    $itemAta = $cols[0].Trim()
    $nome = $cols[1].Trim()
    $arp = $cols[2].Trim()
    $ata = $cols[3].Trim()
    $empresa = $cols[4].Trim()

    if ([string]::IsNullOrWhiteSpace($nome)) { throw "nome_oficial vazio em: $line" }
    if ($nome -eq "Item temporário" -or $nome -eq "Produto exemplo") { throw "Nome proibido em: $line" }

    $empresaKey = Normalize-Key $empresa
    $arpKey = Normalize-Key $arp
    $ataKey = Normalize-Ata $ata
    $itemKey = Normalize-ItemKey $itemAta

    $produtoKey = ("{0}__{1}__{2}__{3}" -f $empresaKey.ToUpperInvariant(), $arpKey.ToUpperInvariant(), $ataKey.ToUpperInvariant(), $itemKey.ToUpperInvariant())
    $pastaRel = "assets/produtos/$empresaKey/$arpKey/$ataKey/$itemKey/"
    $previewRel = "${pastaRel}preview.svg"

    $dir = Join-Path $assetsBase "$empresaKey\$arpKey\$ataKey\$itemKey"
    New-Item -ItemType Directory -Path $dir -Force | Out-Null

    $nomePreview = $nome
    if ($nomePreview.Length -gt 56) { $nomePreview = $nomePreview.Substring(0,56) + "..." }

    $svg = @"
<svg xmlns='http://www.w3.org/2000/svg' width='320' height='180' viewBox='0 0 320 180'>
  <rect width='320' height='180' fill='#1f1f23'/>
  <rect x='8' y='8' width='304' height='164' rx='8' fill='none' stroke='#ed1c24' stroke-width='2'/>
  <text x='16' y='28' font-size='14' fill='#ffffff' font-family='Arial, sans-serif'>DEMO</text>
  <text x='16' y='48' font-size='12' fill='#cccccc' font-family='Arial, sans-serif'>EMPRESA: $(Escape-Xml $empresa)</text>
  <text x='16' y='64' font-size='12' fill='#cccccc' font-family='Arial, sans-serif'>ARP: $(Escape-Xml $arp)</text>
  <text x='16' y='80' font-size='12' fill='#cccccc' font-family='Arial, sans-serif'>ATA: $(Escape-Xml $ata)</text>
  <text x='16' y='96' font-size='12' fill='#cccccc' font-family='Arial, sans-serif'>ITEM: $(Escape-Xml $itemAta)</text>
  <text x='16' y='124' font-size='11' fill='#ffffff' font-family='Arial, sans-serif'>$(Escape-Xml $nomePreview)</text>
</svg>
"@
    Set-Content -Path (Join-Path $dir "preview.svg") -Value $svg -Encoding UTF8

    $seed += [ordered]@{
        id = $id
        produto_key = $produtoKey
        empresa = $empresa
        empresa_key = $empresaKey
        arp = $arp
        arp_key = $arpKey
        ata_numero = $ata
        ata_key = $ataKey
        item_ata = $itemAta
        item_key = $itemKey
        nome_oficial = $nome
        categoria = (Infer-Categoria $nome)
        imagem = [ordered]@{
            pasta = $pastaRel
            preview = $previewRel
            status = "DEMO"
        }
        status = "ATIVO"
    }
    $id++
}

if ($seed.Count -ne 147) { throw "Quantidade invalida: $($seed.Count). Esperado: 147" }

$jsonPath = Join-Path $RepoRoot "01-mrp\front_end\data\produtos_seed.json"
$seed | ConvertTo-Json -Depth 10 | Set-Content -Path $jsonPath -Encoding UTF8

Write-Output "SEED_OK=$($seed.Count)"
