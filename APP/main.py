from pickle import TRUE
from flask import Flask, render_template, request, redirect, url_for, session
from db_config import mysql
from app import app
import pymysql
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

ALLOWED_EXTENSIONS = {'doc', 'pdf'}

# log in
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

#log out
@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('user_id', None)
	session.pop('user_name', None)
	session.pop('user_fullname', None)
	return redirect(url_for('login'))

#หน้าหลัก
@app.route('/home')
def home():
    a=session['user_id']
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        row = cursor.fetchall()
        return render_template('home.html', row=row )
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#โครงการของฉัน
@app.route('/myproject')
def myproject():
    m=session['user_id']
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.manager.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(m))
        row = cursor.fetchall()
        cursor.execute("SELECT financial_amount FROM nsm_project.process")
        rows = cursor.fetchall()
        return render_template('home.html', row=row , rows=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
 #หน้าโครงการ
@app.route('/project/<int:id>', methods=[ 'GET'])
def project(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x,DATE_FORMAT(startproject_date, %s) as startdate FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id WHERE nsm_project.projects.pj_id = %s", (format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,id))
        ev = cursor.fetchall()
        if rows:
            return render_template('project.html', row=row , rows=rows , id=id ,ev=ev)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
#หน้าร่างโครงการ
@app.route('/project/<int:id>/draft', methods=[ 'GET'])
def draft(id):
    conn = None
    cursor = None
    phase = '1'
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,DATE_FORMAT(startproject_date, %s) as startdate FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.board.role_id", (format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,id))
        ev = cursor.fetchall()
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role']) :
                return render_template('draft.html', row=row , rows=rows ,id=id ,ev=ev)
        if(phase == role['bo_phase'] ):
            if (assistant == role['role']) :
                return render_template('draft.html', row=row , rows=rows ,id=id ,ev=ev)
            elif (board ==  role['role']) :
                return render_template('draftB.html', row=row , rows=rows ,id=id ,ev=ev)
        else:
            return render_template('inept.html', row=row , rows=rows ,id=id ,ev=ev)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#หน้าพิจารณาโครงการ
@app.route('/project/<int:id>/consider', methods=[ 'GET'])
def consider(id):
    conn = None
    cursor = None
    phase = '2'
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,DATE_FORMAT(startproject_date, %s) as startdate FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.board.role_id", (format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,id))
        ev = cursor.fetchall()
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role']) :
                return render_template('consider.html', row=row , rows=rows ,id=id ,ev=ev)
        elif(phase == role['bo_phase'] ):
            if (assistant == role['role']) :
                return render_template('consider.html', row=row , rows=rows ,id=id ,ev=ev)
            elif (board ==  role['role']) :
                return render_template('considerB.html', row=row , rows=rows ,id=id ,ev=ev)
        else:
            return render_template('inept.html', row=row , rows=rows ,id=id ,ev=ev)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#หน้าตรวจสอบโครงการ
@app.route('/project/<int:id>/examine', methods=[ 'GET'])
def examine(id):
    conn = None
    cursor = None
    phase = '3'
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,DATE_FORMAT(startproject_date, %s) as startdate,DATE_FORMAT(contt_date, %s) as conttdate,DATE_FORMAT(contt_start, %s) as conttstart,DATE_FORMAT(contt_end, %s) as conttend FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.tbl_role.role_id", (format,format,format,format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(ins_date, %s) as insdate FROM nsm_project.projects LEFT JOIN nsm_project.disburse ON nsm_project.projects.pj_id = nsm_project.disburse.pj_id WHERE nsm_project.projects.pj_id = %s order by ins_no desc", (format,id))
        dis = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,id))
        ev = cursor.fetchall()
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role']) :
                return render_template('examine.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis)
        elif(phase == role['bo_phase'] ):
            if (assistant == role['role']) :
                return render_template('examine.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis)
            elif (board ==  role['role']) :
                return render_template('examineB.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis)
        else:
            return render_template('inept.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#หน้าเพิ่มคณะกรรมการ
@app.route('/project/<int:id>/addboard',methods=[ 'GET'])
def addboard_get(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.users ")
        row = cursor.fetchall()
        if row:
            return render_template('addboard.html', row=row ,id=id,)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#หน้ากิจกรรม
@app.route('/project/<int:id>/draftEvent', methods=[ 'GET'])
def draftevent(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.events.ev_id) as row_num,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s", (format,id))
        row = cursor.fetchall()
        if row:
            return render_template('draftEvent.html', row=row , id=id)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/project/<int:id>/considerEvent', methods=[ 'GET'])
def considerEvent(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.events.ev_id) as row_num,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 2 WHERE nsm_project.projects.pj_id = %s", (format,id))
        row = cursor.fetchall()
        if row:
            return render_template('considerEvent.html', row=row , id=id)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/project/<int:id>/examineEvent', methods=[ 'GET'])
def examineEvent(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%d/%m/%Y'
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.events.ev_id) as row_num,DATE_FORMAT(ev_date, %s) as evdate FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 3 WHERE nsm_project.projects.pj_id = %s", (format,id))
        row = cursor.fetchall()
        if row:
            return render_template('examineEvent.html', row=row , id=id)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#หน้าเพิ่มกิจกรรม
@app.route('/project/<int:id>/addeventd', methods=[ 'GET'])
def addeventd(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects WHERE nsm_project.projects.pj_id = %s", id)
    row = cursor.fetchall()
    return render_template('addeventd.html', id=id,row=row)

@app.route('/addeventd', methods=[ 'POST'])
def addeventd2():
    conn = None
    cursor = None
    try:
        ev_name = request.form['evname']
        ev_detail = request.form['evdetail']
        ev_date = request.form['evdate']
        ev_phase = request.form['evphase']
        pj_id = request.form['pjid']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO events(ev_name, ev_detail, ev_date, ev_phase, pj_id) VALUES(%s, %s, %s, %s, %s)"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/project/'+pj_id+'/draftEvent')
        else:
            return 'ไม่สามารถเพิ่มกิจกรรมได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/project/<int:id>/addeventc', methods=[ 'GET'])
def addeventc(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects WHERE nsm_project.projects.pj_id = %s", id)
    row = cursor.fetchall()
    return render_template('addeventc.html', id=id,row=row)

@app.route('/addeventc', methods=[ 'POST'])
def addeventc2():
    conn = None
    cursor = None
    try:
        ev_name = request.form['evname']
        ev_detail = request.form['evdetail']
        ev_date = request.form['evdate']
        ev_phase = request.form['evphase']
        pj_id = request.form['pjid']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO events(ev_name, ev_detail, ev_date, ev_phase, pj_id) VALUES(%s, %s, %s, %s, %s)"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/project/'+pj_id+'/considerEvent')
        else:
            return 'ไม่สามารถเพิ่มกิจกรรมได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/project/<int:id>/addevente', methods=[ 'GET'])
def addevente(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects WHERE nsm_project.projects.pj_id = %s", id)
    row = cursor.fetchall()
    return render_template('addevente.html', id=id,row=row)

@app.route('/addevente', methods=[ 'POST'])
def addevente2():
    conn = None
    cursor = None
    try:
        ev_name = request.form['evname']
        ev_detail = request.form['evdetail']
        ev_date = request.form['evdate']
        ev_phase = request.form['evphase']
        pj_id = request.form['pjid']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO events(ev_name, ev_detail, ev_date, ev_phase, pj_id) VALUES(%s, %s, %s, %s, %s)"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/project/'+pj_id+'/examineEvent')
        else:
            return 'ไม่สามารถเพิ่มกิจกรรมได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#หน้าแก้ไขกิจกรรม
@app.route('/project/<int:id>/editevent/<int:idd>')
def editevent(id,idd):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id WHERE nsm_project.projects.pj_id = %s AND nsm_project.events.ev_id = %s", (id,idd))
    row = cursor.fetchall()
    return render_template('editevent.html', id=id,row=row)

@app.route('/editevent', methods=[ 'POST'])
def editevent2():
    conn = None
    cursor = None
    try:
        ev_name = request.form['evname']
        ev_detail = request.form['evdetail']
        ev_date = request.form['evdate']
        ev_phase = request.form['evphase']
        pj_id = request.form['pjid']
        ev_id = request.form['evid']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and ev_id and request.method == 'POST':
# save edits
            sql = "UPDATE events SET ev_name=%s, ev_detail=%s, ev_date=%s, ev_phase=%s WHERE pj_id=%s AND ev_id=%s"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id,ev_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            if ev_phase == '1':
                return redirect('/project/'+pj_id+'/draftEvent')
            elif ev_phase == '2':
                return redirect('/project/'+pj_id+'/considerEvent')
            elif ev_phase == '3':
                return redirect('/project/'+pj_id+'/examineEvent')
        else:
            return 'ไม่สามารถแก้ไขกิจกรรมได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#หน้าทดสอบการนับถอยหลัง
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

#หน้าเพิ่มโครงการ
# เพิ่มโปรเจค
@app.route('/addproject', methods=['POST'])
def user():
    conn = None
    cursor = None
    try:
        id = request.form['id']
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
            return redirect('/runp/'+id)
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

# ก่อนเอาไอดีpjไปเก็บ
@app.route('/addNewProject')
def addNewProject():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT pj_id FROM projects ORDER BY pj_id DESC LIMIT 1")
        rows = cursor.fetchone()
        id = rows 
        print(id)
        return render_template("addproject.html", rows=rows) 
    except Exception as e:
        print(e)
    finally: 
        cursor.close()
        conn.close()

# เอาไอดี pj ไปเก็บ manager กับ process
@app.route('/runp/<int:id>')
def runp(id):
    conn = None
    cursor = None
    x = id+1
    user = session['user_id']
    try:
        sql = "INSERT INTO manager (user_id, pj_id) VALUES(%s, %s)"
        data = (user,x)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        sql = "INSERT INTO process (pj_id) VALUES(%s)"
        data2 = (x)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data2)
        conn.commit()
        return redirect('/home')
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()  

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#อัพเอกสาร
@app.route('/project/<int:id>/doc', methods=['GET',"POST"])
def doc(id):
    form = UploadFileForm()
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.path")
    row = cursor.fetchall()
    if form.validate_on_submit():
       
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        sql = "INSERT INTO path(path_path) VALUES(%s)"
        data = secure_filename(file.filename)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return "File has been uploaded."
    return render_template('doc.html', row=row,form=form,id=id)

#ทดสอบ


@app.route('/t', methods=['GET',"POST"])
def test():
    form = UploadFileForm()
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.path")
    row = cursor.fetchall()
    if form.validate_on_submit():
       
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        sql = "INSERT INTO path(path_path) VALUES(%s)"
        data = secure_filename(file.filename)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return "File has been uploaded."
    return render_template('test.html', row=row,form=form)


if __name__ == "__main__":
    app.run(debug=True)
