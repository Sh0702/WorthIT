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
        print(account)
        return render_template('asset.html')
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

@app.route('/forgetpassword')
def forget():
    return render_template('forgetpassword.html')

@app.route('/changepassword')
def change():
    return render_template('changepassword.html')

@app.route('/redirect')
def redirect():
    return render_template('redirect.html')

@app.route('/assets/add', methods = ['POST'])
def add():
    name = request.form['Assets[]']
    cost = request.form['Cost_asset[]']
    addButton = request.form['add']
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM assets WHERE name=%s;",(name,))
    account = cursor.fetchone()
    if account:
        msg = 'Asset of this name already exists'
    else:
        cursor.execute('INSERT INTO assets(user_id,name,cost) VALUES (%s,%s,%s);',(name,cost,))
        db.connection.commit()
        msg = 'Your Asset has been successfully added.'
    return render_template('asset.html', msg=msg)

"""
@app.route('/assets/remove/:id', methods = ['POST'])
def remove():
    cursor = db.connection.cursor()
    account = cursor.fetchone()
    cursor.execute('DELETE FROM assets WHERE id = %s;',(id,))
    db.connection.commit()
    msg = 'Your Asset has been successfully deleted.'
    return render_template('asset.html', msg=msg)
"""

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)