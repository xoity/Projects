#!/bin/bash

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --minChars) minChars="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Load custom rules
custom_rules=$(cat custom_rules.json 2>/dev/null)
minChars=$(echo $custom_rules | jq -r '.password_policy.minChars // empty')

# Check password policy
password_policy=$(pwpolicy getaccountpolicies | grep -E 'minChars' || echo "minChars not set")
firewall_status=$(sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate || echo "Firewall status unknown")
updates_status=$(sudo softwareupdate --schedule || echo "Automatic updates not enabled")

password_compliance="Non-compliant"
if [[ $password_policy == *"minChars"* ]]; then
    password_compliance="Compliant"
fi

firewall_compliance="Non-compliant"
if [[ $firewall_status == *"enabled"* ]]; then
    firewall_compliance="Compliant"
fi

updates_compliance="Non-compliant"
if [[ $updates_status == *"on"* ]]; then
    updates_compliance="Compliant"
fi

# Additional checks
open_ports=$(netstat -an | grep LISTEN)
selinux_status=$(sestatus 2>/dev/null || echo "SELinux status unknown")

results=$(cat <<EOF
[
    {
        "check": "Password Policy",
        "status": "$password_compliance",
        "details": "$password_policy"
    },
    {
        "check": "Firewall Status",
        "status": "$firewall_compliance",
        "details": "$firewall_status"
    },
    {
        "check": "Automatic Updates",
        "status": "$updates_compliance",
        "details": "$updates_status"
    },
    {
        "check": "Open Ports",
        "status": "Info",
        "details": "$open_ports"
    },
    {
        "check": "SELinux Status",
        "status": "$selinux_status",
        "details": "$selinux_status"
    }
]
EOF
)

echo $results