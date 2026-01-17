
---

## 📄 Task 2 `README.md`
**Location:** `/task2/README.md`

```md
# Task 2 – Publishers and Subscribers

## Objective
To extend the client–server application to support multiple concurrent clients acting as publishers or subscribers.

## Description
- Server handles multiple client connections concurrently.
- Clients can join as either:
  - PUBLISHER
  - SUBSCRIBER
- Messages sent by publishers are forwarded to all subscribers.
- Publisher messages are not shown on other publisher terminals.

## How to Run
### Server
```bash
my_server_app <PORT>
