#!/usr/bin/env python3
import socket
import sys
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[CLIENT] Server Disconnected.")
                break
            print(data.decode("utf-8").strip())
        except:
            break

def run_client(server_ip: str, port: int, role: str) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        sock.connect((server_ip, port))
        print(f"[CLIENT] Connected to {server_ip}:{port}")

        
        sock.sendall((role + "\n").encode("utf-8"))
        print(f"[CLIENT] Running as {role}")

        
        if role == "SUBSCRIBER":
            print("[CLIENT] Waiting for messages from publishers...\n")
            thread = threading.Thread(target=receive_messages, args=(sock,))
            thread.daemon = True
            thread.start()

           
            while True:
                pass

       
        elif role == "PUBLISHER":
            print('Type messages and press Enter. Type "terminate" to exit.\n')
            while True:
                message = input("> ").strip()
                if message.lower() == "terminate":
                    sock.sendall("terminate\n".encode("utf-8"))
                    print("[CLIENT] Terminating connection...")
                    break
                sock.sendall((message + "\n").encode("utf-8"))

    except ConnectionRefusedError:
        print("[CLIENT] Connection refused. Is the server running?")
    except KeyboardInterrupt:
        print("\n[CLIENT] Client stopped.")
    finally:
        sock.close()
        print("[CLIENT] Connection closed.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <SERVER_IP> <PORT> <PUBLISHER|SUBSCRIBER>")
        sys.exit(1)

    server_ip = sys.argv[1]

    try:
        port_num = int(sys.argv[2])
    except ValueError:
        print("PORT must be a number.")
        sys.exit(1)

    role = sys.argv[3].upper()
    if role not in ("PUBLISHER", "SUBSCRIBER"):
        print("Role must be PUBLISHER or SUBSCRIBER.")
        sys.exit(1)

    run_client(server_ip, port_num, role)
