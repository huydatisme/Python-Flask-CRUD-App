from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)
app.secret_key = 'flash message'

# Cấu hình kết nối MySQL
db_config = {
    'host': 'flaskapp-server.mysql.database.azure.com',
    'user': 'gnhtcebvax',
    'password': 'CJcTF25jDk$W9wk8',
    'db': 'flaskapp-database',
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

def create_database_and_table():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Execute SQL commands from the file
            with open('create_database.sql', 'r') as f:
                sql_script = f.read()
                cursor.execute(sql_script)
        connection.commit()
    finally:
        connection.close()

create_database_and_table()

@app.route('/')
def index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM students")
            data = cur.fetchall()
        return render_template('index.html', students=data)
    finally:
        connection.close()

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        connection = get_db_connection()
        try:
            with connection.cursor() as cur:
                cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
            connection.commit()
        finally:
            connection.close()
        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        flash("Data Updated Successfully")

        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        connection = get_db_connection()
        try:
            with connection.cursor() as cur:
                cur.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s
                WHERE id=%s
                """, (name, email, phone, id_data))
            connection.commit()
        finally:
            connection.close()
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['POST'])
def delete(id_data):
    flash("Data Deleted Successfully")

    connection = get_db_connection()
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
