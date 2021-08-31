from flask import Flask,render_template,url_for,request
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'Q5AnYu8fbC'
app.config['MYSQL_PASSWORD'] = '6TMd3zYuOe'
app.config['MYSQL_DB'] = 'Q5AnYu8fbC'

db = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods =['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    cursor = db.connection.cursor()
    cursor.execute('SELECT * FROM register WHERE Username = %s AND Password = %s', (username, password,))
    account = cursor.fetchone()
    if account:
        msg = 'Login Successful !!!'
        return render_template('index.html',msg=msg)
    msg = 'Incorrect username or password !'
    return render_template('login.html',msg=msg)

@app.route("/createaccount")
def create():
    return render_template('signup.html')

@app.route('/register', methods =['POST'])
def insert():
    fullName = request.form['name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm']
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM register WHERE username = %s;", (username ,))
    account = cursor.fetchone()   
    
    if account:   
        msg = 'Account already exists !'
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        msg = 'Invalid email address !'
    elif not re.match(r'[A-Za-z]',fullName):
        msg = 'Name can only contain alphabetical characters'
    elif not username or not password or not email or not fullName:
        msg = 'Please fill out the form !'
    elif password != confirm:
        msg = 'Passwords do not match.'
    else:
        cursor.execute('INSERT INTO register(fullName,emailID,Username,Password) VALUES (%s, %s, %s, %s);', (fullName,email,username,password))
        db.connection.commit()
        msg = 'You have successfully registered !'    
    return render_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)