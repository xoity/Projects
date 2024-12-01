import socket
import json
import geoip2.database
from datetime import datetime
from cryptography.fernet import Fernet
from config import Config

class HoneypotService:
    def __init__(self, service_name):
        self.service_name = service_name
        self.log_file = f"{service_name}_honeypot.log"
        self.responses = self.load_fake_responses()
        self.geo_reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        self.cipher_suite = Fernet(Fernet.generate_key())

    def get_location_data(self, ip):
        try:
            response = self.geo_reader.city(ip)
            return {
                'country': response.country.name,
                'city': response.city.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude
            }
        except geoip2.errors.AddressNotFoundError:
            return None

    def log_interaction(self, ip, port, action, payload=None):
        location_data = self.get_location_data(ip)
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "ip": ip,
            "port": port,
            "action": action,
            "payload": payload,
            'location': location_data,
            'service': self.service_name
        }
        encrypted_entry = self.cipher_suite.encrypt(json.dumps(log_entry).encode())
        with open(self.log_file, 'a') as log:
            log.write(encrypted_entry.decode() + "\n")

    def handle_connection(self, conn, addr):
        if addr[0] in Config.IP_WHITELIST:
            return
        ip, port = addr
        print(f"Connection from {ip}:{port}")
        self.log_interaction(ip, port, "Connection attempt")
        # Fake response to keep attacker engaged
        conn.sendall(b"Welcome to the fake service!\n")

    def load_fake_responses(self):
        with open(f'responses/{self.service_name.lower()}_responses.json') as f:
            return json.load(f)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', self.port))
            s.listen()
            print(f"{self.service_name} honeypot listening on port {self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    self.handle_connection(conn, addr)

def main():
    print("Select the service to simulate:")
    print("1. SSH")
    print("2. HTTP")
    choice = input("Enter your choice (1/2): ")
    if choice == '1':
        honeypot = HoneypotService("SSH")
    elif choice == '2':
        honeypot = HoneypotService("HTTP")
    else:
        print("Invalid choice")
        return
    honeypot.start()

if __name__ == "__main__":
    main()