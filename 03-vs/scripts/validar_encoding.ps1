param(
    [ValidateSet("Ativo", "Completo")]
    [string]$Modo = "Ativo"
)
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
$reportDir = Join-Path $root "03-vs\relatorios\encoding"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

function Get-Rel([string]$p) { return $p.Substring($root.Length).TrimStart("\\") -replace "\\", "/" }
function Has-BomUtf8([byte[]]$b) { return $b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF }
function Test-Utf8([byte[]]$b) {
    try { $enc = [System.Text.UTF8Encoding]::new($false, $true); $null = $enc.GetString($b); return $true } catch { return $false }
}
function Write-Utf8NoBom([string]$path, [string]$text) { [System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false)) }

$textExt = @(".txt", ".md", ".json", ".ps1", ".js", ".css", ".html", ".xml", ".svg", ".toml", ".csv", ".bat", ".cmd")
$skip = @(".git", "node_modules", ".venv", "venv")
if ($Modo -eq "Ativo") { $skip += @("03-vs/patches", "03-vs/snapshots", "03-vs/quarentena", "03-vs/relatorios") }
$files = Get-ChildItem -Path $root -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {
    $rel = Get-Rel $_.FullName
    $ok = $true
    foreach ($s in $skip) { if ($rel -like "$s/*" -or $rel -eq $s) { $ok = $false } }
    if ($rel -eq "03-vs/scripts/validar_encoding.ps1") { $ok = $false }
    $ok -and ($textExt -contains $_.Extension.ToLower() -or $_.Name -eq ".gitignore")
}
$issues = @()
foreach ($f in $files) {
    $rel = Get-Rel $f.FullName
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    if (Has-BomUtf8 $bytes) { $issues += [pscustomobject]@{tipo="UTF8_BOM";arquivo=$rel;risco="MEDIO"} }
    if (-not (Test-Utf8 $bytes)) { $issues += [pscustomobject]@{tipo="NAO_UTF8_VALIDO";arquivo=$rel;risco="ALTO"}; continue }
    $txt = [System.Text.Encoding]::UTF8.GetString($(if (Has-BomUtf8 $bytes) { $bytes[3..($bytes.Length-1)] } else { $bytes }))
    if ($txt -match "VersÃ|AÃ‡O|CORRIMÃƒO|ÃƒO|Ã§|Ã£|Ã©|Ã¡|Ã³|Ãº|â€”|â€“|�") {
        $issues += [pscustomobject]@{tipo="POSSIVEL_MOJIBAKE";arquivo=$rel;risco="ALTO"}
    }
}
$status = if ($issues.Count -eq 0) { "OK" } else { "ERRO" }
$obj = [ordered]@{ gerado_em=(Get-Date).ToString("yyyy-MM-dd HH:mm:ss"); modo=$Modo; status=$status; arquivos_analisados=$files.Count; ocorrencias=$issues.Count; itens=$issues }
$json = $obj | ConvertTo-Json -Depth 6
Write-Utf8NoBom (Join-Path $reportDir "relatorio_encoding.json") $json
$md = @("# Relatorio de Encoding", "", "- Status: $status", "- Modo: $Modo", "- Arquivos analisados: $($files.Count)", "- Ocorrencias: $($issues.Count)", "")
if ($issues.Count -gt 0) { $md += "## Itens"; foreach ($i in $issues) { $md += "- [$($i.tipo)] $($i.arquivo) :: risco=$($i.risco)" } }
Write-Utf8NoBom (Join-Path $reportDir "relatorio_encoding.md") ($md -join "`n")
Write-Host "ENCODING_STATUS=$status"
Write-Host "OCORRENCIAS=$($issues.Count)"
if ($issues.Count -gt 0) { exit 1 }
exit 0
