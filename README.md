# Real-Time Messaging System

A WebSocket-based messaging system with a Python server and web client interface.

## Features
- Real-time message broadcasting
- Connection status indicators
- Message history persistence
- Responsive UI with system messages
- Client identification

## Prerequisites
- Python 3.7+
- Modern web browser

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server
```bash
python server.py
```

### Accessing Clients
1. Start a web server in the project directory:
```bash
python -m http.server 8000
```

2. Open clients in your browser:
- Message Display: http://localhost:8000/index.html
- Chat Interface: http://localhost:8000/client.html

Open multiple client tabs/windows to test real-time communication.

## Project Structure
