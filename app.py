from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash message'

# Cấu hình kết nối MySQL
db_connection = pymysql.connect(
    host='flaskserver.mysql.database.azure.com',
    user='nhyjmrbbrt',
    password='m',
    db='flaskapp_database',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    try:
        with db_connection.cursor() as cur:
            cur.execute("SELECT * FROM students")
            data = cur.fetchall()
        return render_template('index.html', students=data)
    except Exception as e:
        flash(f"Error: {str(e)}")
        return render_template('index.html', students=[])

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            with db_connection.cursor() as cur:
                cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
                db_connection.commit()
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == "POST":
        flash("Data Updated Successfully")

        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            with db_connection.cursor() as cur:
                cur.execute("""
                UPDATE students
                SET name=%s, email=%s, phone=%s
                WHERE id=%s
                """, (name, email, phone, id_data))
                db_connection.commit()
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['POST', 'GET'])
def delete(id_data):
    flash("Data Deleted Successfully")

    try:
        with db_connection.cursor() as cur:
            cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
            db_connection.commit()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
