# HoneyBee Honeypot Project

## Overview

HoneyBee is a comprehensive honeypot system designed to detect, log, and analyze malicious activities targeting various network services. It includes features for logging, alerting, automated actions, machine learning-based anomaly detection, and visualization of attack data.

## Features

- **Deployment Script**: Automates the setup of the honeypot environment.
- **Logging and Alerting**: Monitors and logs connection attempts, and sends alerts based on predefined thresholds.
- **Machine Learning Analyzer**: Uses an Isolation Forest model to detect anomalies in the attack patterns.
- **Automated Actions**: Blocks IP addresses that exceed a certain number of failed login attempts.
- **Visualization**: Provides graphical representations of attack data.
- **Dashboard**: A web-based interface for monitoring and managing the honeypot system.

## Components

### 1. Deployment Script (`deployment.sh`)

This script sets up the honeypot environment, including downloading necessary databases, setting up log rotation, and starting the honeypot services.

### 2. Logging and Alerting (`logging_and_alerting.py`)

Monitors the honeypot logs for failed login attempts and sends email alerts when the number of attempts from a single IP exceeds a threshold.

### 3. Machine Learning Analyzer (`ml_analyzer.py`)

Trains an Isolation Forest model on the log data to detect anomalies in the attack patterns.

### 4. Honeypot Core (`honeypot_core.py`)

Handles incoming connections to the honeypot, logs interactions, and provides fake responses to keep attackers engaged.

### 5. Automated Actions (`automated_actions.py`)

Analyzes the logs and blocks IP addresses that exceed a certain number of failed login attempts using iptables.

### 6. Visualization (`visualization.py`)

Generates visual representations of the attack data, such as the frequency of attacks by hour.

### 7. Configuration (`config.py`)

Contains configuration settings for the honeypot system, including secret keys, log directories, alert settings, and service ports.

### 8. Dashboard (`dashboard.py`)

A Flask-based web application that provides a user interface for monitoring and managing the honeypot system. It includes user authentication, attack data visualization, and API endpoints for retrieving attack logs.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/HoneyBee.git
    cd HoneyBee
    ```

2. Set up the environment:
    ```bash
    chmod +x deployment.sh
    sudo ./deployment.sh
    ```

3. Configure environment variables:
    ```bash
    export SECRET_KEY='your-secret-key'
    export ADMIN_USERNAME='admin'
    export ADMIN_PASSWORD='password'
    export SLACK_TOKEN='your-slack-token'
    export TELEGRAM_TOKEN='your-telegram-token'
    ```

4. Start the dashboard:
    ```bash
    python3 dashboard.py
    ```

## Usage

- Access the dashboard at `http://localhost:5000` and log in with the admin credentials.
- Monitor the attack data and visualize it using the provided graphs.
- Configure alert settings and automated actions as needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [MaxMind GeoIP2](https://www.maxmind.com/en/geoip2-services-and-databases)
- [Scikit-learn](https://scikit-learn.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Plotly](https://plotly.com/)

## Note

this project is still a work under progress