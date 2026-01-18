# 📡 Middleware Architectures – Assignment 01  
## Task 1: Client–Server Socket Application (Python)

**Module:** SCS2314 – Middleware Architectures  
**University:** UCSC  
**Year:** 2025  
**Task:** Basic Client–Server communication using sockets

---

## 🎯 Objective
The objective of Task 1 is to demonstrate basic **Client–Server communication** using **TCP sockets**.  
A client sends text messages via a Command Line Interface (CLI), and the server displays those messages on its terminal.

---

## 🛠️ Technology Stack
- Language: **Python 3**
- Communication: **TCP Sockets**
- Interface: **Command Line (CLI)**

---

## 📁 Directory Structure
-task1/
-├── server.py
-├── client.py
-└── README.md

---

## ▶️ How to Run the Application

### 🔹 Step 1: Start the Server
Open a terminal and navigate to the project folder.

**Windows**
```bash
python server.py 5000

Expected output:
[SERVER] Listening on 0.0.0.0:5000

### 🔹 Step 2: Start the Client

Open a new terminal in the same folder.

Windows

python client.py 127.0.0.1 5000
Expected output:

[CLIENT] Connected to 127.0.0.1:5000
💬 Communication Flow

Type any text in the client terminal

The message will appear instantly on the server terminal

The client runs continuously until a termination keyword is entered

❌ Terminating the Client

To stop the client, type:

terminate


Expected behavior:

Client disconnects from server

Client program exits

Server detects client disconnection