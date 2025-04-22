import socket
import os
import sys

if len(sys.argv) != 2:
    print("Usage: python proxy.py <port>")
    sys.exit(1)

port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", port))
server.listen(100)

print(f"Proxy Server Running on Port {port}")

def handle_client_request(client_socket):
    try:
        request = client_socket.recv(4096)
        if not request:
            client_socket.close()
            return

        request_lines = request.split(b"\r\n")
        request_line = request_lines[0].decode("utf-8")

        if not request_line.startswith("GET "):
            response = b"HTTP/1.0 501 Not Implemented\r\nContent-Type: text/html\r\n\r\n"
            response += b"<html><body><h1>501 Not Implemented</h1><p>The requested HTTP method is not supported.</p></body></html>"
            client_socket.sendall(response)
            client_socket.close()
            return
        if b"Host:" not in request:
            response = b"HTTP/1.0 400 Bad Request\r\nContent-Type: text/html\r\n\r\n"
            response += b"<html><body><h1>400 Bad Request</h1><p>The request is missing a valid Host header.</p></body></html>"
            client_socket.sendall(response)
            client_socket.close()
            return

        host, port = extract_host_port_from_request(request)

        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.connect((host, port))

        request = request.replace(b"HTTP/1.1", b"HTTP/1.0")
        destination_socket.sendall(request)

        while True:
            data = destination_socket.recv(4096)
            if not data:
                break
            client_socket.sendall(data)
            
        client_socket.close()
        destination_socket.close()

    except Exception as e:
        print("Error:", e)
        client_socket.close()


def extract_host_port_from_request(request):
    host_line = next((line for line in request.split(b"\r\n") if line.startswith(b"Host:")), None)
    if not host_line:
        return None, None

    host = host_line.split(b":", 1)[1].strip().decode("utf-8")
    if ":" in host:
        hostname, port = host.split(":")
        return hostname, int(port)
    return host, 80

while True:
    client_socket, addr = server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")

    pid = os.fork()
    if pid == 0:
        server.close()
        handle_client_request(client_socket)
        os._exit(0)
    else:
        client_socket.close()
