# Day 60 - Privacy-conscious local Windows Security log export.
# READ ONLY against Windows Security log. Writes a local pseudonymised JSONL file.
# Run in Windows PowerShell 5.1+ (ideally as Administrator) on a Windows PC you own.
# Do not publish output without reviewing it for sensitive timestamps and patterns.
[CmdletBinding()]
param(
    [ValidateRange(1, 168)] [int] $Hours = 24,
    [ValidateRange(1, 20000)] [int] $MaxEvents = 2000,
    [string] $OutputPath = (Join-Path $env:TEMP "day60_signins_anonymized.jsonl")
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# A fresh random salt each run preserves joins within one export but prevents
# easy cross-export linkage. The salt is intentionally NOT stored in the output.
$salt = [guid]::NewGuid().ToString('N')

function Get-Pseudonym {
    param([string] $Value, [string] $Prefix)
    if ([string]::IsNullOrWhiteSpace($Value) -or $Value -eq '-') {
        return '-'
    }
    $text = "$salt|$Prefix|$Value"
    $hashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
    try {
        $raw = [Text.Encoding]::UTF8.GetBytes($text)
        $digest = $hashAlgorithm.ComputeHash($raw)
        $hex = [BitConverter]::ToString($digest).Replace('-', '').ToLowerInvariant()
        return ('{0}_{1}' -f $Prefix, $hex.Substring(0, 16))
    }
    finally { $hashAlgorithm.Dispose() }
}

try {
    $filter = @{
        LogName = 'Security'
        Id = @(4624, 4625)
        StartTime = (Get-Date).AddHours(-$Hours)
    }
    # Get-WinEvent is a read-only query. Some systems need elevated permissions.
    $events = @(Get-WinEvent -FilterHashtable $filter -MaxEvents $MaxEvents -ErrorAction Stop)
}
catch {
    throw "Cannot read Windows Security log (no events, unavailable auditing, or access denied): $($_.Exception.Message)"
}

$directory = [IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($OutputPath))
[void][IO.Directory]::CreateDirectory($directory)
$writer = New-Object IO.StreamWriter(
    [IO.Path]::GetFullPath($OutputPath), $false, (New-Object Text.UTF8Encoding($false))
)
$written = 0
$skipped = 0
try {
    foreach ($event in $events) {
        try {
            [xml] $doc = $event.ToXml()
            $data = @{}
            foreach ($field in @($doc.Event.EventData.Data)) {
                if ($null -ne $field -and $field.GetAttribute('Name')) {
                    $data[[string]$field.GetAttribute('Name')] = [string]$field.InnerText
                }
            }
            if (-not $data.ContainsKey('LogonType') -or
                -not $data.ContainsKey('TargetUserName') -or
                -not $data['TargetUserName'] -or
                $data['TargetUserName'] -eq '-') {
                $skipped++
                continue
            }
            $logonType = [int]$data['LogonType']
            $src = [string]$data['IpAddress']
            if ([string]::IsNullOrWhiteSpace($src) -or $src -eq '-') {
                $src = '-'
            }
            else {
                $parsedAddress = [System.Net.IPAddress]::None
                if (-not [System.Net.IPAddress]::TryParse($src, [ref]$parsedAddress) -or
                    [System.Net.IPAddress]::IsLoopback($parsedAddress)) {
                    $src = '-'
                }
            }
            $domain = [string]$data['TargetDomainName']
            $userComposite = "$domain\$($data['TargetUserName'])"
            $row = [ordered]@{
                TimeCreated = $event.TimeCreated.ToUniversalTime().ToString(
                    'yyyy-MM-ddTHH:mm:ss.fffZ',
                    [Globalization.CultureInfo]::InvariantCulture
                )
                EventID = [int]$event.Id
                TargetUserName = Get-Pseudonym -Value $userComposite -Prefix 'acct'
                IpAddress = Get-Pseudonym -Value $src -Prefix 'ip'
                LogonType = $logonType
                Computer = Get-Pseudonym -Value ([string]$event.MachineName) -Prefix 'host'
            }
            $writer.WriteLine(($row | ConvertTo-Json -Compress -Depth 3))
            $written++
        }
        catch {
            $skipped++
            # Do not print raw event content or personal identifiers on error.
            Write-Warning ("Skipped an event because it could not be parsed: " + $_.Exception.GetType().Name)
        }
    }
}
finally { $writer.Dispose() }
Write-Output ("Exported {0} pseudonymised records to {1} (skipped {2}; maximum fetched {3})." -f
    $written, [IO.Path]::GetFullPath($OutputPath), $skipped, $MaxEvents)
Write-Output "This file remains local. It contains real timestamps/patterns; review before sharing."
