import asyncio
import websockets
import logging 
import json
from database import MessageDatabase

logging.basicConfig(level=logging.INFO)

db = MessageDatabase()
connected_clients = set()

async def broadcast(message):
    """Send a message to all connected clients."""
    db.store_message(message)
    
    if connected_clients:
        tasks = [asyncio.create_task(client.send(message)) for client in connected_clients]
        
        done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

        for task in done:
            try:
                task.result()
            except websockets.exceptions.ConnectionClosed as e:
                logging.info(f"Client connection closed during broadcast: {e.code} {e.reason}")
                pass
            except Exception as e:
                logging.error(f"Error during broadcast send: {e}")

async def send_message_history(websocket):
    """Send message history to a newly connected client."""
    try:
        recent_messages = db.get_recent_messages(30)  
        if recent_messages:
            logging.info(f"Sending message history ({len(recent_messages)} messages) to client {websocket.remote_address}")
            history_message = {
                "sender": "system",
                "text": "Message History",
                "type": "history_start",
                "timestamp": ""
            }
            await websocket.send(json.dumps(history_message))
            
            for message in recent_messages:
                await websocket.send(json.dumps(message))
                
            history_end = {
                "sender": "system",
                "text": "End of History",
                "type": "history_end",
                "timestamp": ""
            }
            await websocket.send(json.dumps(history_end))
    except Exception as e:
        logging.error(f"Error sending message history: {e}")

async def handler(websocket):
    """Handles individual WebSocket client connections."""
    logging.info(f"Client connected from {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        
        connection_msg = json.dumps({
            "sender": "system",
            "text": "New client connected",
            "timestamp": ""
        })
        await broadcast(connection_msg)
        
        
        await send_message_history(websocket)
        
        async for message in websocket:
            logging.info(f"Received message from {websocket.remote_address}: {message}")
            await broadcast(message)
            
    except websockets.exceptions.ConnectionClosedOK:
        logging.info(f"Client {websocket.remote_address} disconnected normally.")
    except websockets.exceptions.ConnectionClosedError as e:
        logging.warning(f"Client {websocket.remote_address} disconnected with error: {e.code} {e.reason}")
    finally:
        connected_clients.discard(websocket)
      
        disconnection_msg = json.dumps({
            "sender": "system",
            "text": "A client disconnected",
            "timestamp": ""
        })
        await broadcast(disconnection_msg)
        logging.info(f"Client {websocket.remote_address} removed. Total clients: {len(connected_clients)}")

async def main():
    logging.info("Starting WebSocket server on ws://0.0.0.0:8765")
    server = await websockets.serve(handler, "0.0.0.0", 8765)
    logging.info("WebSocket server started successfully.")
    await server.wait_closed() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    except Exception as e:
        logging.error(f"Server failed to start or run: {e}") 