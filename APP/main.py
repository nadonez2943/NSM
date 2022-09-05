from flask import Flask, render_template, request, redirect, url_for, session
from db_config import MySQL
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/draft')
def draft():
    return render_template('draft.html')

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/addproject')
def addproject():
    return render_template('addproject.html')

@app.route('/addboard')
def addboard():
    return render_template('addboard.html')

@app.route('/กรรมการ')
def k():
    return render_template('กรรมการ.html')

if __name__ == "__main__":
    app.run(debug=True)
