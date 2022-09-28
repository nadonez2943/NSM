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
