from asyncio.log import logger
from asyncio.windows_events import NULL
from pickle import TRUE
# from ssl import AlertDescription
# from click import confirm
from flask import Flask,render_template, request, redirect, url_for, session,flash,jsonify
from db_config import mysql
from app import app
import pymysql
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from datetime import date,datetime

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
            session['user_role'] = account['user_role']
            if session['user_role']=="user":
                return redirect('/home')
            elif session['user_role']=="admin":
                return redirect('/admin')
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
    session.pop('user_role', None)
    return redirect(url_for('login'))

#หน้าหลัก
@app.route('/home')
def home():
    if session['user_role']=="user":
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.manager.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",session['user_id'])
            MN = cursor.fetchall()
            cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",session['user_id'])
            BO = cursor.fetchall()
            cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 1 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",session['user_id'])
            DR = cursor.fetchall()
            cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 2 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",session['user_id'])
            CO = cursor.fetchall()
            cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 3 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",session['user_id'])
            EX = cursor.fetchall()
            return render_template('home.html', BO=BO,MN=MN,DR=DR,CO=CO,EX=EX )
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()
    else:
        return render_template('inept.html')
        
 #หน้าโครงการ
@app.route('/project/<int:id>', methods=[ 'GET'])
def project(id):
    conn = None
    cursor = None
    user = session['user_id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%e %b %Y'
        tformat = '%H:%i'
        cursor.execute("SET lc_time_names = 'th_TH'")
        cursor.execute("SELECT *,DATEDIFF(ADDDATE(nsm_project.process.conapp_date, INTERVAL 7 DAY),date(now())) AS condiff,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x,DATE_FORMAT(DATE_ADD(startproject_date , INTERVAL 543 YEAR ), %s) as startdate, FORMAT(pj_amount, 0) as pjamount FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id WHERE nsm_project.projects.pj_id = %s", (format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,tformat,id))
        ev = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(pac_date , INTERVAL 543 YEAR ), %s) as pacdate FROM nsm_project.pacel RIGHT JOIN nsm_project.projects ON nsm_project.projects.pj_id = nsm_project.pacel.pj_id WHERE nsm_project.projects.pj_id=%s ORDER BY pac_id DESC",(format,id))
        pac = cursor.fetchall()
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        return render_template('project.html', row=row , rows=rows , id=id , ev=ev, pac=pac,role=role,user_role=session['user_role'])
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
@app.route('/project/<int:id>/conauto', methods=['GET','POST'])
def conauto(id):
    conn = None
    cursor = None
    try:
        stcon_id = 7
        conapp_status = 'yes'
        conPMcheck = 'yes'
        sql = "UPDATE process SET stcon_id=%s,conapp_status=%s,conPMcheck=%s WHERE pj_id=%s"
        data = (stcon_id,conapp_status,conPMcheck, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id))
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close() 

#หน้าร่างโครงการ

@app.route('/project/<int:id>/draft', methods=[ 'GET'])
def draft(id):
    if session['user_role']=="user":
        conn = None
        cursor = None
        phase = 1
        user = session['user_id']
        manager = 'manager'
        assistant = 'assistant'
        board = 'board'
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            format = '%e %b %Y'
            tformat = '%H:%i'
            cursor.execute("SET lc_time_names = 'th_TH'")
            cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(startproject_date , INTERVAL 543 YEAR ), %s) as startdate, FORMAT(pj_amount, 0) as pjamount FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 1 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.board.role_id", (format,id))
            row = cursor.fetchall()
            cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
            rows = cursor.fetchall()
            cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,tformat,id))
            ev = cursor.fetchall()
            cursor.execute("SELECT nsm_project.process.start_draft,DATE_FORMAT(DATE_ADD(start_draft , INTERVAL 543 YEAR ), %s) as startdate,DATE_FORMAT(DATE_ADD(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY), INTERVAL 543 YEAR ), %s) AS endproject_date,DATEDIFF(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY),date(now())) AS diff FROM nsm_project.process WHERE nsm_project.process.pj_id = %s", (format,format,id))
            diff = cursor.fetchall()
            cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
            role = cursor.fetchone()
            if (manager ==  role['role']) :
                    return render_template('draft.html', row=row , rows=rows ,id=id ,ev=ev,diff=diff,role=role)
            elif(phase == role['bo_phase'] and manager !=  role['role']):
                if (assistant == role['role']) :
                    return render_template('draft.html', row=row , rows=rows ,id=id ,ev=ev,diff=diff,role=role)
                elif (board ==  role['role']) :
                    return render_template('draftB.html', row=row , rows=rows ,id=id ,ev=ev,diff=diff)
            else:
                return render_template('inept.html', row=row , rows=rows ,id=id )
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    else:
        conn = None
        cursor = None
        phase = 1
        manager = 'manager'
        assistant = 'assistant'
        board = 'board'
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            format = '%e %b %Y'
            tformat = '%H:%i'
            cursor.execute("SET lc_time_names = 'th_TH'")
            cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(startproject_date , INTERVAL 543 YEAR ), %s) as startdate, FORMAT(pj_amount, 0) as pjamount FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 1 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.board.role_id", (format,id))
            row = cursor.fetchall()
            cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
            rows = cursor.fetchall()
            cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,tformat,id))
            ev = cursor.fetchall()
            cursor.execute("SELECT nsm_project.process.start_draft,DATE_FORMAT(DATE_ADD(start_draft , INTERVAL 543 YEAR ), %s) as startdate,DATE_FORMAT(DATE_ADD(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY), INTERVAL 543 YEAR ), %s) AS endproject_date,DATEDIFF(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY),date(now())) AS diff FROM nsm_project.process WHERE nsm_project.process.pj_id = %s", (format,format,id))
            diff = cursor.fetchall()
            return render_template('draftB.html', row=row , rows=rows ,id=id ,ev=ev,diff=diff)
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
    phase = 2
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%e %b %Y'
        tformat = '%H:%i'
        cursor.execute("SET lc_time_names = 'th_TH'")
        cursor.execute("SELECT *,DATEDIFF(ADDDATE(nsm_project.process.conapp_date, INTERVAL 7 DAY),date(now())) AS condiff,DATEDIFF(nsm_project.process.winner_date ,date(now())) AS windiff,DATE_FORMAT(DATE_ADD(startproject_date , INTERVAL 543 YEAR ), %s) as startdate,DATE_FORMAT(DATE_ADD(contt_date , INTERVAL 543 YEAR ), %s) as conttdate, FORMAT(pj_amount, 0) as pjamount FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 2 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.board.role_id", (format,format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 2 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,tformat,id))
        ev = cursor.fetchall()
        std = row[0]['stdraft_id']
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role']) :
            if (std == 5) :
                return render_template('consider.html', row=row , rows=rows ,id=id ,ev=ev,role=role)
            elif (std < 5) :
                    return render_template('errorcon.html')
        elif(phase == role['bo_phase'] ):
            if (assistant == role['role']) :
                return render_template('consider.html', row=row , rows=rows ,id=id ,ev=ev,role=role)
            elif (board ==  role['role']) :
                return render_template('considerB.html', row=row , rows=rows ,id=id ,ev=ev,role=role)
        else:
            return render_template('inept.html', row=row , rows=rows ,id=id ,ev=ev)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/project/<int:id>/considerauto', methods=['GET','POST'])
def considerauto(id):
    conn = None
    cursor = None
    try:
        stcon_id = 7
        conapp_status = 'yes'
        conPMcheck = 'yes'
        sql = "UPDATE process SET stcon_id=%s,conapp_status=%s,conPMcheck=%s WHERE pj_id=%s"
        data = (stcon_id,conapp_status,conPMcheck, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id)+'/consider')
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
    phase = 3
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%e %b %Y'
        tformat = '%H:%i'
        cursor.execute("SET lc_time_names = 'th_TH'")
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(contt_date , INTERVAL 543 YEAR ), %s) as conttdate FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 3 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.tbl_role.role_id", (format,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(check_date , INTERVAL 543 YEAR ), %s) as checkdate,cast(((ins_amount/contt_fin)*100) as decimal(11, 2)) as ff FROM nsm_project.projects LEFT JOIN nsm_project.checks ON nsm_project.projects.pj_id = nsm_project.checks.pj_id  LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id WHERE nsm_project.projects.pj_id = %s order by ins_no  ", (format,id))
        dis = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 3 WHERE nsm_project.projects.pj_id = %s order by nsm_project.events.ev_id desc",(format,tformat,id))
        ev = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ins_date , INTERVAL 543 YEAR ), %s) as checkdate,DATEDIFF(ins_date,date(now())) AS daten FROM nsm_project.projects LEFT JOIN nsm_project.checks ON nsm_project.projects.pj_id = nsm_project.checks.pj_id   WHERE nsm_project.projects.pj_id = %s and  nsm_project.checks.ins_no = 1 ",(format,id))
        one = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ins_date , INTERVAL 543 YEAR ), %s) as checkdate,DATEDIFF(ins_date,date(now())) AS daten FROM nsm_project.projects LEFT JOIN nsm_project.checks ON nsm_project.projects.pj_id = nsm_project.checks.pj_id   WHERE nsm_project.projects.pj_id = %s and  nsm_project.checks.ins_no = 2 ",(format,id))
        two = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(ins_date , INTERVAL 543 YEAR ), %s) as checkdate,DATEDIFF(ins_date,date(now())) AS daten FROM nsm_project.projects LEFT JOIN nsm_project.checks ON nsm_project.projects.pj_id = nsm_project.checks.pj_id   WHERE nsm_project.projects.pj_id = %s and  nsm_project.checks.ins_no = 3 ",(format,id))
        three = cursor.fetchall()
        stc = row[0]['stcon_id']
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role']) :
                if (stc == 7) :
                    return render_template('examine.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis, role=role, one=one, two=two, three=three)
                elif (stc < 7) :
                    return render_template('errorex.html')
        elif(phase == role['bo_phase'] ):
            if (assistant == role['role']) :
                return render_template('examine.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis, role=role, one=one, two=two, three=three)
            elif (board ==  role['role']) :
                return render_template('examineB.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis,role=role, one=one, two=two, three=three)
        else:
            return render_template('inept.html', row=row , rows=rows ,id=id ,ev=ev,dis=dis,role=role)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#ยุติโครงการ
@app.route('/project/<int:id>/closeProject', methods=[ 'POST'])
def closeProject(id):
    conn = None
    cursor = None
    try:
        pj_status = 'closed'
        sql = "UPDATE projects SET pj_status=%s WHERE pj_id=%s"
        data = (pj_status, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id))
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close() 

@app.route('/project/<int:id>/conclosed', methods=['GET','POST'])
def conclosed(id):
    conn = None
    cursor = None
    try:
        pj_status = 'closed'
        if pj_status and request.method == 'POST':
            sql = "UPDATE projects SET pj_status=%s WHERE pj_id=%s"
            data = (pj_status, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
        return redirect('/project/'+str(id)+'/consider')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#PMเพิ่มคณะกรรมการ
@app.route('/project/<int:id>/PMad', methods=[ 'POST'])
def PMad(id):
    conn = None
    cursor = None
    try:
        stdraft_id = 2
        if stdraft_id and request.method == 'POST':
            sql = "UPDATE process SET stdraft_id=%s WHERE pj_id=%s"
            data = (stdraft_id, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
        return redirect('/project/'+str(id)+'/draft')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close() 

@app.route('/project/<int:id>/PMac', methods=[ 'POST'])
def PMac(id):
    conn = None
    cursor = None
    try:
        stcon_id = 2
        if stcon_id and request.method == 'POST':
            sql = "UPDATE process SET stcon_id=%s WHERE pj_id=%s"
            data = (stcon_id, id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
        return redirect('/project/'+str(id)+'/consider')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close() 

#หน้าแก้ไขคณะกรรมการ
@app.route('/project/<int:id>/addboardd',methods=[ 'GET'])
def addboardd(id):
    conn = None
    cursor = None
    phase = 1
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 1 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.office ON nsm_project.users.of_id = nsm_project.office.of_id LEFT JOIN nsm_project.division ON nsm_project.users.dv_id = nsm_project.division.dv_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.tbl_role.role_id", id)
    row = cursor.fetchall()
    cursor.execute("SELECT * FROM (SELECT nsm_project.users.user_id,nsm_project.users.user_fullname,nsm_project.division.dv_shname FROM nsm_project.users LEFT JOIN nsm_project.division ON nsm_project.users.dv_id = nsm_project.division.dv_id) as a LEFT JOIN (SELECT nsm_project.board.user_id FROM nsm_project.projects LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 1 LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ) as b ON a.user_id = b.user_id where (CASE when b.user_id = a.user_id then 0 else a.user_id end) != 0 ", id)
    rows = cursor.fetchall()
    cursor.execute("SELECT count(case when nsm_project.board.role_id = '1' then 1 end) as cmng ,count(case when nsm_project.board.role_id = '2' then 1 end) as cboa,count(case when nsm_project.board.role_id = '3' then 1 end) as cas FROM  nsm_project.board WHERE nsm_project.board.pj_id = %s AND nsm_project.board.bo_phase=1", id)
    crole = cursor.fetchall()
    cursor.execute("SELECT * FROM nsm_project.process WHERE nsm_project.process.pj_id=%s", id)
    status = cursor.fetchall()
    std = int(status[0]['stdraft_id'])
    cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
    role = cursor.fetchone()
    if (manager ==  role['role'] and std == 1 ) :
            return render_template('PMad.html', id=id,row=row,rows=rows,crole=crole)
    elif (manager ==  role['role'] and std > 1 ) :
            return render_template('inept.html', id=id,row=row,rows=rows,crole=crole)        
    if(phase == role['bo_phase'] ):
        if (assistant == role['role']) :
            return render_template('addboardd.html', id=id,row=row,rows=rows,crole=crole)
    else:
        return render_template('inept.html', row=row , rows=rows ,id=id )

@app.route('/addboardd', methods=[ 'POST'])
def addboardd2():
    conn = None
    cursor = None
    try:
        user_id = request.form['userid']
        role_id = request.form['roleid']
        bo_phase = request.form['bophase']
        pj_id = request.form['pjid']
# validate the received values
        if user_id and role_id and bo_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO board(user_id, role_id, bo_phase, pj_id) VALUES(%s, %s, %s, %s)"
            data = (user_id, role_id, bo_phase, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('เพิ่มรายชื่อสำเร็จ')
            return redirect('/project/'+pj_id+'/addboardd')
        else:
            return 'ไม่สามารถเพิ่มได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/project/<int:id>/addboardc',methods=[ 'GET'])
def addboardc(id):
    conn = None
    cursor = None
    phase = 2
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 2 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.office ON nsm_project.users.of_id = nsm_project.office.of_id LEFT JOIN nsm_project.division ON nsm_project.users.dv_id = nsm_project.division.dv_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.tbl_role.role_id", id)
    row = cursor.fetchall()
    cursor.execute("SELECT * FROM (SELECT nsm_project.users.user_id,nsm_project.users.user_fullname,nsm_project.division.dv_shname FROM nsm_project.users LEFT JOIN nsm_project.division ON nsm_project.users.dv_id = nsm_project.division.dv_id) as a LEFT JOIN (SELECT nsm_project.board.user_id FROM nsm_project.projects LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 2 LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ) as b ON a.user_id = b.user_id where (CASE when b.user_id = a.user_id then 0 else a.user_id end) != 0 ", id)
    rows = cursor.fetchall()
    cursor.execute("SELECT count(case when nsm_project.board.role_id = '1' then 1 end) as cmng ,count(case when nsm_project.board.role_id = '2' then 1 end) as cboa,count(case when nsm_project.board.role_id = '3' then 1 end) as cas FROM  nsm_project.board WHERE nsm_project.board.pj_id = %s AND nsm_project.board.bo_phase=2", id)
    crole = cursor.fetchall()
    cursor.execute("SELECT * FROM nsm_project.process WHERE nsm_project.process.pj_id=%s", id)
    status = cursor.fetchall()
    stc = int(status[0]['stcon_id'])
    cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
    role = cursor.fetchone()
    if (manager ==  role['role'] and stc == 1 ) :
            return render_template('PMac.html', id=id,row=row,rows=rows,crole=crole)
    elif (manager ==  role['role'] and stc > 1 ) :
            return render_template('inept.html', id=id,row=row,rows=rows,crole=crole)           
    if (assistant == role['role'] and stc > 1 and phase == role['bo_phase'] ) :
            return render_template('addboardc.html', id=id,row=row,rows=rows,crole=crole)
    else:
        return render_template('inept.html', row=row , rows=rows ,id=id )

@app.route('/addboardc', methods=['POST'])
def addboardc2():
    conn = None
    cursor = None
    try:
        user_id = request.form['userid']
        role_id = request.form['roleid']
        bo_phase = request.form['bophase']
        pj_id = request.form['pjid']
# validate the received values
        if user_id and role_id and bo_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO board(user_id, role_id, bo_phase, pj_id) VALUES(%s, %s, %s, %s)"
            data = (user_id, role_id, bo_phase, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('เพิ่มรายชื่อสำเร็จ')
            return redirect('/project/'+pj_id+'/addboardc')
        else:
            return 'ไม่สามารถเพิ่มได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/project/<int:id>/addboarde',methods=[ 'GET'])
def addboarde(id):
    conn = None
    cursor = None
    phase = '3'
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 3 LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.office ON nsm_project.users.of_id = nsm_project.office.of_id LEFT JOIN nsm_project.division ON nsm_project.users.dv_id = nsm_project.division.dv_id WHERE nsm_project.projects.pj_id = %s order by nsm_project.tbl_role.role_id", id)
    row = cursor.fetchall()
    cursor.execute("SELECT * FROM (SELECT nsm_project.users.user_id,nsm_project.users.user_fullname,nsm_project.division.dv_shname FROM nsm_project.users LEFT JOIN nsm_project.division ON nsm_project.users.dv_id = nsm_project.division.dv_id) as a LEFT JOIN (SELECT nsm_project.board.user_id FROM nsm_project.projects LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id AND nsm_project.board.bo_phase = 3 LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id WHERE nsm_project.projects.pj_id = %s ) as b ON a.user_id = b.user_id where (CASE when b.user_id = a.user_id then 0 else a.user_id end) != 0 ", id)
    rows = cursor.fetchall()
    cursor.execute("SELECT count(case when nsm_project.board.role_id = '1' then 1 end) as cmng ,count(case when nsm_project.board.role_id = '2' then 1 end) as cboa,count(case when nsm_project.board.role_id = '3' then 1 end) as cas FROM  nsm_project.board WHERE nsm_project.board.pj_id = %s AND nsm_project.board.bo_phase=3", id)
    crole = cursor.fetchall()
    cursor.execute("SELECT * FROM nsm_project.process WHERE nsm_project.process.pj_id=%s", id)
    status = cursor.fetchall()
    stc = int(status[0]['stex_id'])
    cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
    role = cursor.fetchone()
    if (manager ==  role['role'] and stc == 1 ) :
           return render_template('addboarde.html', id=id,row=row,rows=rows,crole=crole)
    elif (manager ==  role['role'] and stc > 1 ) :
            return render_template('inept.html', id=id,row=row,rows=rows,crole=crole)        
    elif (assistant == role['role'] and stc == 1 or stc == 2 or stc == 3 or stc == 4 or stc == 5 or stc == 6) :
            return render_template('PMae.html', id=id,row=row,rows=rows,crole=crole)
    else:
        return render_template('inept.html', row=row , rows=rows ,id=id )

@app.route('/addboarde', methods=[ 'POST'])
def addboarde2():
    conn = None
    cursor = None
    try:
        user_id = request.form['userid']
        # ev_name = request.form['evname']
        role_id = request.form['roleid']
        bo_phase = request.form['bophase']
        pj_id = request.form['pjid']
# validate the received values
        if user_id and role_id and bo_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO board(user_id, role_id, bo_phase, pj_id) VALUES(%s, %s, %s, %s)"
            data = (user_id, role_id, bo_phase, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('เพิ่มรายชื่อสำเร็จ')
            return redirect('/project/'+pj_id+'/addboarde')
        else:
            return 'ไม่สามารถเพิ่มได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#ลบกรรมการ
@app.route('/project/<int:id>/deleteboardd/<int:idd>')
def delete_boardd(id,idd):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE bo_id=%s", (idd))
        conn.commit()
        flash('ลบรายชื่อสำเร็จ')
        return redirect('/project/'+str(id)+'/addboardd')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/project/<int:id>/deleteboardc/<int:idd>')
def delete_boardc(id,idd):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE bo_id=%s", (idd))
        conn.commit()
        flash('ลบรายชื่อสำเร็จ')
        return redirect('/project/'+str(id)+'/addboardc')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/project/<int:id>/deleteboarde/<int:idd>')
def delete_boarde(id,idd):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM board WHERE bo_id=%s", (idd))
        conn.commit()
        flash('ลบรายชื่อสำเร็จ')
        return redirect('/project/'+str(id)+'/addboarde')
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
    phase = 1
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%e %b %Y'
        tformat = '%H:%i'
        cursor.execute("SET lc_time_names = 'th_TH'")
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.events.ev_id) as row_num,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 1 WHERE nsm_project.projects.pj_id = %s", (format,tformat,id))
        row = cursor.fetchall()
        cursor.execute("SELECT nsm_project.process.PMcheck,nsm_project.process.start_draft,DATE_FORMAT(DATE_ADD(start_draft , INTERVAL 543 YEAR ), %s) as startdate,DATE_FORMAT(DATE_ADD(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY), INTERVAL 543 YEAR ), %s) AS endproject_date,DATEDIFF(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY),date(now())) AS diff,nsm_project.process.stdraft_id FROM nsm_project.process WHERE nsm_project.process.pj_id = %s", (format,format,id))
        diff = cursor.fetchall()
        drift = int(diff[0]['diff'])
        std = int(diff[0]['stdraft_id'])
        pmc = diff[0]['PMcheck']
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if(std <= 2 and pmc != 'prewait' and pmc != 'wait'):
            return render_template('draftEventB.html', row=row , id=id )
        elif (manager ==  role['role'] and drift > 30 or drift < 0 or std == 5) :
            return render_template('draftEventB.html', row=row , id=id )
        elif (manager ==  role['role'] and drift >= 1 or drift <= 30) :
            return render_template('draftEvent.html', row=row , id=id )
        elif(phase == role['bo_phase'] and manager !=  role['role']):
            if (assistant == role['role'] and drift >= 1 or drift <= 30) :
                return render_template('draftEvent.html', row=row ,id=id)
            elif (assistant == role['role'] and drift > 30 or drift < 0 or std == 5) :
                return render_template('draftEventB.html', row=row ,id=id)
            elif (board ==  role['role']) :
                return render_template('draftEventB.html', row=row ,id=id)
        else:
            return render_template('inept.html', row=row ,id=id )
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/project/<int:id>/considerEvent', methods=[ 'GET'])
def considerEvent(id):
    conn = None
    cursor = None
    phase = 2
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%e %b %Y'
        tformat = '%H:%i'
        cursor.execute("SET lc_time_names = 'th_TH'")
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.events.ev_id) as row_num,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 2 WHERE nsm_project.projects.pj_id = %s", (format,tformat,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM process WHERE pj_id=%s", id)
        rows = cursor.fetchall()
        stc = int(rows[0]['stcon_id'])
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role'] and stc == 7) :
            return render_template('considerEventB.html', row=row , id=id )
        elif (manager ==  role['role'] and stc < 7) :
            return render_template('considerEvent.html', row=row , id=id )
        elif (assistant == role['role'] and stc < 7 and phase == role['bo_phase']) :
            return render_template('considerEvent.html', row=row ,id=id)
        elif (assistant == role['role'] and stc == 7 and phase == role['bo_phase']) :
            return render_template('considerEventB.html', row=row ,id=id)
        elif (board ==  role['role'] and phase == role['bo_phase']) :
            return render_template('considerEventB.html', row=row ,id=id)
        else:
            return render_template('inept.html', row=row ,id=id )
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/project/<int:id>/examineEvent', methods=[ 'GET'])
def examineEvent(id):
    conn = None
    cursor = None
    phase = 3
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%e %b %Y'
        tformat = '%H:%i'
        cursor.execute("SET lc_time_names = 'th_TH'")
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.events.ev_id) as row_num,DATE_FORMAT(DATE_ADD(ev_date , INTERVAL 543 YEAR ), %s) as evdate,TIME_FORMAT(ev_time, %s) as evtime FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id AND nsm_project.events.ev_phase = 3 WHERE nsm_project.projects.pj_id = %s", (format,tformat,id))
        row = cursor.fetchall()
        cursor.execute("SELECT * FROM process WHERE pj_id=%s", id)
        rows = cursor.fetchall()
        stc = int(rows[0]['stex_id'])
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if (manager ==  role['role'] and stc == 6) :
            return render_template('examineEventB.html', row=row , id=id )
        elif (manager ==  role['role'] and stc < 6) :
            return render_template('examineEvent.html', row=row , id=id )
        elif (assistant == role['role'] and stc < 6 and phase == role['bo_phase']) :
            return render_template('examineEvent.html', row=row ,id=id)
        elif (assistant == role['role'] and stc == 6 and phase == role['bo_phase']) :
            return render_template('examineEventB.html', row=row ,id=id)
        elif (board ==  role['role'] and phase == role['bo_phase']) :
            return render_template('examineEventB.html', row=row ,id=id)
        else:
            return render_template('inept.html', row=row ,id=id )
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
    phase = 1
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects WHERE nsm_project.projects.pj_id = %s", id)
    row = cursor.fetchall()
    cursor.execute("SELECT nsm_project.process.start_draft,ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY) AS endproject_date,DATEDIFF(ADDDATE(nsm_project.process.start_draft, INTERVAL 30 DAY),date(now())) AS diff,nsm_project.process.stdraft_id FROM nsm_project.process WHERE nsm_project.process.pj_id = %s", (id))
    diff = cursor.fetchall()
    drift = int(diff[0]['diff'])
    std = int(diff[0]['stdraft_id'])
    cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
    role = cursor.fetchone()
    if (manager ==  role['role'] and drift > 30 or drift < 0 or std == 5) :
        return render_template('inept.html', id=id,row=row)
    elif (manager ==  role['role'] and drift >= 1 or drift <= 30) :
        return render_template('addeventd.html', row=row , id=id ,diff=diff)
    elif(phase == role['bo_phase'] and manager !=  role['role']):
        if (assistant == role['role'] and drift >= 1 or drift <= 30) :
            return render_template('addeventd.html', row=row ,id=id,diff=diff)
        elif (assistant == role['role'] and drift > 30 or drift < 0 or std == 5) :
            return render_template('inept.html', row=row ,id=id)
        elif (board ==  role['role']) :
            return render_template('inept.html', row=row ,id=id)
    else:
        return render_template('inept.html', row=row ,id=id )
    

@app.route('/addeventd', methods=[ 'POST'])
def addeventd2():
    conn = None
    cursor = None
    try:
        ev_name = request.form['evname']
        ev_detail = request.form['evdetail']
        ev_date = request.form['evdate']
        ev_phase = request.form['evphase']
        ev_time = request.form['evtime']
        pj_id = request.form['pjid']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO events(ev_name, ev_detail, ev_date, ev_phase, pj_id, ev_time) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id,ev_time)
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
    phase = 2
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects WHERE nsm_project.projects.pj_id = %s", id)
    row = cursor.fetchall()
    cursor.execute("SELECT * FROM process WHERE pj_id=%s", id)
    rows = cursor.fetchall()
    stc = int(rows[0]['stcon_id'])
    cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
    role = cursor.fetchone()
    if (manager ==  role['role'] and stc == 7) :
        return render_template('inept.html', id=id,row=row)
    elif (manager ==  role['role'] and stc < 7) :
        return render_template('addeventd.html', row=row , id=id )
    elif(phase == role['bo_phase'] and manager !=  role['role']):
        if (assistant == role['role'] and stc < 7) :
            return render_template('addeventd.html', row=row ,id=id)
        elif (assistant == role['role'] and stc == 7) :
            return render_template('inept.html', row=row ,id=id)
        elif (board ==  role['role']) :
            return render_template('inept.html', row=row ,id=id)
    else:
        return render_template('inept.html', row=row ,id=id )

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
        ev_time = request.form['evtime']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO events(ev_name, ev_detail, ev_date, ev_phase, pj_id, ev_time) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id, ev_time)
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
    phase = 3
    user = session['user_id']
    manager = 'manager'
    assistant = 'assistant'
    board = 'board'
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects WHERE nsm_project.projects.pj_id = %s", id)
    row = cursor.fetchall()
    cursor.execute("SELECT * FROM process WHERE pj_id=%s", id)
    rows = cursor.fetchall()
    stc = int(rows[0]['stex_id'])
    cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
    role = cursor.fetchone()
    if (manager ==  role['role'] and stc == 6) :
        return render_template('inept.html', id=id,row=row)
    elif (manager ==  role['role'] and stc < 6) :
        return render_template('addevente.html', row=row , id=id )
    elif(phase == role['bo_phase'] and manager !=  role['role']):
        if (assistant == role['role'] and stc < 6) :
            return render_template('addevente.html', row=row ,id=id)
        elif (assistant == role['role'] and stc == 6) :
            return render_template('inept.html', row=row ,id=id)
        elif (board ==  role['role']) :
            return render_template('inept.html', row=row ,id=id)
    else:
        return render_template('inept.html', row=row ,id=id )

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
        ev_time = request.form['evtime']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and request.method == 'POST':
# save edits
            sql = "INSERT INTO events(ev_name, ev_detail, ev_date, ev_phase, pj_id, ev_time) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (ev_name, ev_detail, ev_date, ev_phase, pj_id, ev_time)
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
@app.route('/project/<int:id>/editevent/<int:phase>/<int:idd>')
def editevent(id,idd,phase):
    if phase==1:
        phase="draft"
    elif phase==3:
        phase="consider"
    elif phase==4:
        phase="examine"
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id WHERE nsm_project.projects.pj_id = %s AND nsm_project.events.ev_id = %s", (id,idd))
    row = cursor.fetchall()
    return render_template('editevent.html', id=id,row=row,phase=phase)

@app.route('/editevent', methods=[ 'POST'])
def editevent2():
    conn = None
    cursor = None
    try:
        ev_name = request.form['evname']
        ev_detail = request.form['evdetail']
        ev_date = request.form['evdate']
        ev_time = request.form['evtime']
        ev_phase = request.form['evphase']
        pj_id = request.form['pjid']
        ev_id = request.form['evid']
# validate the received values
        if ev_name and ev_detail and ev_date and ev_phase and pj_id and ev_id and request.method == 'POST':
# save edits
            sql = "UPDATE events SET ev_name=%s, ev_detail=%s, ev_date=%s, ev_time=%s, ev_phase=%s WHERE pj_id=%s AND ev_id=%s"
            data = (ev_name, ev_detail, ev_date, ev_time, ev_phase, pj_id,ev_id)
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

#ลบอีเว้นท์
@app.route('/project/<int:id>/EVENT/<int:phase>/<int:evid>')
def delete_event(id,phase,evid):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        ph = phase
        cursor.execute("DELETE FROM events WHERE ev_id=%s", (evid))
        conn.commit()
        if ph == 1 :
            return redirect('/project/'+str(id)+'/draftEvent')
        elif ph == 2 :
            return redirect('/project/'+str(id)+'/considerEvent')
        elif ph == 3 :
            return redirect('/project/'+str(id)+'/examineEvent')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


#อัพเดทสถานะ
@app.route('/project/<int:id>/draft', methods=['POST'])
def update_std(id):
    conn = None
    cursor = None
    try:
        std = request.form['std']
        start_draft = request.form['startd']
        dast = request.form['appr']
        choose_stdraft = request.form['stdr']
        pmc = request.form['PMC']
        stdd = int(std)
        if stdd == 2 and pmc != 'wait' and pmc != 'prewait' :
            stdraft = 2
            draftapp_status = ''
            sdd = choose_stdraft
            pmch = 'prewait'
            end_draftd = '0000-00-00'
            end_draftt = '00:00:00'
        elif stdd == 2 and pmc == 'prewait' :
            stdraft = 2
            draftapp_status = 'finished'
            sdd = start_draft
            pmch = 'wait'
            end_draftd = '0000-00-00'
            end_draftt = '00:00:00'
        elif stdd == 2 and pmc == 'wait' :
            stdraft = 3
            draftapp_status = 'waitapp'
            sdd = start_draft
            pmch = ''
            end_draftd = '0000-00-00'
            end_draftt = '00:00:00'
        elif stdd == 3 and pmc != 'wait':
            stdraft = 3
            draftapp_status = 'yes'
            sdd = start_draft
            pmch = 'wait'
            end_draftd = '0000-00-00'
            end_draftt = '00:00:00'
        elif stdd == 3 and pmc == 'wait' and dast == 'yes':
            stdraft = 4
            draftapp_status = 'yes'
            sdd = start_draft
            pmch = 'yes'
            end_draftd = '0000-00-00'
            end_draftt = '00:00:00'
        elif stdd == 3 and pmc == 'wait' and dast == 'no':
            stdraft = 2
            draftapp_status = 'no'
            sdd = start_draft
            pmch = 'no'
            end_draftd = '0000-00-00'
            end_draftt = '00:00:00'
        elif stdd == 4 and pmc == 'yes':
            stdraft = 5
            draftapp_status = 'yes'
            sdd = start_draft
            pmch = 'yes'
            end_draftd = date.today()
            now = datetime.now()
            end_draftt = now.strftime("%H:%M:%S")
        sql = "UPDATE process SET stdraft_id=%s,draftapp_status=%s, start_draft=%s,end_draft_date=%s,end_draft_time=%s,PMcheck=%s WHERE pj_id=%s"
        data = (stdraft,draftapp_status,sdd,end_draftd,end_draftt,pmch, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id)+'/draft')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/project/<int:id>/consider', methods=['POST'])
def update_stc(id):
    conn = None
    cursor = None
    stc = request.form['stc']
    stcc = int(stc)
    cpmc = request.form['CPMC']
    cbd = request.form['checkboxdate']
    buydate = request.form['buy_date']
    invitedate = request.form['invite_date']
    propdate = request.form['prop_date']
    finishcondate = request.form['finishcon_date']
    reportdate = request.form['report_date']
    reporttime = request.form['report_time']
    winnerdate = request.form['winner_date']
    try:
        bdate = request.form['bdate']
        idate = request.form['idate']
        pdate = request.form['pdate']
        fdate = request.form['fdate']
        rdate = request.form['rdate']
        rtime = request.form['rtime']
        wdate = request.form['wdate']
        cdate = request.form['conappd']
        capp = request.form['conapp']
        pj_status = ''
        if (stcc == 2 and cpmc != "wait"):
            if (cbd == "1"):
                stcon = 2
                buy_date = buydate
                invite_date = invitedate
                prop_date = propdate
                finishcon_date = '0000-00-00'
                report_date = '0000-00-00'
                report_time = '00:00:00'
                winner_date = '0000-00-00'
                conapp_date = '0000-00-00'
                conapp_status = ''
                conPMcheck = 'wait'
            elif (cbd == "0"):
                stcon = 2
                buy_date = '0000-00-00'
                invite_date = '0000-00-00'
                prop_date = '0000-00-00'
                finishcon_date = '0000-00-00'
                report_date = '0000-00-00'
                report_time = '00:00:00'
                winner_date = '0000-00-00'
                conapp_date = '0000-00-00'
                conapp_status = ''
                conPMcheck = 'wait'
        elif (stcc == 2 and cpmc == "wait"):
            stcon = 3
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = finishcondate
            report_date = '0000-00-00'
            report_time = '00:00:00'
            winner_date = '0000-00-00'
            conapp_date = '0000-00-00'
            conapp_status = ''
            conPMcheck = ''
        elif (stcc == 3 and cpmc != "wait"):
            stcon = 3
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = '0000-00-00'
            report_time = '00:00:00'
            winner_date = '0000-00-00'
            conapp_date = '0000-00-00'
            conapp_status = ''
            conPMcheck = 'wait'
        elif (stcc == 3 and cpmc == "wait"):
            stcon = 4
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = '0000-00-00'
            report_time = '00:00:00'
            winner_date = '0000-00-00'
            conapp_date = '0000-00-00'
            conapp_status = ''
            conPMcheck = ''
        elif (stcc == 4):
            stcon = 5
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = reportdate
            report_time = reporttime
            winner_date = '0000-00-00'
            conapp_date = '0000-00-00'
            conapp_status = ''
            conPMcheck = ''
        elif (stcc == 5 and cpmc != "wait" ):
            stcon = 5
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = rdate
            report_time = rtime
            winner_date = winnerdate
            conapp_date = '0000-00-00'
            conapp_status = ''
            conPMcheck = 'wait'
        elif (stcc == 6 and cpmc != "wait" ):
            stcon = 6
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = rdate
            report_time = rtime
            winner_date = wdate
            conapp_date = cdate
            conapp_status = 'yes'
            conPMcheck = 'wait'
        elif (stcc == 6 and capp == 'yes' and cpmc == "wait" ):
            stcon = 7
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = rdate
            report_time = rtime
            winner_date = wdate
            conapp_date = cdate
            conapp_status = 'yes'
            conPMcheck = 'yes'
        elif (stcc == 6 and capp == 'no' and cpmc == "wait" ):
            stcon = 6
            buy_date = bdate
            invite_date = idate
            prop_date = pdate
            finishcon_date = fdate
            report_date = rdate
            report_time = rtime
            winner_date = wdate
            conapp_date = cdate
            conapp_status = 'no'
            conPMcheck = 'no'
            pj_status = 'closed'
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "UPDATE process SET stcon_id=%s,buy_date=%s,invite_date=%s,prop_date=%s,finishcon_date=%s,report_date=%s,report_time=%s,winner_date=%s,conapp_date=%s,conapp_status=%s,conPMcheck=%s WHERE pj_id=%s"
        data = (stcon,buy_date,invite_date,prop_date,finishcon_date,report_date,report_time,winner_date,conapp_date,conapp_status,conPMcheck, id)
        cursor.execute(sql, data)
        sql1 = "UPDATE projects SET pj_status=%s WHERE pj_id=%s"
        data1 = (pj_status, id)
        cursor.execute(sql1, data1)
        conn.commit()
        return redirect('/project/'+str(id)+'/consider')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close() 

@app.route('/project/<int:id>/examine', methods=['POST'])
def update_ste(id):
    conn = None
    cursor = None
    try:
        ste = request.form['ste']
        stex_id = int(ste)+1
        stex = stex_id
        sql = "UPDATE process SET stex_id=%s WHERE pj_id=%s"
        data = (stex, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id)+'/examine')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#ไม่อนุมัติ
@app.route('/project/<int:id>/draft/unapproved', methods=['POST'])
def unapproved(id):
    conn = None
    cursor = None
    try:
        stdraft = 3
        draftapp_status = 'no'
        pmch = 'wait'
        sql = "UPDATE process SET stdraft_id=%s,draftapp_status=%s,PMcheck=%s WHERE pj_id=%s"
        data = (stdraft,draftapp_status,pmch, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id)+'/draft')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#มีอุทธรณ์
@app.route('/project/<int:id>/consider/appeal', methods=['POST'])
def uappeal(id):
    conn = None
    cursor = None
    try:
        conapp_status = 'no'
        cpmch = 'wait'
        sql = "UPDATE process SET conapp_status=%s,conPMcheck=%s WHERE pj_id=%s"
        data = (conapp_status,cpmch, id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id)+'/consider')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


#หน้าเพิ่มโครงการ
# ก่อนเอาไอดีpjไปเก็บ
@app.route('/addProject',methods=['GET'])
def addProjectview():
    cursor = mysql.connect().cursor(pymysql.cursors.DictCursor)
    format = '%Y'
    cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 543 YEAR ), %s) as curyear,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 542 YEAR ), %s) as curyear1,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 541 YEAR ), %s) as curyear2,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 544 YEAR ), %s) as curyear11,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 545 YEAR ), %s) as curyear22 FROM office ORDER BY of_id",(format,format,format,format,format))
    office = cursor.fetchall()
    return render_template("addproject.html", office=office) 
    
@app.route('/addProject',methods=['POST'])
def addProject():
    user = session['user_id']
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        pj_refNumber = request.form['refNumber']
        of_id = request.form['ofid']
        dv_id = request.form['dvid']
        pj_name = request.form['name']
        pj_type = request.form['radio']
        pj_amount = request.form['amount']
        pj_detail = request.form['detail']
        pj_financeAmount = request.form['financeAmount']
        pj_budgetSource = request.form['budgetSource']
        pj_budgetYears = request.form['budgetYears']
        if  pj_refNumber and of_id and dv_id and pj_name and pj_type and pj_amount and pj_detail and pj_financeAmount and pj_budgetSource and pj_budgetYears and request.method == 'POST':
            sql1 = "INSERT INTO projects (pj_refNumber,of_id,dv_id,pj_name,pj_type,pj_amount,pj_detail,pj_financeAmount,pj_budgetSource,pj_budgetYears) VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s)"
            data1 = (pj_refNumber,of_id,dv_id,pj_name,pj_type,pj_amount,pj_detail,pj_financeAmount,pj_budgetSource,pj_budgetYears)
            cursor.execute(sql1, data1)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT pj_id FROM nsm_project.projects order by pj_id DESC;")
            sql2 = cursor.fetchall()
            pj_id = sql2[0]['pj_id']
            sql3 = "INSERT INTO manager (user_id,pj_id) VALUES(%s, %s)"
            data3 = (user,pj_id)
            cursor.execute(sql3, data3)
            sql4 = "INSERT INTO process (pj_id,stdraft_id,stcon_id,stex_id,startproject_date) VALUES(%s,%s,%s,%s,%s)"
            data4 = (pj_id,1,1,1,date.today())
            cursor.execute(sql4, data4)
            conn.commit()
            return redirect ('/home')
        else:
            return 'Error'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close() 

@app.route("/division",methods=["POST","GET"])
def division():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            category_id = request.form['category_id'] 
            result = cursor.execute("SELECT * FROM  division WHERE of_id = %s ORDER BY dv_name ASC", [category_id])
            division = cursor.fetchall() 
            OutputArray = []
            for result in division:
                outputObj = {
                    'id': result['dv_id'],
                    'name': result['dv_name'],
                    'shname':result['dv_shname']}
                OutputArray.append(outputObj)
            return jsonify(OutputArray) 
            
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#อัพเอกสาร
@app.route('/project/<int:id>/doc/<int:phase>', methods=['GET',"POST"])
def doc(id,phase):
    if phase==1:
        p='draft'
    elif phase==2:
        p='consider'
    elif phase==3:
        p='examine'
    form = UploadFileForm()
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.path WHERE nsm_project.path.pj_id=%s AND nsm_project.path.path_phase=%s",(id,phase))
    row = cursor.fetchall()
    if form.validate_on_submit():
        path_name = request.form['path_name']
        path_detail = request.form['path_detail']
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        sql = "INSERT INTO path(pj_id,path_phase,path_path,path_name,path_detail) VALUES(%s,%s,%s,%s,%s)"
        data = (id,phase,file.filename,path_name,path_detail)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect(str(phase))
    return render_template('doc.html', row=row,form=form,id=id,phase=phase,p=p)

#ลบเอกสาร
@app.route('/project/<int:id>/doc/<int:phase>/<int:path>')
def delete_docd(id,phase,path):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM path WHERE path_id=%s", (path))
        conn.commit()
        return redirect('/project/'+str(id)+'/doc/'+str(phase)+'')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#ทดสอบ

@app.route('/t')
def test():
    a=session['user_id']
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 543 YEAR ), %s) as curyear,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 542 YEAR ), %s) as curyear1,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 541 YEAR ), %s) as curyear2,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 544 YEAR ), %s) as curyear11,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 545 YEAR ), %s) as curyear22 FROM office ORDER BY of_id",(format,format,format,format,format))
        office = cursor.fetchall()
        return render_template('test.html', office=office )
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/t2')
def test2():
    a=session['user_id']
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.manager.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        MN = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        BO = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 1 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        DR = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 2 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        CO = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 3 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        EX = cursor.fetchall()
        return render_template('test2.html', BO=BO,MN=MN,DR=DR,CO=CO,EX=EX )
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/t3')
def test3():
    a=session['user_id']
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.manager.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        MN = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        BO = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 1 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        DR = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 2 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        CO = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id WHERE nsm_project.board.user_id = %s and nsm_project.board.bo_phase = 3 group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc",(a))
        EX = cursor.fetchall()
        return render_template('test3.html', BO=BO,MN=MN,DR=DR,CO=CO,EX=EX )
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/project/<int:id>/editproject',methods = ['GET'])
def editproject(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM nsm_project.projects  WHERE nsm_project.projects.pj_id = %s ", (id))
    row = cursor.fetchall()
    return render_template('editproject.html', id=id,row=row)

#html ชื่อ editproject
@app.route('/editproject', methods=[ 'POST'])
def editproject2():
    conn = None
    cursor = None
    try:
        refNumber = request.form['refNumber']
        name = request.form['name']
        amount = request.form['amount']
        detail = request.form['detail']
        pj_id = request.form['pjid']
# validate the received values
        if refNumber and name and amount and detail and pj_id and request.method == 'POST':
# save edits
            sql = "UPDATE projects SET pj_refNumber=%s,  pj_name=%s,  pj_amount=%s,  pj_detail=%s WHERE pj_id=%s"
            data = (refNumber, name, amount, detail, pj_id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect ('/project/'+pj_id+'')
        else:
            return 'ไม่สามารถแก้ไขโปรเจคได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

#หน้าเพิ่มข้อมูลบริษัท
@app.route('/addcontractor/<int:id>',methods=['GET'])
def addcontractor(id):
    conn = None
    cursor = None
    phase = 2
    user = session['user_id']
    assistant = 'assistant'
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT max(contt_id) FROM nsm_project.contractor;")
        row = cursor.fetchall()
        cursor.execute("SELECT pj_amount FROM projects WHERE pj_id=%s", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if(phase == role['bo_phase'] and assistant == role['role']):
            return render_template("addcontractor.html",id=id,row=row,rows=rows) 
        else:
            return render_template('inept.html', row=row ,id=id ) 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    
@app.route('/addcontractor/<int:id>', methods=['POST'])
def addcontractor2(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        contt_date = request.form['contt_date']
        contt_name = request.form['contt_name']
        contt_address = request.form['contt_address']
        contt_tel = request.form['contt_tel']
        contt_email = request.form['contt_email']
        contt_fin = request.form['contt_fin']
        if  contt_date and contt_name and contt_address and contt_tel and contt_email and contt_fin and  request.method == 'POST':
            sql = "INSERT INTO contractor (contt_date, contt_name, contt_address, contt_tel, contt_email, contt_fin) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (contt_date,contt_name,contt_address,contt_tel,contt_email,contt_fin)
            cursor.execute(sql, data)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT contt_id,contt_date FROM nsm_project.contractor order by contt_id DESC;")
            sql1 = cursor.fetchall()
            contt = sql1[0]['contt_id']
            conttstart = sql1[0]['contt_date']
            conPM = ''
            update = "UPDATE process SET contt_id=%s,stcon_id=%s,conapp_date=%s,conPMcheck=%s WHERE pj_id = %s"
            data1 = (contt,6,conttstart,conPM,id)
            cursor.execute(update, data1)
            conn.commit()
            return redirect ('/project/'+str(id)+'/consider')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
        cursor.close() 
        conn.close()

#แก้ไขcontrac
@app.route('/editcontractor/<int:id>',methods=['GET'])
def editcontractorveiw(id):
    conn = None
    cursor = None
    phase = 2
    user = session['user_id']
    assistant = 'assistant'
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.process LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id =  nsm_project.contractor.contt_id WHERE pj_id=%s", id)
        row = cursor.fetchall()
        cursor.execute("SELECT pj_amount FROM projects WHERE pj_id=%s", id)
        rows = cursor.fetchall()
        cursor.execute("SELECT *,CASE WHEN nsm_project.manager.user_id = nsm_project.users.user_id THEN 'manager' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 1 OR nsm_project.board.role_id = 2 THEN 'board' WHEN nsm_project.board.user_id = nsm_project.users.user_id AND nsm_project.board.role_id = 3 THEN 'assistant' END AS role FROM nsm_project.projects LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.pj_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id LEFT JOIN nsm_project.tbl_role ON nsm_project.board.role_id = nsm_project.tbl_role.role_id LEFT JOIN nsm_project.users ON nsm_project.board.user_id = nsm_project.users.user_id or nsm_project.manager.user_id = nsm_project.users.user_id Where nsm_project.projects.pj_id = %s and nsm_project.users.user_id = %s group by nsm_project.users.user_id",(id ,user))
        role = cursor.fetchone()
        if(phase == role['bo_phase'] and assistant == role['role']):
            return render_template("editcontractor.html",id=id,row=row,rows=rows) 
        else:
            return render_template('inept.html', row=row ,id=id ) 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/editcontractor/<int:id>', methods=['POST'])
def editcontractor(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        contt_name = request.form['contt_name']
        contt_address = request.form['contt_address']
        contt_tel = request.form['contt_tel']
        contt_email = request.form['contt_email']
        contt_fin = request.form['contt_fin']
        if  contt_name and contt_address and contt_tel and contt_email and contt_fin and  request.method == 'POST':
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "UPDATE contractor SET contt_name=%s, contt_address=%s, contt_tel=%s, contt_email=%s, contt_fin=%s "
            data = (contt_name,contt_address,contt_tel,contt_email,contt_fin,)
            cursor.execute(sql, data)
            conn.commit()
            return redirect ('/project/'+str(id)+'/consider')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
        cursor.close() 
        conn.close()

#หน้าประกาศจาก กพ. -----------------------------------------------------------------------------------------------------------------------------------
@app.route('/project/<int:id>/viewpac', methods=[ 'GET'])
def viewpac(id):
    format = '%e %b %Y'
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SET lc_time_names = 'th_TH'")
    cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(pac_date , INTERVAL 543 YEAR ), %s) as pacdate FROM nsm_project.pacel RIGHT JOIN nsm_project.projects ON nsm_project.projects.pj_id = nsm_project.pacel.pj_id WHERE nsm_project.projects.pj_id=%s ORDER BY pac_id DESC",(format,id))
    pac = cursor.fetchall()
    return render_template('viewpac.html', id=id,pac=pac)

@app.route('/project/<int:id>/addpacview', methods=[ 'GET'])
def addpacview(id):
    format = '%e %b %Y'
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SET lc_time_names = 'th_TH'")
    cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(pac_date , INTERVAL 543 YEAR ), %s) as pacdate FROM nsm_project.pacel RIGHT JOIN nsm_project.projects ON nsm_project.projects.pj_id = nsm_project.pacel.pj_id WHERE nsm_project.projects.pj_id=%s ORDER BY pac_id DESC",(format,id))
    pac = cursor.fetchall()
    return render_template('addpac.html', id=id,pac=pac)

@app.route('/addpac/<int:id>', methods=[ 'POST'])
def addpac(id):
    conn = None
    cursor = None
    try:
        pac_detail = request.form['pac_detail']
        pac_date = request.form['pac_date']
        if pac_detail and pac_date and request.method == 'POST':
            sql = "INSERT INTO pacel(pac_detail,pac_date,pj_id) VALUES(%s, %s, %s)"
            data = (pac_detail,pac_date,id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            return redirect('/project/'+str(id)+'/addpacview')
        else:
            return 'ไม่สามารถเพิ่มกิจกรรมได้'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/deletepac/<int:id>/<int:pac_id>')
def deletepac(id,pac_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacel WHERE pac_id=%s", (pac_id))
        conn.commit()
        flash('ลบรายการประกาศเสร็จสิ้น')
        return redirect('/project/'+str(id)+'/addpacview')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/editpac/<int:id>/<int:pac_id>',methods=['GET'])
def editpacveiw(id,pac_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.pacel WHERE nsm_project.pacel.pac_id=%s;",pac_id)
        pac = cursor.fetchall()
        return render_template("editpac.html",id=id,pac=pac) 
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/editpac/<int:id>/<int:pac_id>', methods=['POST'])
def editpac(id,pac_id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        pac_detail = request.form['pac_detail']
        pac_date = request.form['pac_date']
        if  pac_detail and pac_date and  request.method == 'POST':
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "UPDATE pacel SET pac_detail=%s,pac_date=%s WHERE pac_id=%s"
            data = (pac_detail,pac_date,pac_id)
            cursor.execute(sql, data)
            conn.commit()
            return redirect ('/project/'+str(id)+'/addpacview')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
        cursor.close() 
        conn.close()
#---------------------------------------------------------------------------------------------------------------------------------------------------

#addmin
@app.route('/admin')
def admin():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num ,CAST(((stdraft_percent+stcon_percent+stex_percent)/3) AS DECIMAL(15, 2)) as x FROM nsm_project.projects LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.status_draft ON nsm_project.process.stdraft_id = nsm_project.status_draft.stdraft_id LEFT JOIN nsm_project.status_consider ON nsm_project.process.stcon_id = nsm_project.status_consider.stcon_id LEFT JOIN nsm_project.status_examine ON nsm_project.process.stex_id = nsm_project.status_examine.stex_id LEFT JOIN nsm_project.events ON nsm_project.projects.pj_id = nsm_project.events.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.manager ON nsm_project.projects.pj_id = nsm_project.manager.mn_id  LEFT JOIN nsm_project.users ON nsm_project.manager.user_id = nsm_project.users.user_id LEFT JOIN nsm_project.board ON nsm_project.projects.pj_id = nsm_project.board.pj_id group by nsm_project.projects.pj_id order by nsm_project.projects.pj_id asc, nsm_project.events.ev_id desc")
        row = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num FROM nsm_project.projects order by nsm_project.projects.pj_id desc;")
        pjAll = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num FROM nsm_project.projects where nsm_project.projects.pj_status=1 order by nsm_project.projects.pj_id desc;")
        st1 = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num FROM nsm_project.projects where nsm_project.projects.pj_status=2 order by nsm_project.projects.pj_id desc;")
        st2 = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.projects.pj_id) as row_num FROM nsm_project.projects where nsm_project.projects.pj_status=3 order by nsm_project.projects.pj_id desc;")
        st3 = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.users.user_id) as row_num FROM nsm_project.users order by nsm_project.users.user_id desc;")
        em = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.office.of_id) as row_num FROM nsm_project.office order by nsm_project.office.of_id desc;")
        of = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.division.dv_id) as row_num FROM nsm_project.division order by nsm_project.division.dv_id desc;")
        dv = cursor.fetchall()
        return render_template('admin.html',row=row,em=em,of=of,dv=dv,st1=st1,st2=st2,st3=st3,pjAll=pjAll)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/admin/office')
def adminOffice():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        format = '%Y'
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 543 YEAR ), %s) as curyear,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 542 YEAR ), %s) as curyear1,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 541 YEAR ), %s) as curyear2,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 544 YEAR ), %s) as curyear11,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 545 YEAR ), %s) as curyear22 FROM office ORDER BY of_id",(format,format,format,format,format))
        office = cursor.fetchall()
        return render_template('adminOffice.html',office=office)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/admin/employee')
def adminEmployee():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.users.user_id) as row_num FROM nsm_project.users LEFT JOIN nsm_project.office ON nsm_project.users.of_id=nsm_project.office.of_id LEFT JOIN nsm_project.division ON nsm_project.users.dv_id=nsm_project.division.dv_id WHERE nsm_project.users.user_role='user' order by nsm_project.users.user_id desc;")
        em = cursor.fetchall()
        cursor.execute("SELECT *,ROW_NUMBER() OVER(ORDER BY nsm_project.users.user_id) as row_num FROM nsm_project.users LEFT JOIN nsm_project.office ON nsm_project.users.of_id=nsm_project.office.of_id LEFT JOIN nsm_project.division ON nsm_project.users.dv_id=nsm_project.division.dv_id WHERE nsm_project.users.user_role='admin' order by nsm_project.users.user_id desc;")
        ad = cursor.fetchall()
        return render_template('adminEmployee.html',em=em,ad=ad)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/admin/employee/edit/<int:id>',methods=['GET'])
def adminEmployeeEdit(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.users LEFT JOIN nsm_project.office ON nsm_project.users.of_id=nsm_project.office.of_id LEFT JOIN nsm_project.division ON nsm_project.users.dv_id=nsm_project.division.dv_id WHERE nsm_project.users.user_id=%s;",(id))
        row = cursor.fetchall()
        cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 543 YEAR ), %s) as curyear,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 542 YEAR ), %s) as curyear1,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 541 YEAR ), %s) as curyear2,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 544 YEAR ), %s) as curyear11,DATE_FORMAT(DATE_ADD(curdate(), INTERVAL 545 YEAR ), %s) as curyear22 FROM office ORDER BY of_id",(format,format,format,format,format))
        office = cursor.fetchall()
        return render_template('adminEmployeeEdit.html',row=row,office=office)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
    

@app.route('/edituser/<int:id>', methods=['POST'])
def editUser(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        user_name = request.form['user_name']
        user_fullname = request.form['user_fullname']
        user_email = request.form['user_email']
        user_role = request.form['user_role']
        tel = request.form['tel']
        of_id = request.form['of_id']
        dv_id = request.form['dv_id']
        if  user_name and user_fullname and user_email and user_role and tel and of_id and dv_id and request.method == 'POST':
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "UPDATE pacel SET user_name=%s,user_fullname=%s,user_email=%s,user_role=%s,tel=%s,of_id=%s,dv_id and WHERE user_id=%s"
            data = (user_name,user_fullname,user_email,user_role,tel,of_id,dv_id,id)
            cursor.execute(sql, data)
            conn.commit()
            return redirect ('/admin/employee')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/delete/user/<int:id>')
def deleteUser(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=%s", (id))
        conn.commit()
        flash('ลบพนักงานเสร็จสิ้น')
        return redirect('/admin/employee')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/project/<int:id>/check', methods=['GET'])
def check(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    format = '%e %b %Y'
    cursor.execute("SET lc_time_names = 'th_TH'")
    cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(check_date , INTERVAL 543 YEAR ), %s) as checkdate,DATE_FORMAT(DATE_ADD(ins_date , INTERVAL 543 YEAR ), %s) as insdate FROM nsm_project.projects  LEFT JOIN nsm_project.process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN nsm_project.contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id LEFT JOIN nsm_project.checks ON nsm_project.projects.pj_id = nsm_project.checks.pj_id WHERE nsm_project.projects.pj_id = %s group by nsm_project.checks.check_id", (format,format,id))
    row = cursor.fetchall()
    return render_template('check.html', id=id,row=row)


@app.route('/addcheck', methods=['POST'])
def addcheck():
    conn = None
    cursor = None
    try:
        pj_id = request.form['pj_id']
        ins_no = request.form['ins_no']
        contractNo = request.form['contractNo']
        check_date = request.form['check_date']
        check_detail = request.form['check_detail']
        ins_date = request.form['ins_date']
        ins_amount = request.form['ins_amount']
        ins_detail = request.form['ins_detail']
        ins_no1 = request.form['ins_no1']
        contractNo1 = request.form['contractNo1']
        check_date1 = request.form['check_date1']
        check_detail1 = request.form['check_detail1']
        ins_date1 = request.form['ins_date1']
        ins_amount1 = request.form['ins_amount1']
        ins_detail1 = request.form['ins_detail1']
        ins_no2 = request.form['ins_no2']
        contractNo2 = request.form['contractNo']
        check_date2 = request.form['check_date2']
        check_detail2 = request.form['check_detail2']
        ins_date2 = request.form['ins_date2']
        ins_amount2 = request.form['ins_amount2']
        ins_detail2 = request.form['ins_detail2']
        contt_m = request.form['contt_m']
        if  pj_id and ins_no and contractNo and check_date and check_detail and ins_date and ins_amount and ins_detail and ins_no1 and contractNo1 and check_date1 and check_detail1 and ins_date1 and ins_amount1 and ins_detail1 and ins_no2 and contractNo2 and check_date2 and check_detail2 and ins_date2 and ins_amount2 and ins_detail2 and  request.method == 'POST':
            sql = "INSERT INTO checks (pj_id, ins_no, conNo, check_date, check_detail, ins_date, ins_amount, ins_detail) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (pj_id,ins_no,contractNo,check_date,check_detail,ins_date,ins_amount,ins_detail, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            sql = "INSERT INTO checks (pj_id, ins_no, conNo, check_date, check_detail, ins_date, ins_amount, ins_detail) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            data1 = (pj_id,ins_no1,contractNo1,check_date1,check_detail1,ins_date1,ins_amount1,ins_detail1, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data1)
            conn.commit()
            sql = "INSERT INTO checks (pj_id, ins_no, conNo, check_date, check_detail, ins_date, ins_amount, ins_detail) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            data2 = (pj_id,ins_no2,contractNo2,check_date2,check_detail2,ins_date2,ins_amount2,ins_detail2, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data2)
            conn.commit()
            sql = "UPDATE process SET  stex_id = 3 where pc_id =%s"
            data3 = (pj_id, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data3)
            conn.commit()
            return redirect('/project/'+pj_id+'/examine')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

# --------------------------------------------------------------------------------------------------------
@app.route('/editcheck/<int:id>', methods=['GET'])
def editcheck(id):
    conn = None
    cursor = None
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    format = '%e %b %Y'
    cursor.execute("SET lc_time_names = 'th_TH'")
    cursor.execute("SELECT *,DATE_FORMAT(DATE_ADD(check_date , INTERVAL 543 YEAR ), %s) as checkdate,DATE_FORMAT(DATE_ADD(ins_date , INTERVAL 543 YEAR ),%s) as insdate FROM checks LEFT JOIN projects ON nsm_project.checks.pj_id = nsm_project.projects.pj_id LEFT JOIN process ON nsm_project.projects.pj_id = nsm_project.process.pj_id LEFT JOIN contractor ON nsm_project.process.contt_id = nsm_project.contractor.contt_id WHERE nsm_project.checks.pj_id = %s", (format,format,id))
    row = cursor.fetchall()
    return render_template('editcheck.html', id=id,row=row)

@app.route('/upchecksss', methods=['POST'])
def upchecksss():
    conn = None
    cursor = None
    try:
        pj_id = request.form['pj_id']
        ins_no = request.form['ins_no']
        contractNo = request.form['contractNo']
        check_date = request.form['check_date']
        check_detail = request.form['check_detail']
        ins_date = request.form['ins_date']
        ins_amount = request.form['ins_amount']
        ins_detail = request.form['ins_detail']
        ins_no1 = request.form['ins_no1']
        contractNo1 = request.form['contractNo1']
        check_date1 = request.form['check_date1']
        check_detail1 = request.form['check_detail1']
        ins_date1 = request.form['ins_date1']
        ins_amount1 = request.form['ins_amount1']
        ins_detail1 = request.form['ins_detail1']
        ins_no2 = request.form['ins_no2']
        contractNo2 = request.form['contractNo2']
        check_date2 = request.form['check_date2']
        check_detail2 = request.form['check_detail2']
        ins_date2 = request.form['ins_date2']
        ins_amount2 = request.form['ins_amount2']
        ins_detail2 = request.form['ins_detail2']
        check_id1 = request.form['check_id1']
        check_id2 = request.form['check_id2']
        check_id3 = request.form['check_id3']
        if  pj_id and ins_no and contractNo and check_date and check_detail and ins_date and ins_amount and ins_detail and ins_no1 and contractNo1 and check_date1 and check_detail1 and ins_date1 and ins_amount1 and ins_detail1 and ins_no2 and contractNo2 and check_date2 and check_detail2 and ins_date2 and ins_amount2 and ins_detail2 and  request.method == 'POST':
            sql = "UPDATE checks SET  conNo=%s, check_date=%s, check_detail=%s, ins_date=%s, ins_amount=%s, ins_detail=%s WHERE check_id =%s"
            data = (contractNo,check_date,check_detail,ins_date,ins_amount,ins_detail,check_id1, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            sql = "UPDATE checks SET  conNo=%s, check_date=%s, check_detail=%s, ins_date=%s, ins_amount=%s, ins_detail=%s WHERE check_id =%s"
            data1 = (contractNo1,check_date1,check_detail1,ins_date1,ins_amount1,ins_detail1,check_id2, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data1)
            conn.commit()
            sql = "UPDATE checks SET  conNo=%s, check_date=%s, check_detail=%s, ins_date=%s, ins_amount=%s, ins_detail=%s WHERE check_id =%s"
            data2 = (contractNo2,check_date2,check_detail2,ins_date2,ins_amount2,ins_detail2,check_id3, )
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data2)
            conn.commit()
            return redirect('/project/'+pj_id+'/examine')
        else:
            return 'Error'
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()


@app.route('/project/<int:id>/examinex', methods=['POST'])
def update_stdx(id):
    conn = None
    cursor = None
    try:
        std = request.form['std']
        pmc = request.form['PMC']
        stdd = int(std)
        print(type(std))
        print(std)
        sql = "UPDATE process SET stex_id=%s,PMcheck=%s WHERE pj_id=%s"
        data = (std,pmc,id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        return redirect('/project/'+str(id)+'/examine')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()

@app.route('/examineup/<int:id>')
def examineup(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM nsm_project.process WHERE nsm_project.process.pj_id=%s", id)
        status = cursor.fetchall()
        stc = int(status[0]['stex_id'])
        if(stc == 1):
            sql = "UPDATE process SET stex_id = 2 where pj_id =%s"
            data = (id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()
            return redirect('/project/'+str(id)+'/examine')
        else:
            return redirect('/project/'+str(id)+'/examine')
    except Exception as e:
           print(e)
    finally:
           cursor.close() 
           conn.close()


if __name__ == "__main__":
    app.run(debug=True)