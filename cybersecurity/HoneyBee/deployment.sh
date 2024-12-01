#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Install necessary packages
apt-get update
apt-get install -y python3 python3-pip iptables

# Install Python dependencies
pip3 install matplotlib

# Create necessary directories
mkdir -p logs archives responses

# Download GeoIP database
wget https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City -O GeoLite2-City.mmdb

# Install additional dependencies
pip3 install -r requirements.txt

# Set up log rotation
cat > /etc/logrotate.d/honeypot << EOF
/var/log/honeypot/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF

# Start services
python3 dashboard.py &
python3 honeypot_core.py &

echo "Honeypot system deployed successfully!"