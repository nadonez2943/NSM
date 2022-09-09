from flask import Flask, render_template, request, redirect, url_for, session
from db_config import mysql
from app import app
import pymysql

@app.route('/home')
def home():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id INNER JOIN nsm_project.status ON nsm_project.process.st_id = nsm_project.status.st_id INNER JOIN nsm_project.events ON nsm_project.process.ev_id = nsm_project.events.ev_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id INNER JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id ")
        row = cursor.fetchall()
        cursor.execute("SELECT financial_amount FROM nsm_project.process")
        rows = cursor.fetchall()
        return render_template('home.html', row=row , rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
# @app.route('/home')
# def datamainS():
#     conn = None
#     cursor = None
#     id = session['user_id']
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM projects  INNER JOIN board ON ( projects.pj_id = board.pj_id ) INNER JOIN users ON ( board.user_id = users.user_id) where users.user_id = %s",id)
#         row = cursor.fetchall()
#         return render_template('home.html', row=row,) 
#     except Exception as e:
#         print(e)
#     finally: 
#         cursor.close()
#         conn.close()
 
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/draft/<int:id>', methods=[ 'GET'])
def draft(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status ON nsm_project.process.st_id = nsm_project.status.st_id LEFT JOIN nsm_project.events ON nsm_project.process.ev_id = nsm_project.events.ev_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id order by nsm_project.tbl_role.role_id")
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id")
        rows = cursor.fetchall()
        if rows:
            return render_template('draft.html', row=row , rows=rows ,id=id)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/consider')
def consider():
    return render_template('consider.html')

@app.route('/examine')
def examine():
    return render_template('examine.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/addevent')
def addevent():
    return render_template('addevent.html')

@app.route('/editevent')
def editevent():
    return render_template('editevent.html')

@app.route('/t')
def h():
    return render_template('test.html')

@app.route('/countdown')
def countdown():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT endproject_DateTime FROM nsm_project.process;")
        rows = cursor.fetchall()
        return render_template('home.html', rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/addproject')
def addproject():
    return render_template('addproject.html')

@app.route('/addboard')
def addboard():
    return render_template('addboard.html')

@app.route('/กรรมการ')
def k():
    return render_template('กรรมการ.html')

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'user_name' in request.form and 'user_password' in request.form:
		user_name = request.form['user_name']
		user_password = request.form['user_password']
		cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE user_name = % s AND user_password = % s', (user_name, user_password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['user_id'] = account['user_id']
			session['user_name'] = account['user_name']
			session['user_fullname'] = account['user_fullname']
			msg = 'Logged in successfully !'
			return redirect('/home')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('user_id', None)
	session.pop('user_name', None)
	session.pop('user_fullname', None)
	return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
