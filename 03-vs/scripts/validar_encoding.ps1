$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..\..")
$ReportDir = Join-Path $RepoRoot "03-vs\relatorios\encoding"
New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null

$Exts = @(".json", ".js", ".css", ".html", ".md", ".ps1", ".csv", ".txt")
$IgnorePathRegex = "\\.git(\\|$)|node_modules(\\|$)|03-vs\\patches(\\|$)|03-vs\\snapshots(\\|$)|03-vs\\quarentena(\\|$)|03-vs\\relatorios\\encoding(\\|$)"

$BadPatterns = @(
  "AÃ‡O", "AÃ§O", "DESCRIÃ‡", "FAMÃ", "NÃº", "NÃš", "CÃ³", "CÃ“", "INFORMAÃ‡", "SITUAÃ‡", "MEDIÃ‡", "OPÃ‡", "REVISÃ", "ATENÃ‡", "MARICÃ", "Âº", "Âª", "â€“"
)

function Read-Utf8([string]$Path) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return [System.Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
    }
    return [System.Text.Encoding]::UTF8.GetString($bytes)
}

function Normalize-Text([string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return "" }
    $formD = $Value.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($c in $formD.ToCharArray()) {
        $cat = [Globalization.CharUnicodeInfo]::GetUnicodeCategory($c)
        if ($cat -ne [Globalization.UnicodeCategory]::NonSpacingMark) { [void]$sb.Append($c) }
    }
    return $sb.ToString().ToUpperInvariant().Trim()
}

$files = Get-ChildItem -Path $RepoRoot -Recurse -File -Force -ErrorAction SilentlyContinue |
    Where-Object { $Exts -contains $_.Extension.ToLower() -and $_.FullName -notmatch $IgnorePathRegex }

$issues = New-Object System.Collections.Generic.List[object]
$scanned = 0
$ignored = 0

foreach ($f in $files) {
    $scanned++
    try {
        $txt = Read-Utf8 $f.FullName
    } catch {
        $issues.Add([pscustomobject]@{ tipo = "READ_FAIL"; arquivo = $f.FullName; detalhe = $_.Exception.Message; risco = "REVISAR_MANUALMENTE" })
        continue
    }

    foreach ($p in $BadPatterns) {
        if ($txt.Contains($p)) {
            $issues.Add([pscustomobject]@{ tipo = "POSSIVEL_MOJIBAKE"; arquivo = $f.FullName; detalhe = "Padrao detectado: $p"; risco = "ALTO_RISCO" })
            break
        }
    }

    $ataCanonica = "SEHIS - GOV. RIO 114443801/2025"
    $ataDuplicada = "$ataCanonica (" + "SEHIS - GOV. RIO" + ")"
    if ($txt.Contains($ataDuplicada)) {
        $issues.Add([pscustomobject]@{ tipo = "ATA_LABEL_DUPLICADA"; arquivo = $f.FullName; detalhe = "Forma com parenteses bloqueada"; risco = "ALTO_RISCO" })
    }

    if ($f.Name -eq "produtos_seed.json") {
        try {
            $arr = $txt | ConvertFrom-Json
            foreach ($p in $arr) {
                $empresa = [string]$p.empresa
                $empresaKey = [string]$p.empresa_key
                $empresaNorm = Normalize-Text $empresa

                if ($empresaKey -eq "aco" -and $empresaNorm -ne "ACO") {
                    $issues.Add([pscustomobject]@{ tipo = "EMPRESA_VISUAL_INVALIDA"; arquivo = $f.FullName; detalhe = "id=$($p.id) empresa='$empresa' key='$empresaKey'"; risco = "ALTO_RISCO" })
                }
                if ($empresaKey -eq "AÇO" -or $empresaKey -eq "AÃ‡O") {
                    $issues.Add([pscustomobject]@{ tipo = "EMPRESA_KEY_INVALIDA"; arquivo = $f.FullName; detalhe = "id=$($p.id) empresa_key='$empresaKey'"; risco = "ALTO_RISCO" })
                }
                if ($empresa -match "GOV|SEHIS" -or $empresaKey -match "gov_rio|sehis") {
                    $issues.Add([pscustomobject]@{ tipo = "DOMINIO_EMPRESA_INVALIDO"; arquivo = $f.FullName; detalhe = "id=$($p.id) empresa='$empresa' key='$empresaKey'"; risco = "ALTO_RISCO" })
                }
            }
        } catch {
            $issues.Add([pscustomobject]@{ tipo = "JSON_INVALIDO"; arquivo = $f.FullName; detalhe = $_.Exception.Message; risco = "ALTO_RISCO" })
        }
    }
}

$status = if ($issues.Count -eq 0) { "OK" } else { "ERRO" }

$obj = [ordered]@{
    status = $status
    arquivos_analisados = $scanned
    arquivos_ignorados = $ignored
    ocorrencias_restantes = $issues.Count
    erros_bloqueadores = ($issues | Where-Object { $_.risco -eq "ALTO_RISCO" }).Count
    itens = $issues
}
$obj | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -Path (Join-Path $ReportDir "relatorio_encoding.json")

$md = @()
$md += "# Relatorio de Encoding"
$md += ""
$md += "- Status: $status"
$md += "- Arquivos analisados: $scanned"
$md += "- Ocorrencias restantes: $($issues.Count)"
$md += "- Erros bloqueadores: $(($issues | Where-Object { $_.risco -eq 'ALTO_RISCO' }).Count)"
$md += ""
$md += "## Itens"
if ($issues.Count -eq 0) {
    $md += "- Nenhuma ocorrencia bloqueadora detectada."
} else {
    foreach ($i in $issues) {
        $md += "- [$($i.tipo)] $($i.arquivo) :: $($i.detalhe)"
    }
}
$md | Set-Content -Encoding UTF8 -Path (Join-Path $ReportDir "relatorio_encoding.md")

Write-Host "STATUS=$status"
Write-Host "ARQUIVOS_ANALISADOS=$scanned"
Write-Host "OCORRENCIAS=$($issues.Count)"
if ($issues.Count -gt 0) { exit 1 }
exit 0
