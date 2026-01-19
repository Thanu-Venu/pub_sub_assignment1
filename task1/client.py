#!/usr/bin/env python3
import socket
import sys


def run_client(server_ip: str, port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((server_ip, port))
        print(f"[CLIENT] Connected to {server_ip}:{port}")
        print('[CLIENT] Type messages and press Enter. Type "terminate" to exit.')

        while True:
            text = input("> ").strip()

            if text.lower() == "terminate":
                print("[CLIENT] Terminating and disconnecting...")
                break

            sock.sendall((text + "\n").encode("utf-8"))

    except ConnectionRefusedError:
        print("[CLIENT] Connection refused. Make sure server is running and IP/PORT are correct.")
    except KeyboardInterrupt:
        print("\n[CLIENT] Stopping client (KeyboardInterrupt).")
    finally:
        try:
            sock.close()
        except Exception:
            pass
        print("[CLIENT] Client closed.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <SERVER_IP> <PORT>")
        sys.exit(1)

    server_ip = sys.argv[1]

    try:
        port_num = int(sys.argv[2])
        if not (1 <= port_num <= 65535):
            raise ValueError
    except ValueError:
        print("Error: PORT must be an integer between 1 and 65535")
        sys.exit(1)

    run_client(server_ip, port_num)
