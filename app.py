from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'clave_segura'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO contacts (name, email, phone, created_at) VALUES (%s, %s, %s, %s)",
                (name, email, phone, datetime.now())
            )
            conn.commit()
            flash("Contacto agregado correctamente.", "success")
        except mysql.connector.Error as err:
            flash(f"Error al agregar contacto: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    else:
        flash("No se pudo conectar a la base de datos.", "danger")

    return redirect(url_for('index'))

@app.route('/contacts')
def contacts():
    conn = get_db_connection()
    data = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('contacts.html', contacts=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
