from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQLdb,MySQL
import mysql.connector,re

db = MySQL()

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'Q5AnYu8fbC'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b5MclYuvJn'
app.config['MYSQL_DATABASE_DB'] = 'login'
app.config['MYSQL_DATABASE_host'] = 'https://remotemysql.com/phpmyadmin/sql.php?server=1&db=Q5AnYu8fbC&table=register&pos=0'
db.init_app(app)

@app.route('/Users/shreyassrinivasan/Desktop/SD_Lab', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'fullName' in request.form and 'emailID' in request.form and 'Username' in request.form and 'Password' in request.form:
        fullName = request.form['Full Name']
        email = request.form['Email address']
        username = request.form['Username']
        password = request.form['Create Password']
        confirm = request.form['Confirm Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z]'):
            msg = 'Name can only contain alphabetical characters'
        elif not username or not password or not email or not fullName:
            msg = 'Please fill out the form !'
        elif password != confirm:
            msg = 'Passwords do not match.'
        else:
            cursor.execute('INSERT INTO register VALUES (%s, % s, % s, % s)', (fullName,email,username,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg = msg)


if __name__ == '__main__':
    app.run(debug=True)