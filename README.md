# HTTP Proxy Server

This project is a simple **HTTP/1.0 proxy server** implemented in Python. It handles **GET requests**, relays them to the destination server, and returns the responses to the clients.

## Features
- Supports only **HTTP/1.0 GET** requests.
- Returns **501 Not Implemented** for unsupported methods.
- Parses and forwards **absolute URIs**.
- Handles multiple concurrent client connections using **`fork()`**.
- Proper error handling with HTTP status codes (400, 502, 503).

## Requirements
- Python 3.x or above.
- Unix-based system (for `fork()` support)

## How to Run on Linux 

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/http-proxy-server.git
    cd http-proxy-server
    ```

2. Run the proxy server:
    ```bash
    python http_proxy.py <port>
    ```
    Example:
    ```bash
    python http_proxy.py 8080
    ```

### outputs attached for reference

3. Configure your browser or tool to use `localhost:<port>` as the HTTP proxy.

## Project Structure
- `http_proxy.py` : Main proxy server code.

## Key Notes
- Only handles **HTTP**, not HTTPS.
- Tested on Linux environments.
