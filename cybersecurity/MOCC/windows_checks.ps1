param (
    [int]$minPasswordLength,
    [string]$customRulesPath = "custom_rules.json"
)

# Load custom rules if not provided as arguments
if (-not $minPasswordLength) {
    $customRules = Get-Content -Raw -Path $customRulesPath | ConvertFrom-Json
    $minPasswordLength = $customRules.password_policy.minPasswordLength
}

# Check password policy
$passwordPolicy = Get-ADDefaultDomainPasswordPolicy | Select-Object -Property MinPasswordLength
$firewallStatus = Get-NetFirewallProfile -Profile Domain,Public,Private | Select-Object -Property Enabled
$updatesStatus = Get-WindowsUpdateLog

$results = @(
    @{
        "check" = "Password Policy"
        "status" = if ($passwordPolicy.MinPasswordLength -ge $minPasswordLength) { "Compliant" } else { "Non-compliant" }
        "details" = "Minimum length set to $($passwordPolicy.MinPasswordLength) characters."
    },
    @{
        "check" = "Firewall Status"
        "status" = if ($firewallStatus.Enabled -contains $false) { "Non-compliant" } else { "Compliant" }
        "details" = "Firewall is $($firewallStatus.Enabled)."
    },
    @{
        "check" = "Automatic Updates"
        "status" = if ($updatesStatus -match "Windows Update is enabled") { "Compliant" } else { "Non-compliant" }
        "details" = "Windows Update is enabled."
    }
)

# Additional checks
$rdpStatus = Get-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name 'fDenyTSConnections'
$antivirusStatus = Get-MpComputerStatus | Select-Object -Property AMRunningStatus

$results += @(
    @{
        "check" = "RDP Status"
        "status" = if ($rdpStatus.fDenyTSConnections -eq 1) { "Compliant" } else { "Non-compliant" }
        "details" = "RDP is $($rdpStatus.fDenyTSConnections)"
    },
    @{
        "check" = "Antivirus Status"
        "status" = if ($antivirusStatus.AMRunningStatus -eq 1) { "Compliant" } else { "Non-compliant" }
        "details" = "Antivirus is $($antivirusStatus.AMRunningStatus)"
    }
)

$results | ConvertTo-Json