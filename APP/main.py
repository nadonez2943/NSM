import pymysql
from app import app
from flask import Flask, render_template, request, redirect, url_for, session
from db_config import mysql
from werkzeug.security import generate_password_hash, check_password_hash

#******** รหัสเข้าเครื่องเหมือนดาต้าเบส**********
#หน้าแรก
@app.route('/')
def log():
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
			session['user_fullname'] = account['user_fullname']
			session['user_role'] = account['user_role']
			if session['user_role']=='user' : #ทางเลือกถ้าเป็นยูส
				return redirect('/homeuse')
			elif session['user_role']=='addmin' : #ทางเลือกถ้าเป็นadd
				return redirect('/homeadd')
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

# # โลทางเลือก ลบเลยก็ได้นะแก้ย้ายไปอยู่กับข้างบนละ
# @app.route('/way')
# def way():
#     if session['user_role']=='user' : 
#        return redirect('/homeuse')
#     elif session['user_role']=='addmin' :
#        return redirect('/homeadd')

#หน้าหลักแอด *แก้เอาของอามมาใส่ก็ได้แต่แก้ select left join โค๊ดตารางให้ฐานข้อมูลให้มันตรงกับเพื่อนหน่อย แต่หน้านี้มันออกนะ ข้อมูลออกทุกอันเลย แต่พอใส่เลขข้างหน้ามันจะกดดูหน้าโปรเจคไม่ได้เลยยังไม่ใส่
@app.route('/homeadd')
def homeadd():
    conn = None
    cursor = None
    id = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id INNER JOIN nsm_project.status ON nsm_project.process.st_id = nsm_project.status.st_id INNER JOIN nsm_project.events ON nsm_project.process.ev_id = nsm_project.events.ev_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id INNER JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id")
        row = cursor.fetchall()
        cursor.execute("SELECT user_id FROM nsm_project.users where user_id = %s",id) #แก้บรรทัดนี้ใหม่ด้วยแค่ลองเฉยๆ
        rows = cursor.fetchall()         
        return render_template('homeadd.html', row=row,rows=rows )
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

#หน้าหลักuser เหมียนกับข้างบนเลย แต่ข้อมูลไม่ออกสักอันตารางโล่งๆ
@app.route('/homeuse')
def homeuse():
    conn = None
    cursor = None
    id = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id INNER JOIN nsm_project.status ON nsm_project.process.st_id = nsm_project.status.st_id INNER JOIN nsm_project.events ON nsm_project.process.ev_id = nsm_project.events.ev_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id INNER JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id")
        row = cursor.fetchall()
        cursor.execute("SELECT user_id FROM nsm_project.users where user_id = %s",id)
        rows = cursor.fetchall()   
        return render_template('homeuse.html', row=row,rows=rows )
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()       

#ค้นหา *ยังไม่ได้ลอง
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

@app.route('/addproject',methods=['GET'])
def addproject():
    return render_template('addproject.html')

# เพิ่มโปรเจคแต่ยังเก็บผู้รับผิดชอบไม่ได้ ตอนกดมันไม่ส่งไปเก็บในฐานข้อมูล***เพราะยังไม่ได้ทำ :( 
@app.route('/addproject', methods=['POST'])
def addprojects():
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
            return redirect('/homeuse')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#หน้าข้อมูลโปรเจค อันนี้กดแล้วไม่ไป ต้องใส่เลขถึงจะขึ้น ToT
@app.route('/project/<int:id>', methods=[ 'GET'])
def project(id):
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
            return render_template('project.html', row=row , rows=rows , id=id )
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# หน้าร่าง เหมือนข้างล่าง ไปดูของฟิวก็ได้
@app.route('/project/<int:id>/draft', methods=[ 'GET'])
def draft(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status ON nsm_project.process.st_id = nsm_project.status.st_id LEFT JOIN nsm_project.events ON nsm_project.process.ev_id = nsm_project.events.ev_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = 2 order by nsm_project.tbl_role.role_id")
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
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

# หน้า พิจารณาผล ยังไม่ลอง ยังติดอยู่อีหน้า Home ตารางไม่ออกกดอะไรไม่ได้
@app.route('/project/<int:id>/consider', methods=[ 'GET'])
def consider(id):
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
            return render_template('consider.html', row=row , rows=rows ,id=id)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# หน้า examine เหมือนข้างบน
@app.route('/project/<int:id>/examine', methods=[ 'GET'])
def examine(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status ON nsm_project.process.st_id = nsm_project.status.st_id LEFT JOIN nsm_project.events ON nsm_project.process.ev_id = nsm_project.events.ev_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id order by nsm_project.tbl_role.role_id")
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id ")
        rows = cursor.fetchall()
        if rows:
            return render_template('examine.html', row=row , rows=rows ,id=id)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()   

if __name__ == "__main__":
    app.run(debug=True)
