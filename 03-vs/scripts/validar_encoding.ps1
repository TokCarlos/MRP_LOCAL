$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$ReportDir = Join-Path $RepoRoot "03-vs\relatorios\encoding"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$Exts = @(".json", ".js", ".css", ".html", ".md", ".ps1", ".csv", ".txt")
$IgnorePathRegex = "\\.git(\\|$)|node_modules(\\|$)|03-vs\\patches(\\|$)|03-vs\\snapshots(\\|$)|03-vs\\quarentena(\\|$)|03-vs\\relatorios\\encoding(\\|$)"

# ASCII-safe regexes. They detect UTF-8 bytes that were decoded as ANSI/Latin-1,
# without embedding mojibake literals inside this script.
$MojibakeRegexes = @(
    "[\u00C2\u00C3][\u0080-\u00BF]",
    "\u00C3[\u0192\u2020\u2021\u0160\u0161\u017D\u017E\u00A0-\u00BF]",
    "\u00E2[\u0080-\u20AC][\u0080-\u2122]?"
)

function Read-Utf8 {
    param([string]$Path)

    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return [System.Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
    }

    return [System.Text.Encoding]::UTF8.GetString($bytes)
}

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Text
    )

    $normalized = (($Text -split "\r?\n") | ForEach-Object { $_.TrimEnd() }) -join "`n"
    $normalized = $normalized.TrimEnd() + "`n"
    [System.IO.File]::WriteAllText($Path, $normalized, $Utf8NoBom)
}

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

function Add-Issue {
    param(
        [System.Collections.Generic.List[object]]$Issues,
        [string]$Tipo,
        [string]$Arquivo,
        [string]$Detalhe,
        [string]$Risco = "ALTO_RISCO"
    )

    $Issues.Add([pscustomobject]@{
        tipo = $Tipo
        arquivo = $Arquivo
        detalhe = $Detalhe
        risco = $Risco
    })
}

$files = Get-ChildItem -Path $RepoRoot -Recurse -File -Force -ErrorAction SilentlyContinue |
    Where-Object {
        $Exts -contains $_.Extension.ToLowerInvariant() -and
        $_.FullName -notmatch $IgnorePathRegex -and
        $_.FullName -ne $MyInvocation.MyCommand.Path
    }

$issues = New-Object System.Collections.Generic.List[object]
$scanned = 0
$ignored = 0

foreach ($f in $files) {
    $scanned++

    try {
        $txt = Read-Utf8 -Path $f.FullName
    } catch {
        Add-Issue -Issues $issues -Tipo "READ_FAIL" -Arquivo $f.FullName -Detalhe $_.Exception.Message -Risco "REVISAR_MANUALMENTE"
        continue
    }

    foreach ($rx in $MojibakeRegexes) {
        $match = [regex]::Match($txt, $rx)
        if ($match.Success) {
            Add-Issue -Issues $issues -Tipo "POSSIVEL_MOJIBAKE" -Arquivo $f.FullName -Detalhe "Padrao Unicode suspeito detectado: U+$([int][char]$match.Value[0])."
            break
        }
    }

    $ataCanonica = "SEHIS - GOV. RIO 114443801/2025"
    $ataDuplicada = "$ataCanonica (SEHIS - GOV. RIO)"
    if ($txt.Contains($ataDuplicada)) {
        Add-Issue -Issues $issues -Tipo "ATA_LABEL_DUPLICADA" -Arquivo $f.FullName -Detalhe "Forma com parenteses bloqueada."
    }

    if ($f.Name -eq "produtos_seed.json") {
        try {
            $arr = $txt | ConvertFrom-Json
            foreach ($p in $arr) {
                $empresa = [string]$p.empresa
                $empresaKey = [string]$p.empresa_key
                $empresaNorm = Normalize-Text -Value $empresa

                if ($empresaKey -eq "aco" -and $empresaNorm -ne "ACO") {
                    Add-Issue -Issues $issues -Tipo "EMPRESA_VISUAL_INVALIDA" -Arquivo $f.FullName -Detalhe "id=$($p.id) empresa='$empresa' key='$empresaKey'"
                }

                if ($empresaKey -ne "" -and $empresaKey -ne "jpl" -and $empresaKey -ne "aco" -and $empresaKey -ne "tcr") {
                    Add-Issue -Issues $issues -Tipo "EMPRESA_KEY_INVALIDA" -Arquivo $f.FullName -Detalhe "id=$($p.id) empresa_key='$empresaKey'"
                }

                if ($empresa -match "GOV|SEHIS" -or $empresaKey -match "gov_rio|sehis") {
                    Add-Issue -Issues $issues -Tipo "DOMINIO_EMPRESA_INVALIDO" -Arquivo $f.FullName -Detalhe "id=$($p.id) empresa='$empresa' key='$empresaKey'"
                }
            }
        } catch {
            Add-Issue -Issues $issues -Tipo "JSON_INVALIDO" -Arquivo $f.FullName -Detalhe $_.Exception.Message
        }
    }
}

$status = if ($issues.Count -eq 0) { "OK" } else { "ERRO" }
$blockers = @($issues | Where-Object { $_.risco -eq "ALTO_RISCO" }).Count

$obj = [ordered]@{
    status = $status
    arquivos_analisados = $scanned
    arquivos_ignorados = $ignored
    ocorrencias_restantes = $issues.Count
    erros_bloqueadores = $blockers
    itens = $issues
}

$json = $obj | ConvertTo-Json -Depth 8
Write-Utf8NoBom -Path (Join-Path $ReportDir "relatorio_encoding.json") -Text $json

$md = @()
$md += "# Relatorio de Encoding"
$md += ""
$md += "- Status: $status"
$md += "- Arquivos analisados: $scanned"
$md += "- Ocorrencias restantes: $($issues.Count)"
$md += "- Erros bloqueadores: $blockers"
$md += ""
$md += "## Itens"

if ($issues.Count -eq 0) {
    $md += "- Nenhuma ocorrencia bloqueadora detectada."
} else {
    foreach ($i in $issues) {
        $md += "- [$($i.tipo)] $($i.arquivo) :: $($i.detalhe)"
    }
}

Write-Utf8NoBom -Path (Join-Path $ReportDir "relatorio_encoding.md") -Text ($md -join [Environment]::NewLine)

Write-Host "STATUS=$status"
Write-Host "ARQUIVOS_ANALISADOS=$scanned"
Write-Host "OCORRENCIAS=$($issues.Count)"
Write-Host "ERROS_BLOQUEADORES=$blockers"

if ($issues.Count -gt 0) { exit 1 }
exit 0
