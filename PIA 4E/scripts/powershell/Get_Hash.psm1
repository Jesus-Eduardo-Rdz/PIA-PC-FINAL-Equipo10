Set-StrictMode -Version Latest

<# 
.SYNOPSIS
   Generate hash for a file and check VirusTotal report.
.DESCRIPTION
   Calculates the file hash and checks VirusTotal for any threat detection.
#>

function Get-FileHashAndVirusTotal {
    param (
        [string]$FilePath,
        [string]$ApiKey,
        [ValidateSet('MD5', 'SHA1', 'SHA256')]
        [string]$HashAlgorithm = 'SHA256'
    )
    $reportPath = "FileHashReport.csv"
    try {
        $fileHash = Get-FileHash -Path $FilePath -Algorithm $HashAlgorithm
        $fileHash.Hash | Export-Csv -Path $reportPath -NoTypeInformation
        Write-Host "Se ejecutó 'Get-FileHashAndVirusTotal' el $(Get-Date)"
        Write-Host "Ubicación del reporte: $reportPath"
    } catch {
        Write-Host "Error en Get-FileHashAndVirusTotal: $_"
    }
}
