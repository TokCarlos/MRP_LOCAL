$ErrorActionPreference = "Continue"

Write-Host "ZERANDO EXECUCAO DO MRP_LOCAL"
Write-Host "Porta alvo: 8765"

try {
    Get-ScheduledTask | Where-Object {
        $_.TaskName -match 'MRP|mrp|FRONTEND|WATCHDOG' -or
        $_.TaskPath -match 'MRP|mrp' -or
        ($_.Actions | Out-String) -match 'MRP|mrp|system_jpl|09_Sistema|01-mrp|03-vs|8765|mrp_frontend'
    } | ForEach-Object {
        Write-Host "Parando/desabilitando tarefa: $($_.TaskPath)$($_.TaskName)"
        Stop-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath -ErrorAction SilentlyContinue
        Disable-ScheduledTask -TaskName $_.TaskName -TaskPath $_.TaskPath -ErrorAction SilentlyContinue
    }
} catch {
    Write-Host "Aviso: falha ao consultar/parar tarefas: $($_.Exception.Message)"
}

try {
    Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue | ForEach-Object {
        $listenerProcessId = [int]$_.OwningProcess
        if ($listenerProcessId -gt 0) {
            Write-Host "Matando processo na porta 8765. PID=$listenerProcessId"
            Stop-Process -Id $listenerProcessId -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    netstat -ano | Select-String ":8765" | Select-String "LISTENING" | ForEach-Object {
        $parts = ($_.ToString() -split "\s+") | Where-Object { $_ -ne "" }
        if ($parts.Count -ge 5) {
            $listenerProcessId = [int]$parts[-1]
            Write-Host "Matando processo na porta 8765. PID=$listenerProcessId"
            Stop-Process -Id $listenerProcessId -Force -ErrorAction SilentlyContinue
        }
    }
}

$currentProcessId = [System.Diagnostics.Process]::GetCurrentProcess().Id

try {
    Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -ne $currentProcessId -and
        $_.CommandLine -and
        $_.CommandLine -match 'MRP|mrp|system_jpl|09_Sistema|01-mrp|03-vs|http.server|8765|mrp_frontend|watchdog'
    } | ForEach-Object {
        Write-Host "Matando processo relacionado. PID=$($_.ProcessId) Nome=$($_.Name)"
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }
} catch {
    Write-Host "Aviso: falha ao consultar processos relacionados: $($_.Exception.Message)"
}

Start-Sleep -Seconds 1

Write-Host ""
Write-Host "Estado final da porta 8765:"
netstat -ano | findstr :8765

Write-Host ""
Write-Host "Se nao aparecer LISTENING, esta zerado."
exit 0
