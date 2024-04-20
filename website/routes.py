from flask import render_template, url_for, redirect, request, session
from website import app
import psycopg2

def db_conn():
    conn = psycopg2.connect(database="flaskdb", host="localhost", user="flaskuser",password="flaskpwd",port="5432")
    return conn

@app.route('/signup', methods=['GET','POST'])
def signup():
    conn=db_conn()
    cur = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        
        selectExistingUserQuery = f'''SELECT * from student where username='{username}';'''
        cur.execute(selectExistingUserQuery)
        data1 = cur.fetchone()
        selectExistingEmailQuery = f'''SELECT * from student where email='{email}';'''
        cur.execute(selectExistingEmailQuery)
        data2 = cur.fetchone()
        
        
        if data1 != None or data2 != None:
            return "Username or email already exists. Please choose another one."
        
        cur.execute("INSERT INTO student (email, pwd, username) VALUES (%s, %s, %s);", (email, password,username))
        conn.commit()
        return redirect(url_for('login'))

    return render_template("signup.html")

@app.route('/login', methods=['GET','POST'])
def login():
    conn=db_conn()
    cur = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        getStudentId = f'''Select * from student where username='{username}';'''
        cur.execute(getStudentId)
        data = cur.fetchone()
        
        studentid=data[0]
        pwd=data[2]
        #print (studentid, pwd)
        if studentid == None :
            return "User account Does not exist. Please Signup."
        else :
            if password != pwd :
                return "Incorrect password."
            else :
                return redirect(url_for('dashboard',studentId=studentid))

    return render_template("login.html")

@app.route('/<int:studentId>/dashboard')
def dashboard(studentId):
    return render_template('dashboard.html',studentId=studentId)

@app.route('/')
def home():
    return render_template("home.html")
