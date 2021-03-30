# 載入Flask
from flask import Flask, redirect, request, render_template, session
import mysql.connector

mydb = mysql.connector.connect(host='localhost',
                               user='root',
                               password='password',
                               database='website')

mycursor = mydb.cursor()

# # # # # # # # # # # # # # # # # # # # #

# 建立app物件
app = Flask(
    __name__,
    static_folder='templates',  # 對應資料夾名稱
    static_url_path='/'  # 資料夾對應的網址
)

app.secret_key = 'jkdkowu48g'


# 建立網站首頁的回應方式
@app.route('/')
def index():
    if 'username' in session:
        return redirect('./member')
    else:
        return render_template('/index.html')


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    pwd = request.form['pwd']

    mycursor.execute('SELECT username,password FROM user')
    myresult = mycursor.fetchall()
    signin = False
    for x in myresult:
        if x[0] == username and x[1] == pwd:
            signin = True
            session['username'] = username
            return redirect('/member')
    if signin == False:
        return redirect('/error')


@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect('/')


@app.route('/member')
def member():
    username = session.get('username')
    if 'username' in session:
        return render_template('./member.html', name=username)
    else:
        return redirect('/')


@app.route('/error')
def error():
    if 'username' in session:
        return redirect('./member')
    else:
        message = '帳號或密碼錯誤'
        return redirect('/error/?message=' + message)


@app.route('/error/')
def errorPage():
    message = request.args.get('message', '錯誤')
    return render_template('./error.html', message=message)


@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    username = request.form['username']
    pwd = request.form['pwd']

    mycursor.execute('SELECT username FROM user')
    myresult = mycursor.fetchall()
    addAccount = True
    for x in myresult:
        if x[0] == username:
            addAccount = False
            break

    if name == '' or username == '' or pwd == '':
        message = '不可為空'
        return redirect('/error/?message=' + message)

    if addAccount == False:
        message = '帳號已被註冊'
        return redirect('/error/?message=' + message)

    else:
        sql = 'INSERT INTO user (name, username, password) VALUES (%s, %s, %s)'
        val = (name, username, pwd)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect('/')


app.run(port=3000)
