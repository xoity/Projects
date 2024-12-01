import os
import subprocess
import json
import argparse
import pandas as pd
import csv

def detect_os():
    platforms = {
        'linux': 'Linux',
        'darwin': 'macOS',
        'win32': 'Windows'
    }
    return platforms.get(os.sys.platform, 'Unknown')

def run_checks(os_type, custom_rules):
    if os_type == 'Linux' or os_type == 'macOS':
        script = 'linux_checks.sh' if os_type == 'Linux' else 'macos_checks.sh'
        result = subprocess.run(['bash', script, '--minlen', str(custom_rules['password_policy']['minlen'])], capture_output=True, text=True)
    elif os_type == 'Windows':
        script = 'windows_checks.ps1'
        result = subprocess.run(['powershell', '-File', script, '-minPasswordLength', str(custom_rules['password_policy']['minPasswordLength'])], capture_output=True, text=True)
    else:
        return None

    if result.returncode != 0:
        print(f"Error running script: {result.stderr}")
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Script output: {result.stdout}")
        return None

def generate_report(results, format='json'):
    report = {
        "os": detect_os(),
        "checks": results
    }
    if format == 'json':
        with open('report.json', 'w') as f:
            json.dump(report, f, indent=4)
        print("Report generated: report.json")
    elif format == 'html':
        df = pd.DataFrame(report['checks'])
        df.to_html('report.html')
        print("Report generated: report.html")
    elif format == 'csv':
        with open('report.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["check", "status", "details"])
            writer.writeheader()
            writer.writerows(report['checks'])
        print("Report generated: report.csv")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Multi-OS Compliance Checker")
    parser.add_argument("--os", choices=["linux", "macos", "windows", "all"], help="Target OS")
    parser.add_argument("--rules", default="custom_rules.json", help="Path to custom rules file")
    parser.add_argument("--format", choices=["json", "html", "csv"], default="json", help="Report format")
    parser.add_argument("--verbose", action='store_true', help="Enable verbose output")
    return parser.parse_args()

def main():
    args = parse_arguments()
    custom_rules = {}
    with open(args.rules, 'r') as f:
        custom_rules = json.load(f)

    os_type = args.os if args.os else detect_os()
    if args.verbose:
        print(f"Detected OS: {os_type}")

    results = []
    if os_type in ['Linux', 'macos', 'Windows']:
        results = run_checks(os_type, custom_rules)
    elif os_type == 'all':
        for os_type in ['Linux', 'macos', 'Windows']:
            os_results = run_checks(os_type, custom_rules)
            if os_results:
                results.extend(os_results)

    if results:
        generate_report(results, args.format)

if __name__ == "__main__":
    main()