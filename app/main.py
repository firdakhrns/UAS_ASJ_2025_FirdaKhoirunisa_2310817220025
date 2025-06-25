from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM review")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['POST'])
def add():
    nama = request.form['nama']
    toko = request.form['toko']
    nilai = request.form['nilai']
    komentar = request.form['komentar']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO review (nama, toko, nilai, komentar) VALUES (%s, %s, %s, %s)", (nama, toko, nilai, komentar))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM review WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        nama = request.form['nama']
        toko = request.form['toko']
        nilai = request.form['nilai']
        komentar = request.form['komentar']
        cursor.execute("UPDATE review SET nama=%s, toko=%s, nilai=%s, komentar=%s WHERE id=%s", (nama, toko, nilai, komentar, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute("SELECT * FROM review WHERE id = %s", (id,))
        data = cursor.fetchone()
        conn.close()
        return render_template('edit.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')