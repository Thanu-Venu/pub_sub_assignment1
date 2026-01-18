# 📡 Middleware Architectures (SCS2314) — Assignment 01  
## ✅ Task 2: Publishers & Subscribers (Python TCP Sockets)

This folder contains the **Task 2** implementation of a simple **Publish/Subscribe middleware** using a **multi-client TCP server** and CLI clients acting as **Publishers** or **Subscribers**.

---

## 🎯 Task 2 Requirements Covered
✅ Server handles **multiple concurrent client connections**  
✅ Client runs in **PUBLISHER** or **SUBSCRIBER** mode (3rd CLI argument)  
✅ Text typed by **Publisher** is displayed on:
- ✅ Server terminal
- ✅ All **Subscriber** terminals  
❌ Publisher messages are **NOT** shown on Publisher terminals (only subscribers)

---

## 🛠️ Tech Stack
- **Python 3**
- **TCP sockets**
- **Threading** (server handles multiple clients concurrently)
- **CLI only** (as required)

---

## 📁 Folder Structure
task2/
├── server.py
├── client.py
└── README.md

---

## ✅ How to Run (Windows / PowerShell / VS Code Terminal)

### 1️⃣ Start the Server (Terminal 1)
Go into the `task2` folder:
```powershell
cd task2
Run server with a port number (example: 5000):

python server.py 5000


Expected output:

[SERVER] Listening on 0.0.0.0:5000

2️⃣ Start Clients (Open Multiple Terminals)

Use separate terminals for each client.

Terminal 2 — Publisher
python client.py 127.0.0.1 5000 PUBLISHER

Terminal 3 — Subscriber 1
python client.py 127.0.0.1 5000 SUBSCRIBER

Terminal 4 — Subscriber 2
python client.py 127.0.0.1 5000 SUBSCRIBER


✅ Now you have:

1 Publisher

2 Subscribers

💬 How Messaging Works

Publisher types a message → Server receives it and prints it

Server broadcasts the message to all subscribers only

Subscribers print the message instantly

Example:

Publisher types:

hello everyone


Server prints:

[SERVER] From PUBLISHER 127.0.0.1:xxxxx -> hello everyone


Subscribers print:

[PUBLISHER 127.0.0.1:xxxxx] hello everyone

🛑 How to Stop the Programs
✅ Stop Publisher

In Publisher terminal type:

terminate

✅ Stop Subscriber

In Subscriber terminal press:

Ctrl + C

✅ Stop Server

Normally:

Ctrl + C