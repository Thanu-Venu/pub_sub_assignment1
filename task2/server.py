#!/usr/bin/env python3
import socket
import sys
import threading


# We keep lists of sockets for each role
publishers = []
subscribers = []

# Lock is used to safely edit the lists from multiple threads
clients_lock = threading.Lock()


def recv_line(conn: socket.socket) -> str:
    """
    Reads bytes from conn until a newline '\n' is found.
    Returns the decoded line (without '\n').
    """
    buffer = b""
    while True:
        chunk = conn.recv(1)  # read 1 byte at a time
        if not chunk:
            # client disconnected before sending a full line
            return ""
        if chunk == b"\n":
            break
        buffer += chunk

    return buffer.decode("utf-8", errors="replace").strip()


def broadcast_to_subscribers(message: str) -> None:
    """
    Send a message to all connected subscriber sockets.
    Removes subscribers that are disconnected.
    """
    dead = []

    with clients_lock:
        for sub in subscribers:
            try:
                sub.sendall((message + "\n").encode("utf-8"))
            except Exception:
                # if sending fails, subscriber is likely disconnected
                dead.append(sub)

        # remove dead subscribers
        for sub in dead:
            try:
                subscribers.remove(sub)
            except ValueError:
                pass
            try:
                sub.close()
            except Exception:
                pass


def handle_client(conn: socket.socket, addr) -> None:
    """
    Runs in a separate thread for each connected client.
    Identifies role, then handles messages.
    """
    ip, port = addr[0], addr[1]
    print(f"[SERVER] New connection from {ip}:{port}")

    # Step 1: receive role line from client
    role = recv_line(conn).upper()

    if role not in ("PUBLISHER", "SUBSCRIBER"):
        print(f"[SERVER] Invalid role from {ip}:{port}. Closing connection.")
        try:
            conn.sendall(b"ERROR: Role must be PUBLISHER or SUBSCRIBER\n")
        except Exception:
            pass
        conn.close()
        return

    # Step 2: register client socket in correct list
    with clients_lock:
        if role == "PUBLISHER":
            publishers.append(conn)
        else:
            subscribers.append(conn)

    print(f"[SERVER] Registered {ip}:{port} as {role}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                # client disconnected
                print(f"[SERVER] {role} disconnected: {ip}:{port}")
                break

            # decode message
            msg = data.decode("utf-8", errors="replace").rstrip("\n").strip()

            # server prints messages received from any client (requirement #2)
            print(f"[SERVER] From {role} {ip}:{port} -> {msg}")

            # Step 3: only broadcast if sender is a PUBLISHER
            if role == "PUBLISHER":
                broadcast_to_subscribers(f"[PUBLISHER {ip}:{port}] {msg}")

    except (ConnectionResetError, OSError):
        # Windows: WinError 10054 happens when client closes the terminal/window forcefully
        print(f"[SERVER] {role} disconnected unexpectedly: {ip}:{port}")

    finally:
        # Step 4: clean remove and close
        with clients_lock:
            if conn in publishers:
                publishers.remove(conn)
            if conn in subscribers:
                subscribers.remove(conn)

        try:
            conn.close()
        except Exception:
            pass

        print(f"[SERVER] Connection closed for {ip}:{port}")


def run_server(port: int) -> None:
    # create server socket (TCP)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind and listen
    server_sock.bind(("0.0.0.0", port))
    server_sock.listen()

    print(f"[SERVER] Listening on 0.0.0.0:{port}")

    try:
        while True:
            conn, addr = server_sock.accept()

            # create a new thread for each client
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

    except KeyboardInterrupt:
        print("\n[SERVER] Stopping server (KeyboardInterrupt).")

    finally:
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
