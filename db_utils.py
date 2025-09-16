import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_type TEXT,
        table_number TEXT,
        subtotal REAL,
        gst REAL,
        discount REAL,
        final_total REAL,
        payment_method TEXT,
        timestamp TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )''')
    conn.commit()
    conn.close()

def insert_menu_from_csv(file_path='menu.csv'):
    df = pd.read_csv(file_path)
    conn = sqlite3.connect('restaurant.db')
    df.to_sql('menu', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def load_menu():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, price FROM menu")
    items = cursor.fetchall()
    conn.close()
    return items

def save_order(order_type, table_number, items, subtotal, gst, discount, total, payment_method):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (order_type, table_number, subtotal, gst, discount, final_total, payment_method, timestamp) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (
            order_type,
            table_number,
            subtotal,
            gst,
            discount,
            total,
            payment_method,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    )
    order_id = cursor.lastrowid

    for item, qty, price in items:
        cursor.execute(
            "INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item, qty, price)
        )

    conn.commit()
    conn.close()
