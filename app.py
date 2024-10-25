from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)

app.secret_key = 'flash message'

# Cấu hình kết nối MySQL
app.config['MYSQL_HOST'] = 'flaskapp-server.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'gnhtcebvax'  
app.config['MYSQL_PASSWORD'] = 'CJcTF25jDk$W9wk8'  
app.config['MYSQL_DB'] = 'flaskapp_database'

def create_database_and_table():
    # Kết nối đến MySQL mà không chỉ định cơ sở dữ liệu
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD']
    )
    
    try:
        with connection.cursor() as cursor:
            # Thực thi các câu lệnh SQL từ tệp
            with open('create_database.sql', 'r') as f:
                sql_script = f.read()
                cursor.execute(sql_script)
        connection.commit()
    finally:
        connection.close()

# Tạo cơ sở dữ liệu và bảng khi khởi động ứng dụng
create_database_and_table()

@app.route('/')
def index():
    # Kết nối đến cơ sở dữ liệu và truy vấn dữ liệu
    db_connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with db_connection.cursor() as cur:
            cur.execute("SELECT * FROM students")
            data = cur.fetchall()
        return render_template('index.html', students=data)
    except Exception as e:
        flash(f"Error: {str(e)}")
        return render_template('index.html', students=[])
    finally:
        db_connection.close()

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        db_connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with db_connection.cursor() as cur:
                cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
                db_connection.commit()
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('index'))
        finally:
            db_connection.close()

@app.route('/update', methods=['POST'])
def update():
    if request.method == "POST":
        flash("Data Updated Successfully")

        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        db_connection = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

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
        finally:
            db_connection.close()

@app.route('/delete/<string:id_data>', methods=['POST'])
def delete(id_data):
    flash("Data Deleted Successfully")

    db_connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with db_connection.cursor() as cur:
            cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
            db_connection.commit()
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error: {str(e)}")
        return redirect(url_for('index'))
    finally:
        db_connection.close()

if __name__ == "__main__":
    app.run(debug=True)
