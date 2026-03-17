import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = 'data/finance_tracker.db'

def init_db():
    """Initialize database and create transactions table if not exists."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(trans_type: str, category: str, amount: float, description: str = '') -> None:
    """Add a new transaction."""
    init_db()  # Ensure DB exists
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        'INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)',
        (date_str, trans_type, category, amount, description)
    )
    conn.commit()
    conn.close()

def get_all_transactions() -> List[Dict]:
    """Fetch all transactions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{'id': row[0], 'date': row[1], 'type': row[2], 'category': row[3], 'amount': row[4], 'description': row[5]} for row in rows]

def get_balance() -> float:
    """Calculate current balance: income - expenses."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expense = cursor.fetchone()[0] or 0
    conn.close()
    return income - expense

def get_transactions_by_category() -> Dict[str, float]:
    """Get total amount per category for expenses."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='expense' GROUP BY category")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}

def get_monthly_trends() -> List[Dict]:
    """Get monthly totals for income and expenses."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT strftime('%Y-%m', date) as month, type, SUM(amount) as total FROM transactions GROUP BY month, type ORDER BY month DESC")
    rows = cursor.fetchall()
    conn.close()
    months = {}
    for row in rows:
        month, typ, total = row
        if month not in months:
            months[month] = {'income': 0, 'expense': 0}
        months[month][typ] = total
    return [{'month': k, **v} for k, v in sorted(months.items(), reverse=True)]

