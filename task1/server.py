#!/usr/bin/env python3
import socket
import sys


def run_server(port: int) -> None:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_sock.bind(("0.0.0.0", port))
    server_sock.listen(1)

    print(f"[SERVER] Listening on 0.0.0.0:{port}")

    conn, addr = server_sock.accept()
    print(f"[SERVER] Client connected from {addr[0]}:{addr[1]}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("[SERVER] Client disconnected.")
                break

            message = data.decode("utf-8", errors="replace").rstrip("\n")
            print(f"[SERVER] Received: {message}")

    except KeyboardInterrupt:
        print("\n[SERVER] Stopping server (KeyboardInterrupt).")
    finally:
        try:
            conn.close()
        except Exception:
            pass
        server_sock.close()
        print("[SERVER] Server closed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    try:
        port_num = int(sys.argv[1])
        if not (1 <= port_num <= 65535):
            raise ValueError
    except ValueError:
        print("Error: PORT must be an integer between 1 and 65535")
        sys.exit(1)

    run_server(port_num)
