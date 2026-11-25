# Day 62: Read-only 4624/4672 correlation; PRIVACY: outputs aggregates only.
# Run from Windows PowerShell with sufficient permission to read the Security log.
# Never paste raw event XML, usernames, SIDs, or logon identifiers into a public issue.
[CmdletBinding()]
param(
    [ValidateRange(1,168)][int]$Hours = 24,
    [ValidateRange(1,10000)][int]$MaxEvents = 2000,
    [ValidateRange(1,300)][int]$MaxSecondsApart = 60
)

$ErrorActionPreference = 'Stop'
try {
    $events = @(Get-WinEvent -FilterHashtable @{
        LogName = 'Security'
        Id = @(4624,4672)
        StartTime = (Get-Date).AddHours(-$Hours)
    } -MaxEvents $MaxEvents -ErrorAction Stop)
}
catch {
    Write-Error "Failed to read Security log. Check local permissions and audit availability."
    return
}

$parsed = @(
    foreach ($ev in $events) {
        [xml]$xml = $ev.ToXml()
        $fields = @{}
        foreach ($node in @($xml.Event.EventData.Data)) {
            if ($null -ne $node) {
                $name = [string]$node.GetAttribute('Name')
                if ($name) { $fields[$name] = [string]$node.InnerText }
            }
        }
        $key = if ($ev.Id -eq 4624) {'TargetLogonId'} else {'SubjectLogonId'}
        if ($fields.ContainsKey($key) -and $fields[$key]) {
            [PSCustomObject]@{
                EventId = [int]$ev.Id
                TimeCreated = $ev.TimeCreated
                Host = [string]$ev.MachineName
                LogonId = [string]$fields[$key]
                LogonType = [string]$fields['LogonType']
            }
        }
    }
)

$success = @($parsed | Where-Object { $_.EventId -eq 4624 })
$privileged = @($parsed | Where-Object { $_.EventId -eq 4672 })

$matched = @(
    foreach ($item in $privileged) {
        $corresponding = $success |
            Where-Object {
                $_.Host -eq $item.Host -and
                $_.LogonId -eq $item.LogonId -and
                [Math]::Abs(($_.TimeCreated - $item.TimeCreated).TotalSeconds) -le $MaxSecondsApart
            } |
            Sort-Object {
                [Math]::Abs(($_.TimeCreated - $item.TimeCreated).TotalSeconds)
            } |
            Select-Object -First 1
        if ($corresponding) {
            [PSCustomObject]@{ LogonType = $corresponding.LogonType }
        }
    }
)

"4624 events parsed: $($success.Count)"
"4672 events parsed: $($privileged.Count)"
"Nearby 4672-to-4624 event matches: $($matched.Count)"
"Not matched (in this bounded query): $($privileged.Count - $matched.Count)"
$matched | Group-Object LogonType | Sort-Object Name | Select-Object Name, Count
Write-Output "Note: matches count EVENTS, not necessarily distinct sessions."
