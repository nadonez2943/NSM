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
			session['user_fullname'] = account['user_fullname']
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
    session.pop('user_fullname', None)
    session.pop('user_role', None)
    session.pop('password', None)
    return render_template('login.html')  

# โลทางเลือก
@app.route('/way')
def way():
    if session['user_role']=='user' :
       return redirect('/datamainU')
    elif session['user_role']=='addmin' :
       return redirect('/datamainA')

#โครงการของฉัน
@app.route('/datamain')
def datamain():
    conn = None
    cursor = None
    id = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT projects.pj_id, projects.pj_name , projects.pj_type,projects.pj_budgetYears,mn_role,st_name FROM projects  INNER JOIN process ON ( projects.pj_id = process.pj_id ) INNER JOIN status ON ( process.st_id = status.st_id) INNER JOIN manager ON ( projects.pj_id = manager.pj_id) where user_id = %s ",id)
        row = cursor.fetchall()
        return render_template('home.html', row=row,) 
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

# โครงการที่เกี่ยวข้องของuser
@app.route('/datamainU')
def datamainS():
    conn = None
    cursor = None
    id = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT projects.pj_id, projects.pj_name , projects.pj_type,projects.pj_budgetYears, tbl_role.role_name,st_name FROM projects  INNER JOIN process ON ( projects.pj_id = process.pj_id ) INNER JOIN status ON ( process.st_id = status.st_id) INNER JOIN board ON ( projects.pj_id = board.pj_id) INNER JOIN tbl_role ON ( board.role_id = tbl_role.role_id)  where user_id = %s ",id)
        row = cursor.fetchall()
        return render_template('home_u.html', row=row,) 
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

#โปรเจ็คหน้าหลักเเอดมิน
@app.route('/datamainA')
def datamainA():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT projects.pj_id,projects.pj_refNumber,projects.pj_name,projects.pj_type,projects.pj_amount,pj_budgetYears,st_name FROM projects  INNER JOIN process ON ( projects.pj_id = process.pj_id ) INNER JOIN status ON ( process.st_id = status.st_id)")
        row = cursor.fetchall()
        return render_template('home_a.html', row=row,) 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#ค้นหา
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

# เพิ่มโปรเจค
@app.route('/addproject', methods=['POST'])
def user():
    conn = None
    cursor = None
    try:
        refNumber = request.form['refNumber']
        office = request.form['office']
        divition = request.form['divition']
        type = request.form['radio']
        name = request.form['name']
        amount = request.form['amount']
        detail = request.form['detail']
        financeAmount = request.form['financeAmount']
        budgetSource = request.form['budgetSource']
        budgetYears = request.form['budgetYears']
        if  refNumber and office and divition and type and name and amount and detail and financeAmount and budgetSource and budgetYears and  request.method == 'POST':
            sql = "INSERT INTO projects (pj_refNumber, pj_office, pj_division, pj_type, pj_name, pj_amount, pj_detail, pj_financeAmount, pj_budgetSource, pj_budgetYears) VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
            data = (refNumber,office,divition,type,name,amount,detail,financeAmount,budgetSource,budgetYears,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/runm')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

# ทดลอง
@app.route('/s')
def runm():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT pj_id FROM projects ORDER BY pj_id DESC LIMIT 1")
        rows = cursor.fetchone()
        return render_template("addproject.html", rows=rows) 
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

# @app.route('/runp/<int:id>')
# def runp(id):
#     conn = None
#     cursor = None
#     user = session['user_id']
#     try:
#         sql = "UPDATE manager SET user_id=%s, pj_id=%s"
#         data = data = (id,user)
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute(sql, data)
#         conn.commit()
#         sql = "UPDATE process SET pj_id=%s"
#         data = data = (id)
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute(sql)
#         conn.commit()
#         return redirect('/datamain')
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()  

if __name__ == "__main__":
    app.run(debug=True)