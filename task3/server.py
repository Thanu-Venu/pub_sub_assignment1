#!/usr/bin/env python3
import socket
import sys
import threading

# Store clients as dictionaries
clients = []  # { "socket": conn, "role": role, "topic": topic }
clients_lock = threading.Lock()


def recv_line(conn):
    buffer = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            return ""
        if chunk == b"\n":
            break
        buffer += chunk
    return buffer.decode().strip()


def broadcast_by_topic(message, topic):
    dead = []

    with clients_lock:
        for c in clients:
            if c["role"] == "SUBSCRIBER" and c["topic"] == topic:
                try:
                    c["socket"].sendall((message + "\n").encode())
                except:
                    dead.append(c)

        for d in dead:
            clients.remove(d)
            d["socket"].close()


def handle_client(conn, addr):
    ip, port = addr
    print(f"[SERVER] Connected: {ip}:{port}")

    role = recv_line(conn).upper()
    topic = recv_line(conn).upper()

    if role not in ("PUBLISHER", "SUBSCRIBER"):
        conn.close()
        return

    with clients_lock:
        clients.append({
            "socket": conn,
            "role": role,
            "topic": topic
        })

    print(f"[SERVER] {ip}:{port} registered as {role} on topic [{topic}]")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()
            print(f"[SERVER] {role} [{topic}] -> {msg}")

            if role == "PUBLISHER":
                broadcast_by_topic(f"[{topic}] {msg}", topic)

    finally:
        with clients_lock:
            clients[:] = [c for c in clients if c["socket"] != conn]
        conn.close()
        print(f"[SERVER] Disconnected: {ip}:{port}")


def run_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen()

    print(f"[SERVER] Listening on port {port}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[SERVER] Server stopped")
    finally:
        server.close()


if __name__ == "__main__":
    run_server(int(sys.argv[1]))
