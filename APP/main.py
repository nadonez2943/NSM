import pymysql
from app import app
# from tables import Results ,Results1 ,Results2
from db_config import mysql
from flask import flash, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/')
def new():
    return render_template('login.html')
    
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'user_name' in request.form and 'user_password' in request.form:
		user_name = request.form['user_name']
		user_password = request.form['user_password']
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE user_name = % s AND user_password = % s', (user_name, user_password ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['user_id'] = account['user_id']
			session['user_fname'] = account['user_fname']
			session['user_role'] = account['user_role']
			msg = 'Logged in successfully !'
			return redirect('/datamain')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)  

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('user_fname', None)
    session.pop('user_role', None)
    session.pop('password', None)
    return render_template('login.html')  

@app.route('/datamain')
def datamain():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM  projects")
        row = cursor.fetchall()
        return render_template('home.html', row=row,) 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
