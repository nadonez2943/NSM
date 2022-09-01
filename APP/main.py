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
			session['user_name'] = account['user_name']
			session['user_role'] = account['user_role']
			msg = 'Logged in successfully !'
			return render_template('home.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)  

@app.route('/add', methods=['POST'])
def user():
    conn = None
    cursor = None
    try:
        first_name = request.form['inputfirst_name']
        last_name = request.form['inputlast_name']
        gender = request.form['inputgender']
        lavel = request.form['inputlavel']
        password = request.form['inputpassword']
# validate the received values
        if  first_name and last_name and gender and lavel and password and request.method == 'POST':
#do not save password as a plain text
            _hashed_password = generate_password_hash(password)
# save edits
            sql = "INSERT INTO user (first_name, last_name, gender, lavel, password) VALUES(%s, %s, %s, %s, %s)"
            data = (first_name,last_name,gender,lavel,password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User added successfully!')
            return redirect('/login')
        else:
            return 'Error while adding user'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
