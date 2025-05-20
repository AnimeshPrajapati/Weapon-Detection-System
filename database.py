import sqlite3

DB_FILE = "database.db"

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            filename TEXT,
            prediction TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert a new log entry
def insert_log(filename, prediction, timestamp):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO uploads VALUES (?, ?, ?)", (filename, prediction, timestamp))
    conn.commit()
    conn.close()

# Retrieve all log entries
def get_logs():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM uploads")
    rows = c.fetchall()
    conn.close()
    return rows
