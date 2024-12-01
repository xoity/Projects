import json
import subprocess

LOG_FILE = "SSH_honeypot.log"
BLOCK_THRESHOLD = 10

def block_ip(ip):
    subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])

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
                if ip_attempts[ip] >= BLOCK_THRESHOLD:
                    block_ip(ip)

def main():
    print("Analyzing logs for automated actions...")
    analyze_logs()
    print("Analysis complete. Malicious IPs have been blocked.")

if __name__ == "__main__":
    main()