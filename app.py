from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash message'

# Cấu hình kết nối MySQL
db_connection = pymysql.connect(
    host='flaskapp-server.mysql.database.azure.com',
    user='gnhtcebvax',
    password='CJcTF25jDk$W9wk8',
    db='flaskapp_database',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def create_database_and_table():
    # Connect to MySQL without specifying a database
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD']
    )
    
    try:
        with connection.cursor() as cursor:
            # Execute SQL commands from the file
            with open('create_database.sql', 'r') as f:
                sql_script = f.read()
                cursor.execute(sql_script)
        connection.commit()
    finally:
        connection.close()

# Create database and table when starting the application
create_database_and_table()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        flash("Data Updated Successfully")

        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students
        SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['POST'])
def delete(id_data):
    flash("Data Deleted Successfully")

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
