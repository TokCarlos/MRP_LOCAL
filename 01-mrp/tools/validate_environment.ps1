$ErrorActionPreference = "Stop"

$OfficialRoot = "C:\Users\carlo\Desktop\PCP SERVIDOR\SISTEMA_MRP"
$ForbiddenPcp = "C:\Users\carlo\Desktop\PCP SERVIDOR\PCP"
$ForbiddenRoots = @(
    "C:\system_jpl",
    "C:\MRP_REDE_FAKE",
    "C:\SISTEMA_MRP",
    $ForbiddenPcp
)
$ShareName = "system_jpl"
$NetworkPath = "\\HOME-MACHINE\system_jpl"
$MappedDrive = "X:\"

function Normalize-PathText {
    param([Parameter(Mandatory = $true)][string]$Path)
    return ([System.IO.Path]::GetFullPath($Path).TrimEnd("\"))
}

function Test-DirectCRoot {
    param([Parameter(Mandatory = $true)][string]$Path)
    $normalized = Normalize-PathText -Path $Path
    return ($normalized -match '^[cC]:\\[^\\]+$')
}

function Add-ValidationResult {
    param(
        [Parameter(Mandatory = $true)][object]$Results,
        [Parameter(Mandatory = $true)][string]$Check,
        [Parameter(Mandatory = $true)][bool]$Ok,
        [Parameter(Mandatory = $true)][string]$Detail
    )

    $Results.Add([pscustomobject]@{
        check = $Check
        ok = $Ok
        detail = $Detail
    }) | Out-Null
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Text,
        [switch]$Append
    )

    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)
    if ($Append -and (Test-Path -LiteralPath $Path)) {
        [System.IO.File]::AppendAllText($Path, $Text, $encoding)
    } else {
        [System.IO.File]::WriteAllText($Path, $Text, $encoding)
    }
}

$results = New-Object 'System.Collections.Generic.List[object]'
$officialRootNorm = Normalize-PathText -Path $OfficialRoot
$forbiddenNorm = @($ForbiddenRoots | ForEach-Object { Normalize-PathText -Path $_ })
$logDir = Join-Path $OfficialRoot "01-mrp\logs\validation"
$logFile = Join-Path $logDir ("validate_environment_{0}.log" -f (Get-Date -Format "yyyyMMdd_HHmmss"))

try {
    Add-ValidationResult -Results $results -Check "official_root_exists" -Ok (Test-Path -LiteralPath $OfficialRoot -PathType Container) -Detail $OfficialRoot
    Add-ValidationResult -Results $results -Check "pcp_exists_but_forbidden" -Ok (Test-Path -LiteralPath $ForbiddenPcp -PathType Container) -Detail $ForbiddenPcp

    $share = $null
    try {
        $share = Get-SmbShare -Name $ShareName -ErrorAction Stop
        Add-ValidationResult -Results $results -Check "share_exists" -Ok $true -Detail $ShareName
    } catch {
        Add-ValidationResult -Results $results -Check "share_exists" -Ok $false -Detail $_.Exception.Message
    }

    if ($share) {
        $sharePathNorm = Normalize-PathText -Path ([string]$share.Path)
        Add-ValidationResult -Results $results -Check "share_points_to_official_root" -Ok ($sharePathNorm -eq $officialRootNorm) -Detail ([string]$share.Path)
        Add-ValidationResult -Results $results -Check "share_not_forbidden_target" -Ok (-not ($forbiddenNorm -contains $sharePathNorm)) -Detail ([string]$share.Path)
        Add-ValidationResult -Results $results -Check "share_not_direct_c_root" -Ok (-not (Test-DirectCRoot -Path $sharePathNorm)) -Detail ([string]$share.Path)
    }

    $mappedDriveExists = Test-Path -LiteralPath $MappedDrive -PathType Container
    Add-ValidationResult -Results $results -Check "mapped_drive_x_exists" -Ok $mappedDriveExists -Detail $MappedDrive

    if ($mappedDriveExists) {
        $testName = ".mrp_validate_environment_{0}.tmp" -f ([Guid]::NewGuid().ToString("N"))
        $testOnX = Join-Path $MappedDrive $testName
        $testOnOfficial = Join-Path $OfficialRoot $testName
        $testOnPcp = Join-Path $ForbiddenPcp $testName

        try {
            Write-Utf8NoBom -Path $testOnX -Text "MRP_LOCAL_VALIDATION_TEST"
            Add-ValidationResult -Results $results -Check "mapped_drive_write_test" -Ok (Test-Path -LiteralPath $testOnX -PathType Leaf) -Detail $testOnX
            Add-ValidationResult -Results $results -Check "test_file_visible_in_official_root" -Ok (Test-Path -LiteralPath $testOnOfficial -PathType Leaf) -Detail $testOnOfficial
            Add-ValidationResult -Results $results -Check "test_file_not_visible_in_pcp" -Ok (-not (Test-Path -LiteralPath $testOnPcp -PathType Leaf)) -Detail $testOnPcp
        } finally {
            if (Test-Path -LiteralPath $testOnX -PathType Leaf) {
                Remove-Item -LiteralPath $testOnX -Force
            }
            if (Test-Path -LiteralPath $testOnOfficial -PathType Leaf) {
                Remove-Item -LiteralPath $testOnOfficial -Force
            }
        }
    }

    foreach ($forbiddenRoot in $ForbiddenRoots) {
        Add-ValidationResult -Results $results -Check "forbidden_root_not_official" -Ok ((Normalize-PathText -Path $forbiddenRoot) -ne $officialRootNorm) -Detail $forbiddenRoot
    }

    Add-ValidationResult -Results $results -Check "official_root_not_direct_c_root" -Ok (-not (Test-DirectCRoot -Path $OfficialRoot)) -Detail $OfficialRoot

    $failed = @($results | Where-Object { -not $_.ok })
    $status = if ($failed.Count -eq 0) { "OK" } else { "FAIL" }
    $lines = New-Object 'System.Collections.Generic.List[string]'
    $lines.Add("timestamp=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')") | Out-Null
    $lines.Add("status=$status") | Out-Null
    foreach ($result in $results) {
        $prefix = if ($result.ok) { "OK" } else { "FAIL" }
        $lines.Add(("{0} | {1} | {2}" -f $prefix, $result.check, $result.detail)) | Out-Null
    }
    Write-Utf8NoBom -Path $logFile -Text (($lines -join "`n") + "`n")

    foreach ($line in $lines) {
        Write-Host $line
    }

    if ($failed.Count -gt 0) {
        exit 1
    }

    exit 0
} catch {
    Write-Utf8NoBom -Path $logFile -Text ("timestamp=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`nstatus=FAIL`nexception=$($_.Exception.Message)`n")
    Write-Error $_.Exception.Message
    exit 1
}
