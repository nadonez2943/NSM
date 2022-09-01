from flask import Flask, render_template, request, redirect, url_for, session
from db_config import MySQL
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/draft')
def draft():
    return render_template('draft.html')

@app.route('/consider')
def consider():
    return render_template('consider.html')

@app.route('/examine')
def examine():
    return render_template('examine.html')

@app.route('/t')
def h():
    return render_template('test.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
