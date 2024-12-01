import json
import smtplib
from email.mime.text import MIMEText

ALERT_THRESHOLD = 5
LOG_FILE = "SSH_honeypot.log"
ALERT_EMAIL = "admin@example.com"

def send_alert(ip, count):
    msg = MIMEText(f"Alert: {count} failed login attempts from {ip}")
    msg['Subject'] = "Honeypot Alert"
    msg['From'] = "honeypot@example.com"
    msg['To'] = ALERT_EMAIL

    with smtplib.SMTP('localhost') as server:
        server.sendmail("honeypot@example.com", [ALERT_EMAIL], msg.as_string())

def analyze_logs():
    ip_attempts = {}
    with open(LOG_FILE, 'r') as log:
        for line in log:
            entry = json.loads(line)
            ip = entry['ip']
            if entry['action'] == "Connection attempt":
                if ip not in ip_attempts:
                    ip_attempts[ip] = 0
                ip_attempts[ip] += 1
                if ip_attempts[ip] >= ALERT_THRESHOLD:
                    send_alert(ip, ip_attempts[ip])

def main():
    print("Analyzing logs for alerts...")
    analyze_logs()
    print("Analysis complete.")

if __name__ == "__main__":
    main()