import sqlite3
from sqlite3 import Error
import os
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shortener.db')

def create_table():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id TEXT PRIMARY KEY,
            target_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            clicks INTEGER DEFAULT 0
        )
        ''')
        
        conn.commit()
        logger.info("Tables Created Successfully!")
    except Error as e: 
        logger.error(f"Error trying to create tables: {e}")
    finally: 
        if conn:
            conn.close()
            
@contextmanager
def get_db_connection():
    """
    Context manager for connection with DB
    """
    conn = None
    try: 
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
    except Error as e: 
        logger.error(f"Error on connection to database: {e}")
        raise
    finally:
        if conn:
            conn.close()
            
def insert_url(short_id, target_url):
    """
    Insert a new url to DB
    
        Args:
        short_id: short id for url
        target_url: original url
        
        Returns:
        bool: True if successful, False otherwise
    """
    try: 
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO urls (id, target_url) VALUES (?, ?)",
                (short_id, target_url)
                )
            conn.commit()
            return True
    except Error as e:
        logger.error(f"Error inserting URL: {e}")
        return False


def get_url_by_id(short_id):
    """
    Get URL by ID
    
    Args:
        short_id: short id for url
        
    Returns:
        dict: URL data or None otherwise
    """
    
    try: 
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, target_url FROM urls WHERE id = ?",
                (short_id,)
                )
            result = cursor.fetchone()
            return dict(result) if result else None
        
    except Error as e:
        logger.error(f"Error searching url: {e}")
        return None
    
def increment_clicks(short_id):
    """
    Increments the click counter for a URL
    
    Args:
        short_id: Short ID/URL identifier
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE urls SET clicks = clicks + 1 WHERE id = ?",
                (short_id,)
            )
            conn.commit()
    except Error as e:
        logger.error(f"Error updating click counter, {e}")
        
def check_id_exists(short_id):
    """
    Verify if id exists in DB
    
    Args:
        short_id: ID to check
        
    Returns:
        bool: True if ID exists, False otherwise
    """
    try: 
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM urls WHERE id = ? LIMIT 1",
                (short_id,)
            )
            return cursor.fetchone() is not None
    except Error as e:
        logger.error(f"Error trying to check ID: {e}")
        return False
    
def get_url_stats(limit=10):
    """
    Retrieves statistics of the most accessed URLs

    Args:
        limit: Maximum number of URLs to return

    Returns:
        list: List of dictionaries with URL statistics
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, target_url, created_at, clicks 
                FROM urls 
                ORDER BY clicks DESC 
                LIMIT ?
                """,
                (limit,)
            )
            results = cursor.fetchall()
            return [dict(row) for row in results]
    except Error as e:
        logger.error(f"Error trying to search statistics, {e}")
        return []

def delete_url(short_id: str) -> bool:
    """
    Delete a URL by its short_id

    Args:
        short_id (str): The short ID of the URL to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM urls WHERE id = ?",
                (short_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
    except Error as e:
        logger.error(f"Error deleting URL: {e}")
        return False