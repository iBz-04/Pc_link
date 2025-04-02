import sqlite3
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageDatabase:
    def __init__(self, db_path="messages.db"):
        """Initialize the database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Create the database tables if they don't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create messages table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()

    def store_message(self, message_data):
        """Store a message in the database.
        
        Args:
            message_data: JSON string or dict containing sender, text, and timestamp
        """
        try:
            # Parse message if it's a JSON string
            if isinstance(message_data, str):
                try:
                    data = json.loads(message_data)
                except json.JSONDecodeError:
                    # If not valid JSON, treat as raw message
                    data = {
                        "sender": "unknown",
                        "text": message_data,
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                data = message_data
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)",
                (data.get("sender", "unknown"), data.get("text", ""), data.get("timestamp", datetime.now().isoformat()))
            )
            
            conn.commit()
            logger.info(f"Message stored in database from {data.get('sender', 'unknown')}")
        except sqlite3.Error as e:
            logger.error(f"Error storing message: {e}")
        except Exception as e:
            logger.error(f"Unexpected error storing message: {e}")
        finally:
            if conn:
                conn.close()

    def get_recent_messages(self, limit=50):
        """Retrieve recent messages from the database.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        messages = []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM messages ORDER BY id DESC LIMIT ?", 
                (limit,)
            )
            
            rows = cursor.fetchall()
            
            # Convert rows to dictionaries
            for row in reversed(rows):  # Reverse to get oldest first
                messages.append({
                    "sender": row["sender"],
                    "text": row["message"],
                    "timestamp": row["timestamp"]
                })
                
            logger.info(f"Retrieved {len(messages)} messages from database")
        except sqlite3.Error as e:
            logger.error(f"Error retrieving messages: {e}")
        finally:
            if conn:
                conn.close()
                
        return messages 