import sqlite3

DB_NAME = "eventflow.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT NOT NULL,
            event_date TEXT NOT NULL,
            capacity INTEGER NOT NULL CHECK (capacity > 0),
            price REAL NOT NULL DEFAULT 0 CHECK (price >= 0)
        );
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            places INTEGER NOT NULL CHECK (places > 0),
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

def query(sql, params=()):
    """Exécute un SELECT et retourne toutes les lignes."""
    conn = get_connection()
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()

def query_one(sql, params=()):
    rows = query(sql, params)
    return rows[0] if rows else None

def execute(sql, params=()):
    """Exécute un INSERT/UPDATE/DELETE. Retourne (id créé, lignes modifiées)."""
    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid, cur.rowcount
    finally:
        conn.close()