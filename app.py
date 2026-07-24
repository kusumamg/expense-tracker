from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import csv
from datetime import datetime
import io

app = Flask(__name__)

# ---------------- DATABASE ---------------- #

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)

    cur.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY,
    theme TEXT DEFAULT 'light',
    currency TEXT DEFAULT '₹',
    date_format TEXT DEFAULT 'YYYY-MM-DD',
    notifications INTEGER DEFAULT 1
)
""")

    cur.execute("""
INSERT OR IGNORE INTO settings
(id, theme, currency, date_format, notifications)
VALUES
(1,'light','₹','YYYY-MM-DD',1)
""")

    conn.commit()
    conn.close()


def get_db():
    return sqlite3.connect("database.db")


init_db()

# ---------------- HOME ---------------- #

@app.route("/")
@app.route("/dashboard")
def dashboard():

    search = request.args.get("search", "")
    filter_date = request.args.get("filter_date", "")

    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if search:
        query += " AND name LIKE ?"
        params.append("%" + search + "%")

    if filter_date:
        query += " AND date=?"
        params.append(filter_date)

    query += " ORDER BY id DESC"

    cur.execute(query, params)
    data = cur.fetchall()

    income = sum(item[3] for item in data if item[2] == "income")
    expense = sum(item[3] for item in data if item[2] == "expense")
    balance = income - expense

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Get theme and currency
    cur.execute("SELECT theme, currency FROM settings WHERE id=1")
    setting = cur.fetchone()

    theme = setting[0]
    currency = setting[1]

    conn.close()

    return render_template(
        "dashboard.html",
        data=data,
        balance=balance,
        income=income,
        expense=expense,
        theme=theme,
        currency=currency,
        current_date=current_date,
        search=search,
        filter_date=filter_date
    )


# Transactions page
@app.route("/transactions")
def transactions():

    search = request.args.get("search", "")
    filter_date = request.args.get("filter_date", "")

    conn = get_db()
    cur = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if search:
        query += " AND name LIKE ?"
        params.append("%" + search + "%")

    if filter_date:
        query += " AND date=?"
        params.append(filter_date)

    query += " ORDER BY id DESC"

    cur.execute(query, params)
    data = cur.fetchall()

    # Get selected currency
    cur.execute("SELECT currency FROM settings WHERE id=1")
    currency = cur.fetchone()[0]

    conn.close()

    return render_template(
        "transactions.html",
        data=data,
        currency=currency,
        search=search,
        filter_date=filter_date
    )
# reports
@app.route("/reports")
def reports():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")

    data = cur.fetchall()

    conn.close()

    income = sum(x[3] for x in data if x[2] == "income")
    expense = sum(x[3] for x in data if x[2] == "expense")

    return render_template(
        "reports.html",
        income=income,
        expense=expense
    )


# analytics
@app.route("/analytics")
def analytics():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses")

    data = cur.fetchall()

    conn.close()

    income = sum(x[3] for x in data if x[2] == "income")
    expense = sum(x[3] for x in data if x[2] == "expense")

    balance = income - expense

    return render_template(
        "analytics.html",
        income=income,
        expense=expense,
        balance=balance,
        total=len(data)
    )

# ---------------- ADD ---------------- #

@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    type_ = request.form["type"]
    amount = request.form["amount"]
    date = request.form["date"]

    if not amount.isdigit():
        return "Invalid Amount"

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO expenses(name,type,amount,date)
        VALUES(?,?,?,?)
        """,
        (name, type_, int(amount), date)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------------- EDIT ---------------- #

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        type_ = request.form["type"]
        amount = request.form["amount"]
        date = request.form["date"]

        cur.execute(
            """
            UPDATE expenses
            SET
                name=?,
                type=?,
                amount=?,
                date=?
            WHERE id=?
            """,
            (name, type_, int(amount), date, id)
        )

        conn.commit()
        conn.close()

        return redirect("/transactions")

    cur.execute(
        "SELECT * FROM expenses WHERE id=?",
        (id,)
    )

    item = cur.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        item=item
    )

# ---------------- DELETE ---------------- #

@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/transactions")



# ---------------- EXPORT CSV ---------------- #

@app.route("/export_csv")
def export_csv():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    data = cur.fetchall()

    conn.close()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Description",
        "Type",
        "Amount",
        "Date"
    ])

    writer.writerows(data)

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
    response.headers["Content-Type"] = "text/csv"

    return response


 # ---------------- SETTINGS ---------------- #

@app.route("/settings")
def settings():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM settings WHERE id=1")

    settings = cur.fetchone()

    conn.close()

    return render_template(
        "settings.html",
        settings=settings
    )


@app.route("/save_settings", methods=["POST"])
def save_settings():

    theme = request.form["theme"]
    currency = request.form["currency"]
    date_format = request.form["date_format"]

    notifications = 1 if request.form.get("notifications") else 0

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE settings
        SET
            theme=?,
            currency=?,
            date_format=?,
            notifications=?
        WHERE id=1
    """,
    (theme, currency, date_format, notifications))

    conn.commit()
    conn.close()

    return redirect("/settings")

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)