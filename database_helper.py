import sqlite3
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)
load_dotenv('keys.env')
SQLITE_PATH = os.getenv('SQLITE_PATH', 'comics.db')

users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT, 
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

reading_list_table =   """
CREATE TABLE IF NOT EXISTS reading_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    series_name TEXT NOT NULL,
    added_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, series_name),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

class DbHandler:

    @staticmethod
    def open_connection():
        conn = sqlite3.connect(SQLITE_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.open_connection()
        conn.execute(users_table)
        conn.execute(reading_list_table)
        conn.commit()
        conn.close()

    def add_user(self, chat_id, user):
        conn = self.open_connection()
        conn.execute("INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (chat_id,user))
        conn.commit()
        conn.close()

    def add_series(self, user_id, series_name):
        conn = self.open_connection()
        conn.execute("INSERT OR IGNORE INTO reading_list (user_id, series_name) VALUES (?, ?)", (user_id, series_name))
        conn.commit()
        conn.close()

    def get_reading_list(self,user_id):
        conn = self.open_connection()
        cursor = conn.execute("SELECT series_name from reading_list WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['series_name'] for row in rows]

    def remove_series(self, user_id, series_name):
        conn = self.open_connection()
        conn.execute("DELETE from reading_list WHERE user_id = ? AND series_name = ?", (user_id, series_name))
        conn.commit()
        conn.close()

    def get_user(self, id):
        conn = self.open_connection()
        cursor = conn.execute("SELECT id from users WHERE id = ?", (id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['id'] for row in rows]

    def add_many(self, user_id, comic_list):
        added = 0
        if isinstance(comic_list, str):
            comic_list = comic_list.split('\n')
        for comic in comic_list:
            comic_title = comic.strip().lower()
            if not comic_title:
                continue
            added += 1
            self.add_series(user_id, comic_title)
        return added

    def remove_many(self, user_id, comic_list):
        removed = 0
        if isinstance(comic_list, str):
            comic_list = comic_list.split('\n')
        for comic in comic_list:
            comic_title = comic.strip().lower()
            if not comic_title:
                continue
            removed += 1
            self.add_series(user_id, comic_title)
        return removed
