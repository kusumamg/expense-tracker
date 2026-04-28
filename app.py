from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------- DB INIT ----------
# ---------- DB INIT ----------
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            amount INTEGER,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# ✅ ADD THIS LINE HERE (VERY IMPORTANT)
init_db()

def get_db():
    return sqlite3.connect('database.db')

# ---------- MAIN PAGE ----------
@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY id DESC")
    data = cur.fetchall()
    conn.close()

    income = sum([x[3] for x in data if x[2] == 'income'])
    expense = sum([x[3] for x in data if x[2] == 'expense'])
    balance = income - expense

    current_date = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        'index.html',
        data=data,
        balance=balance,
        income=income,
        expense=expense,
        current_date=current_date
    )

# ---------- ADD ----------
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    type_ = request.form['type']
    amount = request.form['amount']
    date = request.form['date']

    if not amount.isdigit():
        return "Invalid amount"

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (name, type, amount, date) VALUES (?, ?, ?, ?)",
        (name, type_, int(amount), date)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


# ---------- START ----------
import os


init_db()
