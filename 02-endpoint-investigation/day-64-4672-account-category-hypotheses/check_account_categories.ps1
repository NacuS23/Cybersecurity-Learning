# Day 64: read-only Windows Security Event 4672 account-category review.
# Prints aggregate categories and privilege presence only; no account names/SIDs.
# Requires Windows PowerShell and permission to read the Security log.
# NOT run against the user's PC by the assistant.
[CmdletBinding()]
param(
    [ValidateRange(1,168)][int] $Hours = 24,
    [ValidateRange(1,2000)][int] $MaxEvents = 2000
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
    Write-Warning 'No matching Security Event 4672 records could be read. Confirm access and audit configuration; this is not a security verdict.'
    return
}

$records = @(
    foreach ($event in $events) {
        [xml] $doc = $event.ToXml()
        $fields = @{}
        foreach ($node in @($doc.Event.EventData.Data)) {
            if ($null -eq $node) { continue }
            $fieldName = [string] $node.GetAttribute('Name')
            if ($fieldName) { $fields[$fieldName] = [string] $node.InnerText }
        }
        $sid = if ($fields.ContainsKey('SubjectUserSid')) { [string]$fields['SubjectUserSid'] } else { '' }
        $category = switch ($sid) {
            'S-1-5-18' { 'SYSTEM'; break }
            'S-1-5-19' { 'LOCAL SERVICE'; break }
            'S-1-5-20' { 'NETWORK SERVICE'; break }
            ''         { 'MISSING SID'; break }
            default    { 'OTHER / UNCLASSIFIED'; break }
        }
        $privilegeList = if ($fields.ContainsKey('PrivilegeList')) { [string]$fields['PrivilegeList'] } else { '' }
        $names = @($privilegeList -split '\s+' | Where-Object { $_ })
        [PSCustomObject]@{
            Category = $category
            HasDebug = ($names -contains 'SeDebugPrivilege')
            HasTcb   = ($names -contains 'SeTcbPrivilege')
        }
    }
)

"4672 records in this query: $($records.Count)"
$records |
    Group-Object Category |
    Sort-Object Name |
    ForEach-Object {
        $group = @($_.Group)
        [PSCustomObject]@{
            Category = $_.Name
            Events = $_.Count
            WithDebugPrivilege = @($group | Where-Object { $_.HasDebug }).Count
            WithTcbPrivilege = @($group | Where-Object { $_.HasTcb }).Count
        }
    } | Format-Table -AutoSize
Write-Output 'Other/unclassified is NOT proof of malicious activity. No raw account identifiers were printed.'
