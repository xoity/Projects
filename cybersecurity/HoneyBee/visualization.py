import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

LOG_FILE = "SSH_honeypot.log"

def load_logs():
    with open(LOG_FILE, 'r') as log:
        return [json.loads(line) for line in log]

def plot_attack_frequency(logs):
    timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in logs]
    hours = [ts.hour for ts in timestamps]
    counter = Counter(hours)
    plt.bar(counter.keys(), counter.values())
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Attacks')
    plt.title('Attack Frequency by Hour')
    plt.show()

def main():
    print("Loading logs and generating visualization...")
    logs = load_logs()
    plot_attack_frequency(logs)
    print("Visualization complete.")

if __name__ == "__main__":
    main()