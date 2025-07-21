import sqlite3
import os

DB_PATH = "data/receipts.db"

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            vendor TEXT,
            date TEXT,
            amount REAL,
            category TEXT
        );
    """)
    conn.commit()
    conn.close()

def insert_receipt(filename, vendor, date, amount, category):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO receipts (filename, vendor, date, amount, category)
        VALUES (?, ?, ?, ?, ?);
    """, (filename, vendor, date, amount, category))
    conn.commit()
    conn.close()

def get_all_receipts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts;")
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_by_vendor(vendor_query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM receipts WHERE vendor LIKE ?;
    """, ('%' + vendor_query + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows

def sort_by(field, order='ASC'):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT * FROM receipts ORDER BY {field} {order};
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_receipt(receipt_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receipts WHERE id = ?;", (receipt_id,))
    conn.commit()
    conn.close()

