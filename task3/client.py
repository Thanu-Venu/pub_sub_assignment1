import socket
import sys
import threading


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[CLIENT] Server disconnected.")
                break
            print(data.decode().strip())
        except:
            break


def run_client(ip, port, role, topic):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    sock.sendall((role + "\n").encode())
    sock.sendall((topic + "\n").encode())

    print(f"[CLIENT] {role} connected on topic [{topic}]")

    if role == "SUBSCRIBER":
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
        while True:
            pass

    else:
        while True:
            msg = input("> ")
            if msg.lower() == "terminate":
                break
            sock.sendall((msg + "\n").encode())

    sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python client.py <IP> <PORT> <PUBLISHER|SUBSCRIBER> <TOPIC>")
        sys.exit(1)

    run_client(
        sys.argv[1],
        int(sys.argv[2]),
        sys.argv[3].upper(),
        sys.argv[4].upper()
    )
