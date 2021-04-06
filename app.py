# 載入Flask
from flask import Flask, redirect, request, render_template, session, jsonify, json
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
app.config["JSON_AS_ASCII"] = False


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

    mycursor.execute(
        'SELECT name,username,password FROM user WHERE username="' + username +
        '" AND password="' + pwd + '"')
    myresult = mycursor.fetchall()

    if myresult == []:
        return redirect('/error')
    elif myresult[0][1] == username and myresult[0][2] == pwd:
        name = myresult[0][0]
        session['name'] = name
        session['username'] = username
        return redirect('/member')


@app.route('/signout')
def signout():
    session.pop('username', None)
    return redirect('/')


@app.route('/member/')
def member():
    name = session.get('name')
    if 'name' in session:
        return render_template('./member.html', name=name)
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

    mycursor.execute('SELECT username FROM user where username="' + username +
                     '"')
    myresult = mycursor.fetchall()
    # print(myresult)

    if name == '' or username == '' or pwd == '':
        message = '不可為空'
        return redirect('/error/?message=' + message)

    elif myresult != []:
        message = '帳號已被註冊'
        return redirect('/error/?message=' + message)

    else:
        sql = 'INSERT INTO user (name, username, password) VALUES (%s, %s, %s)'
        val = (name, username, pwd)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect('/')


# week7


@app.route('/api/users')
def api():
    username = request.args.get('username', '')
    mycursor.execute('SELECT * FROM user WHERE username = "' + username + '"')
    myresult = mycursor.fetchall()
    if myresult == []:
        userfound = None
    else:
        userfound = {
            'id': myresult[0][0],
            'name': myresult[0][1],
            'username': myresult[0][2],
        }
    return {'data': userfound}


app.run(port=3000)
