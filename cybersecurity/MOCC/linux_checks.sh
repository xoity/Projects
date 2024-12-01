#!/bin/bash

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --minlen) minlen="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Load custom rules
custom_rules=$(cat custom_rules.json 2>/dev/null)
minlen=$(echo $custom_rules | jq -r '.password_policy.minlen // empty')

# Check password policy
password_policy=$(grep -E '^minlen' /etc/security/pwquality.conf || echo "minlen not set")
firewall_status=$(sudo ufw status | grep Status || echo "Firewall status unknown")
updates_status=$(systemctl is-enabled unattended-upgrades || echo "Unattended upgrades not enabled")

password_compliance="Non-compliant"
if [[ $password_policy == *"minlen"* ]]; then
    password_compliance="Compliant"
fi

firewall_compliance="Non-compliant"
if [[ $firewall_status == *"active"* ]]; then
    firewall_compliance="Compliant"
fi

updates_compliance="Non-compliant"
if [[ $updates_status == *"enabled"* ]]; then
    updates_compliance="Compliant"
fi

# Additional checks
open_ports=$(ss -tuln)
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