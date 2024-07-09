# database.py
import sqlite3
import hashlib

class Database:
    def __init__(self, db_file='users.db'):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError('O usuário já existe.')
        finally:
            self.close_connection()

    def login_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:

            self.cursor.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password_hash))
            user = self.cursor.fetchone()
            if user:
                return True
            else:
                return False
        finally:
            self.close_connection()
    def close_connection(self):
        if self.conn:
            self.conn.close()
