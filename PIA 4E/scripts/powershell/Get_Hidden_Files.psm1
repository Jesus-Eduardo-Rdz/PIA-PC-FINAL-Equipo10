Set-StrictMode -Version Latest

<# 
.SYNOPSIS
   List all hidden files in a specified directory and save report.
.DESCRIPTION
   Lists all hidden files in the specified directory and outputs results to a CSV report.
.PARAMETER FolderPath
   Directory path to check for hidden files.
.EXAMPLE
   Get-HiddenFiles -FolderPath 'C:\Users\User\Documents'
.NOTES
   This function is part of the Get_Hidden_Files module.
#>

function Get-HiddenFiles {
    param (
        [Parameter(Mandatory=$true)]
        [string]$FolderPath
    )

    # Output report path
    $reportPath = Join-Path -Path $FolderPath -ChildPath 'HiddenFilesReport.csv'
    $hiddenFiles = Get-ChildItem -Path $FolderPath -Force | Where-Object { $_.Attributes -match 'Hidden' }
    $hiddenFiles | Select-Object FullName, CreationTime, LastAccessTime | Export-Csv -Path $reportPath -NoTypeInformation

    # Log to console
    $hash = [System.BitConverter]::ToString((Get-FileHash -Path $reportPath -Algorithm SHA256).Hash).Replace("-", "")
    Write-Host "Se ejecutó 'Get-HiddenFiles' el $(Get-Date)"
    Write-Host "Hash del reporte: $hash"
    Write-Host "Ubicación del reporte: $reportPath"
}
