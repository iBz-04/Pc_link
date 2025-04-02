# iPhone to PC instant messaging link
A WebSocket-based messaging system with a Python server and web client interface.

## Features
- Real-time message broadcasting
- Connection status indicators
- SQLite database for message persistence
- Message history display for new connections
- Responsive UI with system messages
- Client identification

## Prerequisites
- Python 3.7+
- Modern web browser
- SQLite3

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
The server will create and use a SQLite database file `messages.db` in the same directory.

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

├── server.py # server implementation
├── database.py # database operations
├── index.html # PC interface
├── client.html # mobile phone interface
├── requirements.txt
├── messages.db # SQLite database (created on first run)
