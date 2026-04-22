from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "inventario.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db_connection()
    productos = conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", productos=productos)

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
            (nombre, categoria, precio, stock)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("form.html", producto=None, accion="Registrar")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_db_connection()
    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (id,)).fetchone()

    if not producto:
        conn.close()
        return "Producto no encontrado", 404

    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        conn.execute(
            "UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre, categoria, precio, stock, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("form.html", producto=producto, accion="Editar")

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)