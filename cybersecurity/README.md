# Projects Repository

## Overview

The **Projects Repository** is a comprehensive collection of cybersecurity tools and frameworks designed to enhance security, compliance, and monitoring capabilities. This repository includes tools tailored for multi-operating system compliance checks and honeypot deployments, making it a valuable resource for researchers, developers, and security professionals. 

## Included Projects

### 1. **Multi-OS Compliance Checker (MOCC)**
A versatile tool to evaluate security compliance across Linux, macOS, and Windows operating systems.

#### Features:
- Automatic OS detection.
- Customizable compliance rules.
- Generates reports in JSON, HTML, or CSV formats.
- Supports detailed logging for debugging and audits.

#### Usage:
1. Define custom rules in `custom_rules.json`:
   ```json
   {
       "password_policy": {
           "minlen": 12,
           "minChars": 12,
           "minPasswordLength": 12
       }
   }
   ```

2. Run compliance checks:
   ```sh
   python main.py --os linux --rules custom_rules.json --format json --verbose
   ```

#### Key Components:
- **Custom Rule Loader**: Accepts user-defined rules in JSON format.
- **Multi-OS Scripts**: Bash for Linux/macOS and PowerShell for Windows.
- **Report Generator**: Outputs compliance results in the chosen format.

### 2. **HoneyBee Honeypot Project**
A honeypot system designed to detect, log, and analyze malicious activities targeting network services.

#### Features:
- Automated deployment with a single script.
- Logging and alerting for suspicious activities.
- Machine learning-based anomaly detection using Isolation Forest.
- Web dashboard for attack visualization and management.
- Automated IP blocking using iptables.

#### Usage:
1. Deploy the honeypot:
   ```bash
   chmod +x deployment.sh
   sudo ./deployment.sh
   ```

2. Configure environment variables:
   ```bash
   export SECRET_KEY='your-secret-key'
   export ADMIN_USERNAME='admin'
   export ADMIN_PASSWORD='password'
   ```

3. Start the dashboard:
   ```bash
   python3 dashboard.py
   ```

4. Access the dashboard at `http://localhost:5000` for real-time monitoring.

#### Key Components:
- **Honeypot Core**: Engages attackers and logs their actions.
- **Machine Learning Analyzer**: Identifies anomalies in attack patterns.
- **Visualization Module**: Graphically represents attack data.
- **Automated Defense**: Blocks malicious IPs based on predefined thresholds.

---

## Prerequisites
- **General Requirements**:
  - Python 3.x
  - jq (for JSON parsing in shell scripts)
  - Bash (for Linux/macOS)
  - PowerShell (for Windows)
  
- **MOCC Specific**:
  - `pandas` for report generation.

- **HoneyBee Specific**:
  - Flask for dashboard functionality.
  - Scikit-learn for machine learning analysis.

## Contribution
Contributions to the repository are welcome. Follow these steps to contribute:
1. Fork the repository.
2. Implement changes or add features.
3. Submit a pull request with a detailed explanation of your changes.

## License
The projects in this repository are licensed under the **MIT License**. See individual project directories for more details.

## Notes
- Both projects are under active development. Expect bugs and incomplete features.
- Use the tools responsibly and only in environments where you have proper authorization.