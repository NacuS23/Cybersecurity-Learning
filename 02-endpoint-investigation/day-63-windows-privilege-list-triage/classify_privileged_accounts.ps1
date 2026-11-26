# Day 63 optional follow-up: PRIVACY-PRESERVING category counts only
# Read-only Windows Security log query. Does NOT export events or identifiers.
# User-run on Windows only; no execution of this script has been claimed yet.
[CmdletBinding()]
param(
    [ValidateRange(1,168)][int]$Hours = 24,
    [ValidateRange(1,2000)][int]$MaxEvents = 2000
)

$ErrorActionPreference = 'Stop'
try {
    $events = @(Get-WinEvent -FilterHashtable @{
        LogName = 'Security'
        Id = 4672
        StartTime = (Get-Date).AddHours(-$Hours)
    } -MaxEvents $MaxEvents -ErrorAction Stop)
}
catch {
    Write-Error 'Could not query Security Event 4672. Check privileges and audit settings.'
    return
}

$categories = @(
    foreach ($event in $events) {
        [xml]$xml = $event.ToXml()
        $field = @($xml.Event.EventData.Data) |
            Where-Object { $_.GetAttribute('Name') -eq 'SubjectUserSid' } |
            Select-Object -First 1
        $sid = if ($field) { [string]$field.InnerText } else { '' }

        # Classify fixed, well-known Windows SIDs. Do not print raw SIDs.
        switch ($sid) {
            'S-1-5-18' { 'SYSTEM'; break }
            'S-1-5-19' { 'LOCAL SERVICE'; break }
            'S-1-5-20' { 'NETWORK SERVICE'; break }
            ''         { 'Missing SID'; break }
            default    { 'Other/Unclassified account'; break }
        }
    }
)

"4672 events in current query: $($events.Count)"
$categories |
    Group-Object |
    Sort-Object Name |
    Select-Object Name, Count

Write-Output 'Category counts only. This is not evidence of privilege use or compromise.'
