Set-StrictMode -Version Latest

<# 
.SYNOPSIS
   Perform a complete system usage check and save report.
.DESCRIPTION
   Generates a report of CPU, Memory, Disk, and Network usage.
#>

function Cpu-Usage {
    $reportPath = "CpuUsageReport.csv"
    try {
        $cpuLoad = Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average | Select-Object -ExpandProperty Average
        $cpuLoad | Export-Csv -Path $reportPath -NoTypeInformation
        Write-Host "Se ejecutó 'Cpu-Usage' el $(Get-Date)"
        Write-Host "Ubicación del reporte: $reportPath"
    } catch {
        Write-Host "Error en Cpu-Usage: $_"
    }
}

function Memory-Usage {
    $reportPath = "MemoryUsageReport.csv"
    try {
        $mem = Get-WmiObject Win32_OperatingSystem
        $memUsage = (($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize) * 100
        $memUsage | Export-Csv -Path $reportPath -NoTypeInformation
        Write-Host "Se ejecutó 'Memory-Usage' el $(Get-Date)"
        Write-Host "Ubicación del reporte: $reportPath"
    } catch {
        Write-Host "Error en Memory-Usage: $_"
    }
}

function Disk-Usage {
    $reportPath = "DiskUsageReport.csv"
    try {
        $disk = Get-WmiObject Win32_LogicalDisk -Filter "DriveType=3"
        $disk | ForEach-Object {
            $diskUsage = (($_.Size - $_.FreeSpace) / $_.Size) * 100
            $_.DeviceID, $diskUsage | Export-Csv -Path $reportPath -Append -NoTypeInformation
        }
        Write-Host "Se ejecutó 'Disk-Usage' el $(Get-Date)"
        Write-Host "Ubicación del reporte: $reportPath"
    } catch {
        Write-Host "Error en Disk-Usage: $_"
    }
}

function Net-Usage {
    $reportPath = "NetUsageReport.csv"
    try {
        $networkAdapters = Get-NetAdapterStatistics
        $networkAdapters | Export-Csv -Path $reportPath -NoTypeInformation
        Write-Host "Se ejecutó 'Net-Usage' el $(Get-Date)"
        Write-Host "Ubicación del reporte: $reportPath"
    } catch {
        Write-Host "Error en Net-Usage: $_"
    }
}
