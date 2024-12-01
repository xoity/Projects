#!/bin/bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Create necessary directories
mkdir -p logs archives responses

# Download GeoIP database
LICENSE_KEY="YOUR_LICENSE_KEY"
wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=${LICENSE_KEY}&suffix=tar.gz" -O GeoLite2-City.tar.gz

# Extract the database
tar -xzf GeoLite2-City.tar.gz -C .

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