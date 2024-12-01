# Multi-OS Compliance Checker (MOCC)

## Overview
The Multi-OS Compliance Checker (MOCC) is a tool designed to perform security compliance checks across multiple operating systems including Linux, macOS, and Windows. It runs a series of checks based on custom rules and generates a report in various formats (JSON, HTML, CSV).

## Features
- Detects the operating system automatically.
- Runs compliance checks based on custom rules.
- Generates reports in JSON, HTML, or CSV format.
- Supports verbose output for detailed logging.

## Prerequisites
- Python 3.x
- Bash (for Linux and macOS)
- PowerShell (for Windows)
- jq (for JSON parsing in shell scripts)
- pandas (for HTML report generation)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/xoity/Projects.git
    cd cybersecurity/MOCC
    ```

2. Install required Python packages:
    ```sh
    pip install pandas
    ```

## Usage
1. Create or modify the `custom_rules.json` file to define your custom rules:
    ```json
    {
        "password_policy": {
            "minlen": 12,
            "minChars": 12,
            "minPasswordLength": 12
        }
    }
    ```

2. Run the program:
    ```sh
    python main.py --os <target_os> --rules <path_to_custom_rules> --format <report_format> [--verbose]
    ```

    - `<target_os>`: Specify the target OS (`linux`, `macos`, `windows`, or `all`).
    - `<path_to_custom_rules>`: Path to the custom rules JSON file.
    - `<report_format>`: Format of the report (`json`, `html`, `csv`).
    - `--verbose`: Enable verbose output (optional).

    Example:
    ```sh
    python main.py --os linux --rules custom_rules.json --format json --verbose
    ```

## Running Tests
To run the unit tests, use the following command:
```sh
python -m unittest discover
```

## License
This project is licensed under the MIT License.

## Note

THIS PROJECT IS STILLL UNDER DEVELOPMENT, DO NOT EXPECT ANYTHING TO WORK AS EXPECTED
