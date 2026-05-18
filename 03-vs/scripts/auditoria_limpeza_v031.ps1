$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
$RootPrefix = $RepoRoot.TrimEnd("\") + "\"
$reportDir = Join-Path $RepoRoot "03-vs\relatorios\limpeza"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

function Get-RelPath {
  param([string]$Path)
  $full = [System.IO.Path]::GetFullPath($Path)
  if ($full.StartsWith($RootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    return $full.Substring($RootPrefix.Length).Replace("\", "/")
  }
  return $full.Replace("\", "/")
}

function Read-Utf8Text {
  param([string]$Path)
  $bytes = [System.IO.File]::ReadAllBytes($Path)
  if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    return [System.Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
  }
  return [System.Text.Encoding]::UTF8.GetString($bytes)
}

$allFiles = Get-ChildItem -Path $RepoRoot -Recurse -File -Force -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notmatch "\\.git(\\|$)" }
$allDirs = Get-ChildItem -Path $RepoRoot -Recurse -Directory -Force -ErrorAction SilentlyContinue |
  Where-Object { $_.FullName -notmatch "\\.git(\\|$)" }

$imgExt = @(".png",".jpg",".jpeg",".webp",".svg",".gif",".ico")
$textExt = @(".html",".js",".css",".json",".md")
$tempRegex = "(?i)(\.tmp$|\.temp$|\.bak$|\.old$|\.orig$|\.backup$|~$|(^|[\\/])\.~|thumbs\.db$|desktop\.ini$|\.ds_store$|^copy\b|^copia\b|^backup\b|^temp\b)"

$tempFiles = $allFiles | Where-Object { $_.Name -match $tempRegex }

$devDirNames = @("node_modules","dist","build",".cache",".vite","coverage",".pytest_cache","__pycache__",".mypy_cache",".ruff_cache",".venv")
$devDirs = $allDirs | Where-Object { $devDirNames -contains $_.Name }
$devFiles = $allFiles | Where-Object { $_.Extension -in @(".pyc",".pyo") -or $_.Name -in @(".eslintcache","yarn.lock","pnpm-lock.yaml","package-lock.json") }

$imgFiles = $allFiles | Where-Object { $imgExt -contains $_.Extension.ToLower() }
$textFiles = $allFiles | Where-Object { $textExt -contains $_.Extension.ToLower() }

$references = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
foreach ($tf in $textFiles) {
  $relTextPath = Get-RelPath $tf.FullName
  if ($relTextPath -match "^02-docs/docs/patch/versoes/|^03-vs/relatorios/|^03-vs/quarentena/") { continue }
  try {
    $content = Read-Utf8Text $tf.FullName
    foreach ($m in [regex]::Matches($content, "(?i)(img/[\w\-\./]+\.(png|jpg|jpeg|webp|svg|gif|ico)|assets/produtos/[\w\-\./]+\.(png|jpg|jpeg|webp|svg|gif|ico))")) {
      [void]$references.Add($m.Value.Replace("\","/"))
    }
  } catch {}
}

$orphans = @()
$assetsOld = @()
foreach ($img in $imgFiles) {
  $rel = Get-RelPath $img.FullName
  $class = "REVISAR_MANUALMENTE"
  if ($references.Contains($rel)) { $class = "REFERENCIADA" }
  elseif ($rel -like "01-mrp/front_end/assets/*") { $class = "LEGADO_PROVAVEL" }
  else { $class = "ORFA_PROVAVEL" }

  if ($class -ne "REFERENCIADA") {
    $orphans += [pscustomobject]@{ path = $rel; classe = $class; size_bytes = $img.Length }
  }

  if ($rel -like "01-mrp/front_end/assets/produtos*") {
    $assetsOld += [pscustomobject]@{
      path = $rel
      referenciada = $references.Contains($rel)
      classe = if ($references.Contains($rel)) {"LEGADO_REFERENCIADO"} else {"LEGADO_NAO_REFERENCIADO"}
    }
  }
}

$dataIssues = @()
$dataDir = Join-Path $RepoRoot "01-mrp\front_end\data"
$frontEndDir = Join-Path $RepoRoot "01-mrp\front_end"
if (Test-Path $dataDir) {
  $jsonFiles = Get-ChildItem -Path $dataDir -File -Filter *.json -ErrorAction SilentlyContinue
  foreach ($jf in $jsonFiles) {
    try { $null = Read-Utf8Text $jf.FullName | ConvertFrom-Json }
    catch { $dataIssues += [pscustomobject]@{tipo="JSON_INVALIDO";arquivo=(Get-RelPath $jf.FullName);detalhe=$_.Exception.Message} }
  }

  $seedPath = Join-Path $dataDir "produtos_seed.json"
  if (Test-Path $seedPath) {
    $seed = Read-Utf8Text $seedPath | ConvertFrom-Json
    $dupKeys = $seed | Group-Object produto_key | Where-Object { $_.Count -gt 1 }
    foreach ($g in $dupKeys) {
      $dataIssues += [pscustomobject]@{tipo="DUPLICIDADE_PRODUTO_KEY";arquivo="01-mrp/front_end/data/produtos_seed.json";detalhe="produto_key '$($g.Name)' repetida $($g.Count)x"}
    }

    foreach ($p in $seed) {
      $empresa = [string]$p.empresa
      $empresaKey = [string]$p.empresa_key
      if ($empresa -match "GOV|SEHIS" -or $empresaKey -match "gov_rio|sehis") {
        $dataIssues += [pscustomobject]@{tipo="DOMINIO_EMPRESA_SUSPEITO";arquivo="01-mrp/front_end/data/produtos_seed.json";detalhe="id=$($p.id) empresa='$empresa' empresa_key='$empresaKey'"}
      }

      $preview = ""
      if ($p.PSObject.Properties.Name -contains "imagem" -and $p.imagem) { $preview = [string]$p.imagem.preview }
      if ([string]::IsNullOrWhiteSpace($preview)) {
        $dataIssues += [pscustomobject]@{tipo="SEM_IMAGEM_PREVIEW";arquivo="01-mrp/front_end/data/produtos_seed.json";detalhe="id=$($p.id)"}
      } else {
        if ($preview -like "assets/produtos*") {
          $dataIssues += [pscustomobject]@{tipo="PREVIEW_CAMINHO_ANTIGO";arquivo="01-mrp/front_end/data/produtos_seed.json";detalhe="id=$($p.id) preview='$preview'"}
        }
        $previewAbs = Join-Path $frontEndDir ($preview -replace "/","\")
        if (-not (Test-Path $previewAbs)) {
          $dataIssues += [pscustomobject]@{tipo="PREVIEW_INEXISTENTE";arquivo="01-mrp/front_end/data/produtos_seed.json";detalhe="id=$($p.id) preview='$preview'"}
        }
      }
    }
  }
}

$frontNonRef = @()
$frontRoot = Join-Path $RepoRoot "01-mrp\front_end"
if (Test-Path $frontRoot) {
  $frontFiles = Get-ChildItem -Path $frontRoot -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Extension -in @(".js",".css",".html") }
  $blob = ""
  foreach ($ff in $frontFiles) {
    try { $blob += "`n" + (Read-Utf8Text $ff.FullName) } catch {}
  }
  foreach ($ff in $frontFiles) {
    if ($blob -notmatch [regex]::Escape($ff.Name)) {
      $frontNonRef += [pscustomobject]@{path=(Get-RelPath $ff.FullName);classe="NAO_REFERENCIADO_PROVAVEL"}
    }
  }
}

$docsFindings = @()
$docRoots = @((Join-Path $RepoRoot "02-docs"),(Join-Path $RepoRoot "03-vs"))
foreach ($dr in $docRoots) {
  if (Test-Path $dr) {
    $cand = Get-ChildItem -Path $dr -Recurse -File -Include "*status*.md","README.md","*manifesto*.json" -ErrorAction SilentlyContinue
    foreach ($f in $cand) {
      try {
        $t = Read-Utf8Text $f.FullName
        if ($t -match "v0\.1\.003") {
          $docsFindings += [pscustomobject]@{path=(Get-RelPath $f.FullName);issue="VERSAO_ANTIGA_MENCIONADA";risco="REVISAR_MANUALMENTE"}
        }
      } catch {}
    }
  }
}

$forbiddenFound = @()
$forbidden = @(
  Join-Path $RepoRoot "01-mrp\front_end\assets\produtos\gov_rio",
  Join-Path $RepoRoot "01-mrp\front_end\assets\produtos\sehis",
  Join-Path $RepoRoot "01-mrp\front_end\img\produtos\gov_rio",
  Join-Path $RepoRoot "01-mrp\front_end\img\produtos\sehis"
)
foreach ($fp in $forbidden) {
  if (Test-Path $fp) { $forbiddenFound += (Get-RelPath $fp) }
}

$gt5 = $allFiles | Where-Object { $_.Length -gt 5MB } | Sort-Object Length -Descending
$gt20 = $allFiles | Where-Object { $_.Length -gt 20MB } | Sort-Object Length -Descending
$gt100 = $allFiles | Where-Object { $_.Length -gt 100MB } | Sort-Object Length -Descending

$largeRows = $gt5 | ForEach-Object {
  $k = if ($_.Extension -in @(".zip",".rar",".7z")) {"PACOTE"} elseif ($imgExt -contains $_.Extension.ToLower()) {"IMAGEM"} else {"REVISAR_MANUALMENTE"}
  [pscustomobject]@{path=(Get-RelPath $_.FullName);size_mb=[math]::Round($_.Length/1MB,2);classe=$k}
}

$packs = $allFiles | Where-Object { $_.Extension.ToLower() -in @(".zip", ".rar", ".7z") } | Sort-Object LastWriteTime -Descending

$brokenRefs = @()
foreach ($r in $references) {
  $abs = Join-Path $frontEndDir ($r -replace "^01-mrp/front_end/", "" -replace "/","\")
  if ($r -like "01-mrp/front_end/*") { $abs = Join-Path $RepoRoot ($r -replace "/","\") }
  if (-not (Test-Path $abs)) {
    $brokenRefs += [pscustomobject]@{referencia=$r;classe="REFERENCIA_QUEBRADA"}
  }
}

$orphans | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $reportDir "arquivos_orfaos.csv")
$assetsOld | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $reportDir "assets_antigos.csv")
$brokenRefs | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $reportDir "referencias_quebradas.csv")
$largeRows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path (Join-Path $reportDir "arquivos_grandes.csv")

$summary = [ordered]@{
  total_arquivos = $allFiles.Count
  total_pastas = $allDirs.Count
  temporarios = $tempFiles.Count
  residuos_dev = ($devDirs.Count + $devFiles.Count)
  imagens_orfas_provaveis = ($orphans | Where-Object { $_.classe -eq "ORFA_PROVAVEL" }).Count
  imagens_legado = ($orphans | Where-Object { $_.classe -like "LEGADO*" }).Count
  referencias_quebradas = $brokenRefs.Count
  arquivos_grandes_gt_5mb = $gt5.Count
  arquivos_grandes_gt_20mb = $gt20.Count
  arquivos_grandes_gt_100mb = $gt100.Count
  revisar_manualmente = ($frontNonRef.Count + $docsFindings.Count)
}

$reportObj = [ordered]@{
  gerado_em = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
  raiz_detectada = $RepoRoot
  resumo = $summary
  categorias = [ordered]@{
    temporarios = @($tempFiles | ForEach-Object { Get-RelPath $_.FullName })
    residuos_dev_dirs = @($devDirs | ForEach-Object { Get-RelPath $_.FullName })
    residuos_dev_files = @($devFiles | ForEach-Object { Get-RelPath $_.FullName })
    estrutura_proibida_encontrada = $forbiddenFound
    json_seed_issues = $dataIssues
    nao_referenciados_provaveis = $frontNonRef
    docs_inconsistencias = $docsFindings
    pacotes = @($packs | ForEach-Object { [pscustomobject]@{path=(Get-RelPath $_.FullName);size_mb=[math]::Round($_.Length/1MB,2)} })
  }
}

$reportObj | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -Path (Join-Path $reportDir "relatorio_limpeza.json")

$md = @()
$md += "# Relatorio de Limpeza (Nao Destrutivo)"
$md += ""
$md += "## 1. Resumo executivo"
$md += "- Raiz detectada: `$RepoRoot`"
$md += "- Total de arquivos analisados: $($summary.total_arquivos)"
$md += "- Total de pastas analisadas: $($summary.total_pastas)"
$md += "- Temporarios suspeitos: $($summary.temporarios)"
$md += "- Residuos de desenvolvimento: $($summary.residuos_dev)"
$md += "- Arquivos orfaos provaveis: $($summary.imagens_orfas_provaveis)"
$md += "- Assets legado detectados: $($assetsOld.Count)"
$md += "- Referencias quebradas: $($summary.referencias_quebradas)"
$md += "- Arquivos grandes (>5MB): $($summary.arquivos_grandes_gt_5mb)"
$md += "- Itens para revisao manual: $($summary.revisar_manualmente)"
$md += "- Risco geral da limpeza: BAIXO/MEDIO"
$md += ""
$md += "## 2. Lista por categoria"
$md += "- Temporarios: $($summary.temporarios)"
$md += "- Cache/build: $($summary.residuos_dev)"
$md += "- Imagens orfas provaveis: $($summary.imagens_orfas_provaveis)"
$md += "- Assets antigos: $($assetsOld.Count)"
$md += "- JSON/seed suspeitos: $($dataIssues.Count)"
$md += "- Codigo nao referenciado provavel: $($frontNonRef.Count)"
$md += "- Docs inconsistentes: $($docsFindings.Count)"
$md += "- ZIP/pacotes: $($packs.Count)"
$md += ""
$md += "## 3. Classificacao de risco"
$md += "- BAIXO_RISCO: temporarios reais e caches."
$md += "- MEDIO_RISCO: assets legado, pacotes antigos e imagens nao referenciadas."
$md += "- ALTO_RISCO: seed, js, css, html e imagens ativas de produto."
$md += "- REVISAR_MANUALMENTE: itens ambiguos."
$md += ""
$md += "## 4. Plano de limpeza proposto"
$md += "- FASE 1: remover somente temporarios reais/cache."
$md += "- FASE 2: manter assets antigos em quarentena, sem apagar definitivo."
$md += "- FASE 3: revisar seed/scripts/docs antes de qualquer remocao."
$md += "- FASE 4: gerar patch futuro aprovado."
$md += ""
$md += "## 5. Comandos sugeridos (nao executados)"
$md += "```powershell"
$md += "# powershell -File .\\03-vs\\scripts\\validar_img_produtos.ps1"
$md += "# powershell -File .\\03-vs\\scripts\\validar_dominio_empresas.ps1"
$md += "# powershell -File .\\03-vs\\scripts\\validar_encoding.ps1"
$md += "```"
$md | Set-Content -Encoding UTF8 -Path (Join-Path $reportDir "relatorio_limpeza.md")

Write-Host "STATUS=OK"
Write-Host "RAIZ=$RepoRoot"
Write-Host "ARQUIVOS=$($summary.total_arquivos)"
Write-Host "REFERENCIAS_QUEBRADAS=$($summary.referencias_quebradas)"
Write-Host "JSON_SEED_ISSUES=$($dataIssues.Count)"
exit 0
