from flask import Flask, render_template, request,session
import pymysql
import time
from datetime import timedelta,datetime
from check import check_db
import sql_api
import main
import os
import json 


app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。

@app.route('/', methods=['GET', 'POST'])
def index():
    check_db()
    return  render_template('index.html')

@app.route('/check-session/',methods=['GET','POST'])
def check_session():
    if session.get('nickname'):
        nickname=session.get('nickname')
        #print(nickname)
        return nickname
    else:
        return ""

@app.route('/clear-session/',methods=['GET','POST'])
def clear_session():
    session.pop('nickname')
    print('clearsession')
    return 'ok'

@app.route('/login-check/', methods=['GET', 'POST'])
def logincheck():
    nickname = request.form.get('nickname')
    passwd = request.form.get('passwd')
    table = request.form.get('table')
    ans=sql_api.logincheck(table,nickname,passwd)
    if ans=="ok":
        session['nickname']=nickname
        session['table']=table
    return ans

@app.route('/login/',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/user/',methods=['GET','POST'])
def show_user():
    # show the user profile for that user
    return render_template('user.html')

@app.route('/signup/',methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/signup-check/',methods=['GET','POST'])
def signup_check():
    nickname=request.form.get('nickname')
    passwd=request.form.get('passwd')
    name=request.form.get('name')
    sex=request.form.get('sex')
    email=request.form.get('email')
    ans=sql_api.insert_users(nickname,passwd,name,sex,email)
    return ans

@app.route('/post-content/',methods=['GET','POST'])
def post_content():
    title=request.form.get('title')
    content=request.form.get('content')
    if session.get("nickname"):
        author_id=sql_api.select_str_db('users','user_id','nickname',session.get('nickname'))[0][0]
        #print('author_id',author_id)
        ans=sql_api.insert_posts(title,content,author_id)
        #print(ans)
        return ans
    else:
        #print('error')
        return "nosession"

@app.route('/newpost/',methods=['GET','POST'])
def newpost():
    return render_template('newpost.html')

@app.route('/get-post/',methods=['GET','POST'])
def get_post():
    ans=sql_api.selectall_db('users_post_info')
    #print(type(ans),ans)
    posts=[]
    for eachline in ans:
        user_id=eachline[0]
        nickname=eachline[1]
        title=eachline[2]
        content=eachline[3]
        author_id=eachline[4]
        nowtime=eachline[5].strftime("%Y-%m-%d %H:%M:%S")
        posts.append((user_id,nickname,title,content,author_id,nowtime))
    return json.dumps(posts)

@app.route('/newcomment/',methods=['GET','POST'])
def newcomment():
    return render_template('newcomment.html')

@app.route('/comment-content/',methods=['GET','POST'])
def commment_content():
    post_id=request.form.get('post_id')
    content=request.form.get('content')
    if session.get("nickname"):
        author_id=sql_api.select_str_db('users','user_id','nickname',session.get('nickname'))[0][0]
        #print('author_id',author_id)
        ans=sql_api.insert_comments(post_id,content,author_id)
        #print(ans)
        return ans
    else:
        #print('error')
        return "nosession"

@app.route('/search/',methods=['GET','POST'])
def search():
    return render_template('search.html')

@app.route('/introduce/',methods=['GET','POST'])
def introduce():
    return render_template('introduce.html')



if __name__ == '__main__':
    app.run(debug=True)