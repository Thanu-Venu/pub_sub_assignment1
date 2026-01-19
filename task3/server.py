#!/usr/bin/env python3
import socket
import sys
import threading

clients = []
clients_lock = threading.Lock()


def recv_line(conn: socket.socket) -> str:
    """
    Read a single line ending with '\n' from the socket.
    Returns "" if the client disconnects before sending a full line.
    """
    buffer = b""
    while True:
        try:
            chunk = conn.recv(1)
        except (ConnectionResetError, OSError):
            return ""

        if not chunk:
            return ""
        if chunk == b"\n":
            break
        buffer += chunk

    return buffer.decode("utf-8", errors="replace").strip()


def broadcast_by_topic(message: str, topic: str) -> None:
    dead = []

    with clients_lock:
        for c in clients:
            if c["role"] == "SUBSCRIBER" and c["topic"] == topic:
                try:
                    c["socket"].sendall((message + "\n").encode("utf-8"))
                except (ConnectionResetError, BrokenPipeError, OSError):
                    dead.append(c)

        for d in dead:
            try:
                clients.remove(d)
            except ValueError:
                pass
            try:
                d["socket"].close()
            except Exception:
                pass


def handle_client(conn: socket.socket, addr) -> None:
    ip, port = addr[0], addr[1]
    print(f"[SERVER] Connected: {ip}:{port}")

    role = recv_line(conn).upper()
    topic = recv_line(conn).upper()

    if role not in ("PUBLISHER", "SUBSCRIBER") or topic == "":
        try:
            conn.close()
        except Exception:
            pass
        print(f"[SERVER] Invalid handshake from {ip}:{port}. Connection closed.")
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
            try:
                data = conn.recv(1024)
            except (ConnectionResetError, OSError):
                print(f"[SERVER] Disconnected unexpectedly: {ip}:{port}")
                break

            if not data:
                break

            msg = data.decode("utf-8", errors="replace").strip()
            if not msg:
                continue

            print(f"[SERVER] {role} [{topic}] -> {msg}")

            if role == "PUBLISHER":
                broadcast_by_topic(f"[{topic}] {msg}", topic)

    finally:
        with clients_lock:
            clients[:] = [c for c in clients if c["socket"] != conn]

        try:
            conn.close()
        except Exception:
            pass

        print(f"[SERVER] Disconnected: {ip}:{port}")


def run_server(port: int) -> None:
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
        print("\n[SERVER] Server stopped (KeyboardInterrupt).")
    finally:
        try:
            server.close()
        except Exception:
            pass
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
