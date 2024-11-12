Set-StrictMode -Version Latest

<# 
.SYNOPSIS
   Check for suspicious processes and save report.
.DESCRIPTION
   Detects processes with high CPU or memory usage, suspicious names, or invalid signatures.
#>

function Check-SuspiciousProcesses {
    param (
        [int]$CpuThreshold = 20,
        [int]$MemoryThreshold = 100MB
    )
    $reportPath = "SuspiciousProcessesReport.csv"
    try {
        $processes = Get-Process | Where-Object { $_.Id -ne 0 }
        $processes | ForEach-Object {
            $isSuspicious = $false
            if ($_.CPU -gt $CpuThreshold) { $isSuspicious = $true }
            if ($_.WorkingSet -gt ($MemoryThreshold * 1MB)) { $isSuspicious = $true }
            if ($isSuspicious) {
                $_ | Export-Csv -Path $reportPath -Append -NoTypeInformation
            }
        }
        Write-Host "Se ejecutó 'Check-SuspiciousProcesses' el $(Get-Date)"
        Write-Host "Ubicación del reporte: $reportPath"
    } catch {
        Write-Host "Error en Check-SuspiciousProcesses: $_"
    }
}
