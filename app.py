from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_employees():
    conn = psycopg2.connect(
        dbname="employees_db",
        user="postgres",
        password="postgres",
        host="db",   # container name of PostgreSQL
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, address FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route("/")
def index():
    employees = get_employees()
    return render_template("index.html", employees=employees)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
