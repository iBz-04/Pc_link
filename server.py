import asyncio
import websockets
import logging 
import json


logging.basicConfig(level=logging.INFO)


connected_clients = set()

async def broadcast(message):
    """Send a message to all connected clients."""
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

async def handler(websocket):
    """Handles individual WebSocket client connections."""
    logging.info(f"Client connected from {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            logging.info(f"Received message from {websocket.remote_address}: {message}")
            await broadcast(message)
            
    except websockets.exceptions.ConnectionClosedOK:
        logging.info(f"Client {websocket.remote_address} disconnected normally.")
    except websockets.exceptions.ConnectionClosedError as e:
        logging.warning(f"Client {websocket.remote_address} disconnected with error: {e.code} {e.reason}")
    finally:
        connected_clients.discard(websocket)
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