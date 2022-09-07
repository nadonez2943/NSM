import pymysql
from app import app
# from tables import Results ,Results1 ,Results2
from db_config import mysql
from flask import flash, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/')
def new():
    return render_template('login.html')

@app.route('/x')
def x():
    return render_template('addproject.html')
# login   
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
			session['user_fname'] = account['user_fname']
			session['user_role'] = account['user_role']
			return redirect('/way')
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)  
# logout
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_fname', None)
    session.pop('user_role', None)
    session.pop('password', None)
    return render_template('login.html')  

# ไม่เอา
# @app.route('/datamain')
# def datamain():
#     conn = None
#     cursor = None
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM  projects")
#         row = cursor.fetchall()
#         return render_template('home.html', row=row,) 
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()

@app.route('/addproject', methods=['POST'])
def user():
    conn = None
    cursor = None
    try:
        refNumber = request.form['refNumber']
        office = request.form['office']
        divition = request.form['divition']
        type = request.form['radio']
        # projace_m = request.form['projace_m']
        name = request.form['name']
        amount = request.form['amount']
        detail = request.form['detail']
        financeAmount = request.form['financeAmount']
        budgetSource = request.form['budgetSource']
        budgetYears = request.form['budgetYears']
        if  refNumber and office and divition and type and name and amount and detail and financeAmount and budgetSource and budgetYears and  request.method == 'POST':
            sql = "INSERT INTO projects (pj_refNumber, pj_office, pj_division, pj_type, pj_name, pj_amount, pj_detail, pj_financeAmount, pj_budgetSource, pj_budgetYears) VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s)"
            data = (refNumber,office,divition,type,name,amount,detail,financeAmount,budgetSource,budgetYears,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/datamain')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

# โลทางเลือกยังไม่ได้ยัด
@app.route('/way')
def way():
    if session['user_role']=='Boss' :
       return redirect('/datamainM')
    elif session['user_role']=='secretary' :
       return redirect('/datamainS')
    elif session['user_role']=='board' :
       return redirect('/datamainS')
    elif session['user_role']=='addmin' :
       return redirect('/datamainA')
    else :
       return render_template('login.html')

#โปรเจ็คหน้าหลักโปรเจค
@app.route('/datamainM')
def datamainsM():
    conn = None
    cursor = None
    id = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects  INNER JOIN manager ON ( projects.pj_id = manager.pj_id ) INNER JOIN users ON ( manager.user_id = users.user_id) where users.user_id = %s",id)
        row = cursor.fetchall()
        return render_template('home.html', row=row) 
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

# #โปรเจ็คหน้าหลักเลขา
@app.route('/datamainS')
def datamainS():
    conn = None
    cursor = None
    id = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects  INNER JOIN board ON ( projects.pj_id = board.pj_id ) INNER JOIN users ON ( board.user_id = users.user_id) where users.user_id = %s",id)
        row = cursor.fetchall()
        return render_template('home_sec.html', row=row,) 
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

@app.route('/datamainA')
def datamain():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM  projects")
        row = cursor.fetchall()
        return render_template('homeA.html', row=row,) 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/showsearchs' , methods=['POST', 'GET'])
def showsearchs():
    conn = None
    cursor = None
    if request.method == 'POST':
        key = request.form['search']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "SELECT * FROM projects WHERE pj_refNumber = '%s' OR pj_name = '%s' OR pj_budgetYears = '%s' OR pj_type = '%s'" % (key,key,key,key)
            sql = sql.encode('utf-8')
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return render_template("showsearch.html", rows=rows)
            except:
                cursor.rollback()
                print('ผิดพลาด')
        except Exception as e:
            print(e)

if __name__ == "__main__":
    app.run(debug=True)