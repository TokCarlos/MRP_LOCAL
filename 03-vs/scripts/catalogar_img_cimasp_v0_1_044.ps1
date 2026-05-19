param(
    [Parameter(Mandatory=$true)] [string]$ZipPath,
    [string]$RepoRoot = "X:\"
)
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Write-Utf8NoBom([string]$Path, [string]$Text) { [System.IO.File]::WriteAllText($Path, $Text, $script:utf8NoBom) }
function Copy-ZipEntry([System.IO.Compression.ZipArchive]$Zip, [string]$EntryName, [string]$Destination) {
    $entry = $Zip.GetEntry($EntryName)
    if ($null -eq $entry) { throw "Entrada nao encontrada no ZIP: $EntryName" }
    $inStream = $entry.Open()
    try { $outStream = [System.IO.File]::Create($Destination); try { $inStream.CopyTo($outStream) } finally { $outStream.Dispose() } } finally { $inStream.Dispose() }
}
function Get-ProdutoArray([string]$Path) {
    $text = [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
    $parsed = $text | ConvertFrom-Json
    $items = @($parsed)
    if ($items.Count -eq 1 -and $items[0].GetType().IsArray) { $items = @($items[0]) }
    return $items
}
$seedPath = Join-Path $RepoRoot "01-mrp\front_end\data\produtos_seed.json"
$imgDir = Join-Path $RepoRoot "01-mrp\front_end\img\produtos\aco\atas\cimasp"
$patchDir = Join-Path $RepoRoot "02-docs\docs\patch\versoes\v0.1.044"
$reportDir = Join-Path $RepoRoot "03-vs\relatorios\correcao_ata_img"
$statusPath = Join-Path $RepoRoot "02-docs\docs\geral\status_geral.md"
$validatorPath = Join-Path $RepoRoot "03-vs\scripts\validar_img_produtos.ps1"
if (!(Test-Path -LiteralPath $ZipPath)) { throw "ZIP nao encontrado: $ZipPath" }
$produtos = Get-ProdutoArray -Path $seedPath
$produtos = @($produtos | Where-Object { -not ($_.arp_key -eq "cimasp" -and ([string]$_.produto_key) -match "^ACO__CIMASP__029_2025__ITEM_\d{3}_1$") })
$cimasp = @($produtos | Where-Object { $_.arp_key -eq "cimasp" -and ([string]$_.item_ata) -match "^\d+$" } | Sort-Object { [int]([string]$_.item_ata) })
if ($cimasp.Count -ne 74) { throw "Esperado 74 produtos CIMASP, encontrado $($cimasp.Count)" }
$variantSources = @{17=@("17-old.png");18=@("18-old.png");19=@("19-1.png");20=@("20-1.png");21=@("21-1.png");25=@("25-1.png");42=@("42-old.png");43=@("43-old.png");44=@("44-1.png");45=@("45-1.png");46=@("46-1.png");47=@("47-1.png");48=@("48-1.png");49=@("49-1.png");55=@("55-1.png");67=@("67-1.png")}
$primarySourceOverride = @{17="17-new.png";18="18-new.png";42="42-new.png";43="43-new.png"}
$zip = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
try {
    $entries = @($zip.Entries | Where-Object { -not $_.FullName.EndsWith("/") })
    $pngEntries = @($entries | Where-Object { $_.FullName -match "\.png$" })
    if ($pngEntries.Count -ne 90) { throw "Esperado 90 PNGs no ZIP, encontrado $($pngEntries.Count)" }
    $entryNames = New-Object "System.Collections.Generic.HashSet[string]"
    foreach ($entry in $entries) { [void]$entryNames.Add([IO.Path]::GetFileName($entry.FullName)) }
    $allNums = New-Object "System.Collections.Generic.HashSet[int]"
    foreach ($entry in $pngEntries) {
        $name = [IO.Path]::GetFileName($entry.FullName)
        if ($name -match "^(\d+)(?:[-_].+)?\.png$") { [void]$allNums.Add([int]$matches[1]) } else { throw "Arquivo fora do padrao numerado: $name" }
    }
    foreach ($n in 1..74) { if (!$allNums.Contains($n)) { throw "Item ausente no ZIP: $n" } }
    $newProdutos = New-Object System.Collections.Generic.List[object]
    foreach ($p in $produtos) { $newProdutos.Add($p) }
    $nextId = [Math]::Max((($produtos | Measure-Object -Property id -Maximum).Maximum + 1), 168)
    $migracoes = New-Object System.Collections.Generic.List[object]
    $variacoes = New-Object System.Collections.Generic.List[object]
    foreach ($p in $cimasp) {
        $itemNum = [int]([string]$p.item_ata)
        $oldPreview = [string]$p.imagem.preview
        $oldStatus = [string]$p.imagem.status
        $baseName = [IO.Path]::GetFileNameWithoutExtension($oldPreview)
        $primarySource = if ($primarySourceOverride.ContainsKey($itemNum)) { $primarySourceOverride[$itemNum] } else { "$itemNum.png" }
        if (!$entryNames.Contains($primarySource)) { throw "PNG principal nao encontrado para item ${itemNum}: $primarySource" }
        $destPrimaryName = "$baseName.png"
        Copy-ZipEntry -Zip $zip -EntryName $primarySource -Destination (Join-Path $imgDir $destPrimaryName)
        $p.imagem.preview = "img/produtos/aco/atas/cimasp/$destPrimaryName"
        $p.imagem.status = "REAL_ATA"
        $migracoes.Add([ordered]@{id=$p.id; item_ata=$p.item_ata; nome_oficial=$p.nome_oficial; imagem_antiga=$oldPreview; imagem_nova=$p.imagem.preview; origem_png=$primarySource; status_antigo=$oldStatus; status_novo="REAL_ATA"; tipo="principal"})
        if ($variantSources.ContainsKey($itemNum)) {
            $idx = 1
            foreach ($variantSource in $variantSources[$itemNum]) {
                if (!$entryNames.Contains($variantSource)) { throw "PNG de variacao nao encontrado para item ${itemNum}: $variantSource" }
                $prefix = "item_$itemNum"
                $variantName = "item_$itemNum`_$idx" + $baseName.Substring($prefix.Length) + ".png"
                Copy-ZipEntry -Zip $zip -EntryName $variantSource -Destination (Join-Path $imgDir $variantName)
                $variantItemAta = "$itemNum-$idx"
                $variantItemKey = ("item_{0:D3}_{1}" -f $itemNum, $idx)
                $variantProdutoKey = ("ACO__CIMASP__029_2025__ITEM_{0:D3}_{1}" -f $itemNum, $idx)
                $clone = [ordered]@{id=$nextId; produto_key=$variantProdutoKey; empresa=$p.empresa; empresa_key=$p.empresa_key; arp=$p.arp; arp_key=$p.arp_key; ata_numero=$p.ata_numero; ata_key=$p.ata_key; item_ata=$variantItemAta; item_key=$variantItemKey; nome_oficial=$p.nome_oficial; categoria=$p.categoria; imagem=[ordered]@{pasta="img/produtos/aco/atas/cimasp/"; preview="img/produtos/aco/atas/cimasp/$variantName"; status="REAL_ATA"}; status=$p.status}
                $newProdutos.Add([pscustomobject]$clone)
                $variacoes.Add([ordered]@{id=$nextId; item_base=[string]$p.item_ata; item_variacao=$variantItemAta; produto_key=$variantProdutoKey; nome_oficial=$p.nome_oficial; imagem_nova=$clone.imagem.preview; origem_png=$variantSource})
                $nextId++; $idx++
            }
        }
    }
    $newProdutosArray = @($newProdutos | Sort-Object {[int]$_.id})
    Write-Utf8NoBom -Path $seedPath -Text (($newProdutosArray | ConvertTo-Json -Depth 20) + [Environment]::NewLine)
    New-Item -ItemType Directory -Force -Path $patchDir | Out-Null
    New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $hashRows = New-Object System.Collections.Generic.List[object]
    foreach ($entry in $pngEntries) { $stream = $entry.Open(); try { $hash = (($sha.ComputeHash($stream) | ForEach-Object { $_.ToString("x2") }) -join ""); $hashRows.Add([pscustomobject]@{arquivo=[IO.Path]::GetFileName($entry.FullName); sha256=$hash; tamanho_bytes=$entry.Length}) } finally { $stream.Dispose() } }
    $duplicidades = @($hashRows | Group-Object sha256 | Where-Object { $_.Count -gt 1 } | ForEach-Object { [ordered]@{arquivos=@($_.Group | Sort-Object arquivo | Select-Object -ExpandProperty arquivo); sha256=$_.Name} })
    $report = [pscustomobject][ordered]@{versao="v0.1.044"; ata="CIMASP"; ata_numero="029/2025"; ata_key="cimasp"; origem_zip=$ZipPath; total_png_zip=$pngEntries.Count; total_itens_cimasp=$cimasp.Count; total_principais_migrados=$migracoes.Count; total_variacoes_criadas=$variacoes.Count; migracoes=$migracoes.ToArray(); variacoes=$variacoes.ToArray(); duplicidades_exatas_no_zip=@($duplicidades); observacao="Nomes oficiais preservados a partir dos registros/SVGs DEMO existentes."}
    Write-Utf8NoBom -Path (Join-Path $reportDir "relatorio_correcao_ata_img_cimasp_v0.1.044.json") -Text (($report | ConvertTo-Json -Depth 30) + [Environment]::NewLine)
    $migrationLines = ($migracoes | ForEach-Object { "- ID $($_.id) item $($_.item_ata): $($_.imagem_antiga) -> $($_.imagem_nova) (origem PNG $($_.origem_png))" }) -join [Environment]::NewLine
    $variantLines = ($variacoes | ForEach-Object { "- ID $($_.id) item $($_.item_variacao): $($_.imagem_nova) (origem PNG $($_.origem_png); nome oficial preservado do item $($_.item_base))" }) -join [Environment]::NewLine
    $duplicateLines = ($duplicidades | ForEach-Object { "- " + ($_.arquivos -join " = ") }) -join [Environment]::NewLine
    Write-Utf8NoBom -Path (Join-Path $reportDir "relatorio_correcao_ata_img_cimasp_v0.1.044.md") -Text ("# Relatorio Correcao ATA/Imagem CIMASP - v0.1.044`n`n- ATA oficial: CIMASP 029/2025`n- Key ATA: cimasp`n- Origem: CIMASP.zip`n- PNGs avaliados no ZIP: $($pngEntries.Count)`n- Itens CIMASP cobertos: $($cimasp.Count)`n- Previews principais migrados: $($migracoes.Count)`n- Variacoes criadas: $($variacoes.Count)`n- Regra aplicada: nomes oficiais preservados a partir dos registros/SVGs DEMO existentes.`n`n## Migracao de preview CIMASP`n$migrationLines`n`n## Variacoes cadastradas`n$variantLines`n`n## Duplicidades exatas observadas no ZIP`n$duplicateLines`n`n## Pendencias`n- Validar visualmente os previews no frontend apos carga.`n- Manter SVGs antigos como referencia visual/demo enquanto nao houver rotina de limpeza aprovada.`n")
    Write-Utf8NoBom -Path (Join-Path $patchDir "registro.md") -Text "# Registro v0.1.044 - Catalogacao imagens CIMASP`n`n## Escopo`n`nCatalogacao das imagens reais da ATA CIMASP 029/2025 no catalogo local de produtos.`n`n## Alteracoes`n`n- Migrados 74 previews CIMASP de SVG DEMO para PNG REAL_ATA.`n- Criadas 16 variacoes de itens quando o ZIP trouxe imagem adicional do mesmo item.`n- Mantidos os nomes oficiais existentes no seed, derivados dos registros/SVGs DEMO atuais.`n- Mantidos os SVGs antigos na pasta de imagens como referencia historica/demo.`n`n## Regra aplicada`n`n- O PNG principal substitui o preview do item existente.`n- A imagem adicional vira item de variacao com sufixo ``-1``, por exemplo ``17-1``.`n- Nao houve alteracao de HTML, CSS ou JavaScript da tela de produtos.`n"
    Write-Utf8NoBom -Path (Join-Path $patchDir "solucao.md") -Text "# Solucao v0.1.044 - CIMASP REAL_ATA`n`n## Decisao`n`nAplicar para CIMASP o mesmo criterio usado em SEHIS/GOV RIO: previews reais em PNG no caminho oficial ``img/produtos/aco/atas/cimasp/``, mantendo SVGs demo como legado.`n`n## Resultado`n`n- 74 produtos CIMASP existentes atualizados para ``imagem.status = REAL_ATA``.`n- 16 novos produtos de variacao adicionados com item ``N-1``.`n- Nomes oficiais preservados sem reescrita.`n- Arquivos PNG nomeados com o mesmo radical dos SVGs oficiais atuais.`n"
    Write-Utf8NoBom -Path (Join-Path $patchDir "validacao.md") -Text "# Validacao v0.1.044 - Imagens CIMASP`n`n## Validacoes previstas`n`n- JSON do seed deve carregar sem erro.`n- Todos os previews CIMASP devem apontar para arquivo fisico PNG.`n- Itens CIMASP devem usar ``imagem.status = REAL_ATA``.`n- Validacao de imagens deve aceitar CIMASP como ATA com PNG real.`n`n## Resultado`n`nA preencher apos execucao dos validadores.`n"
    Write-Utf8NoBom -Path (Join-Path $patchDir "arquivos_alterados.md") -Text "# Arquivos alterados v0.1.044`n`n## Dados`n`n- ``01-mrp/front_end/data/produtos_seed.json```n`n## Imagens`n`n- ``01-mrp/front_end/img/produtos/aco/atas/cimasp/*.png```n`n## Scripts`n`n- ``03-vs/scripts/validar_img_produtos.ps1```n- ``03-vs/scripts/catalogar_img_cimasp_v0_1_044.ps1```n`n## Documentacao e relatorios`n`n- ``02-docs/docs/patch/versoes/v0.1.044/registro.md```n- ``02-docs/docs/patch/versoes/v0.1.044/solucao.md```n- ``02-docs/docs/patch/versoes/v0.1.044/validacao.md```n- ``02-docs/docs/patch/versoes/v0.1.044/arquivos_alterados.md```n- ``03-vs/relatorios/correcao_ata_img/relatorio_correcao_ata_img_cimasp_v0.1.044.md```n- ``03-vs/relatorios/correcao_ata_img/relatorio_correcao_ata_img_cimasp_v0.1.044.json```n- ``02-docs/docs/geral/status_geral.md```n"
    $statusText = [System.IO.File]::ReadAllText($statusPath, [System.Text.Encoding]::UTF8)
    $statusText = $statusText -replace "``v0\.1\.043-preparacao-portabilidade``", "``v0.1.044-catalogacao-imagens-cimasp``"
    if ($statusText -notmatch "Catalogacao imagens CIMASP v0\.1\.044") { $statusText = $statusText.TrimEnd() + "`n`n## Catalogacao imagens CIMASP v0.1.044`n`n- ATA CIMASP 029/2025 migrada de previews SVG DEMO para PNG REAL_ATA.`n- Variacoes de itens registradas com sufixo ``-1`` quando havia imagem adicional no ZIP.`n- Nomes oficiais preservados a partir dos registros existentes.`n" }
    Write-Utf8NoBom -Path $statusPath -Text $statusText
    $validatorText = [System.IO.File]::ReadAllText($validatorPath, [System.Text.Encoding]::UTF8)
    if ($validatorText -notmatch "cimaspTotal") { $validatorText = $validatorText -replace "(\`$realAta = 0)", "`$1`n`$cimaspTotal = 0`n`$cimaspReal = 0" }
    if ($validatorText -notmatch 'arpKey -eq "cimasp"') {
        $insert = @'

    if ($arpKey -eq "cimasp") {
        $cimaspTotal++
        if ($imgStatus -eq "REAL_ATA") { $cimaspReal++ }
        if ($imgStatus -ne "REAL_ATA") { $erros.Add("ID $id CIMASP com status '$imgStatus' (esperado REAL_ATA)") }
        if ($preview -notmatch "\.png$") { $erros.Add("ID $id CIMASP deve apontar para PNG real") }
        if ($preview -match "\.svg$") { $erros.Add("ID $id CIMASP ainda aponta para SVG demo") }
        if ($preview -notmatch "^img/produtos/(aco|jpl)/atas/cimasp/") { $erros.Add("ID $id CIMASP com caminho fora do padrao oficial") }
    }
'@
        $validatorText = [regex]::Replace($validatorText, "(\s+if \(\`$id -ge 148 -and \`$id -le 167\) \{)", ([string]$insert) + '$1')
    }
    if ($validatorText -notmatch "Total CIMASP REAL_ATA") {
        $validatorText = [regex]::Replace($validatorText, '(Write-Host "Total REAL_ATA: \$realAta")', '$1' + "`nWrite-Host `"Total CIMASP: `$cimaspTotal`"`nWrite-Host `"Total CIMASP REAL_ATA: `$cimaspReal`"")
    }
    Write-Utf8NoBom -Path $validatorPath -Text $validatorText
    Write-Host "CIMASP migrado: $($migracoes.Count) principais, $($variacoes.Count) variacoes, $($pngEntries.Count) PNGs no ZIP. Proximo ID: $nextId"
} finally { $zip.Dispose() }
