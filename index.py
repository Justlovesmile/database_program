from flask import Flask, render_template, request,session
import pymysql
import time
from datetime import timedelta,datetime
from check import check_db
import sql_api
import os
import json 


app = Flask(__name__)

#设置session参数
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。

#进入首页
@app.route('/', methods=['GET', 'POST'])
def index():
    check_db()
    return  render_template('index.html')

#检查seesion中是否保存用户名，若有，则说明用户已经登陆，返回用户名
@app.route('/check-session/',methods=['GET','POST'])
def check_session():
    if session.get('nickname'):
        nickname=session.get('nickname')
        #print(nickname)
        return nickname
    else:
        return ""

#设置session['post_id']
@app.route('/set-session-postid/',methods=['GET','POST'])
def set_session_post_id():
    session['post_id']=request.form.get('post_id')
    #print("session_post_id",session['post_id'])
    return "ok"

#获取session['post_id'],传到前端确认
@app.route('/get-session-postid/',methods=['GET','POST'])
def get_session_post_id():
    if session['post_id']:
        return session['post_id']
    else:
        return "error"

#注销登陆账号时清除session['nickname']
@app.route('/clear-session/',methods=['GET','POST'])
def clear_session():
    session.pop('nickname')
    print('clearsession')
    return 'ok'

#链接sql_api中的函数进行登陆时的用户检查，表取决于table参数
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

@app.route('/check-permission/',methods=['GET','POST'])
def check_permission():
    return session['table']

#进入登陆界面
@app.route('/login/',methods=['GET','POST'])
def login():
    return render_template('login.html')

#进入用户个人空间页面
@app.route('/user/',methods=['GET','POST'])
def show_user():
    # show the user profile for that user
    return render_template('user.html')

#进入注册页面
@app.route('/signup/',methods=['GET','POST'])
def signup():
    return render_template('signup.html')

#链接sql_api中的函数，向数据库中添加用户
@app.route('/signup-check/',methods=['GET','POST'])
def signup_check():
    nickname=request.form.get('nickname')
    passwd=request.form.get('passwd')
    name=request.form.get('name')
    sex=request.form.get('sex')
    email=request.form.get('email')
    ans=sql_api.insert_users(nickname,passwd,name,sex,email)
    return ans

#向数据库中添加帖子，会检查会话session，若用户未登陆则返回nosession
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

#进入最新帖子页面
@app.route('/newpost/',methods=['GET','POST'])
def newpost():
    return render_template('newpost.html')

#用于获取数据库帖子，待改进（改进方向：只显示前10（或20）个帖子，有时间再改）
#写的这么繁琐是因为json不能编码datetime类型，只能先取出来改成字符串，再添进列表再json.dumps()
@app.route('/get-post/',methods=['GET','POST'])
def get_post():
    post_id=request.form.get('post_id')
    #如果前端传的空字典
    if None==post_id:
        #获取全部帖子
        ans=sql_api.selectall_db('users_post_info')
        #print(type(ans),ans)
        posts=eachline(ans)
        return json.dumps(posts)
    #如果前端传了post_id
    else:
        #获取特定帖子
        ans=sql_api.select_all_bynum('users_post_info','post_id',post_id)
        #print("ans——————————————————",ans)
        posts=eachline(ans)
        return json.dumps(posts)

#对于每一个帖子，点击链接会进入不同的'/url/'
#flask使用use_for()带参url传值，还不太会！
@app.route('/comment/<name>',methods=['GET','POST'])
def comment(name):
    return render_template('comment.html')

#用于向数据库插入评论内容，会检查session，用户未登录，则返回“nosession”
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

@app.route('/get-comment/',methods=['GET','POST'])
def get_comment():
    ans=sql_api.select_all_bystr('users_comment_info','post_id',session['post_id'])
    #print(type(ans),ans)
    comments=eachline(ans)
    #session.pop('post_id')
    return json.dumps(comments)

#进入搜索页面
@app.route('/search/',methods=['GET','POST'])
def search():
    return render_template('search.html')

#实现搜索
@app.route('/search-key/',methods=['GET','POST'])
def search_key():
    key=request.form.get('key')
    value= request.form.get('value')
    #获取用户全部帖子信息
    ans1=sql_api.select_mohu('users_post_info',key,value)
    answers=eachline(ans1)
    #获取用户全部评论信息
    if key!='title':
        ans2=sql_api.select_mohu('users_comment_info',key,value)
        #print('返回的信息：',ans2)
        for i in eachline(ans2):
            answers.append(i)
    #print('你输入了',value)
    #print('ans',answers)
    if len(answers)==0:
        return "empty"
    return json.dumps(answers)

#获取用户信息
@app.route('/get-user-info/',methods=['GET','POST'])
def get_user_info():
    if session['table']=='users':
        ans=sql_api.select_all_bystr('users_info','nickname',request.form.get('nickname'))
    else:
        ans=sql_api.select_all_bystr('admins_info','nickname',request.form.get('nickname'))
    return json.dumps(ans)

#获取用户记录
@app.route('/get-user-post-comment/',methods=['GET','POST'])
def get_user_post_comment():
    if session['table']=='users':
        key=request.form.get('key')
        value= request.form.get('value')
        #获取用户全部帖子信息
        ans1=sql_api.select_all_bystr('users_post_info',key,value)
        answers=eachline(ans1)
        #获取用户全部评论信息
        ans2=sql_api.select_all_bystr('users_comment_info',key,value)
        #print('返回的信息：',ans2)
        for i in eachline(ans2):
            answers.append(i)
        #print('你输入了',value)
        #print('ans',answers)
        if len(answers)==0:
            return "empty"
        return json.dumps(answers)
    else:
        ans1=sql_api.select_all_bynum('users_post_info',1,1)
        #print(ans1)
        answers=eachline(ans1)
        ans2=sql_api.select_all_bynum('users_comment_info',1,1)
        for i in eachline(ans2):
            answers.append(i)
        if len(answers)==0:
            return "empty"
        return json.dumps(answers)


#执行删除操作
@app.route('/delete/',methods=['GET','POST'])
def delete():
    if request.form.get('table')=='posts':
        ans=sql_api.delete_db('posts','post_id',request.form.get('id'))
        return ans
    else:
        ans=sql_api.delete_db('comments','comment_id',request.form.get('id'))
        return ans

#执行更新操作
@app.route('/update/',methods=['GET','POST'])
def update():
    nickname=request.form.get('nickname')
    name=request.form.get('name')
    sex=request.form.get('sex')
    email=request.form.get('email')
    if session['table']=='users':
        user_id=sql_api.select_str_db('users','user_id','nickname',session['nickname'])[0][0]
        u_sql=f"update users set nickname='{nickname}',name='{name}',sex='{sex}',email='{email}' where user_id={user_id};"
    else:
        user_id=sql_api.select_str_db('administrators','Admin_id','nickname',session['nickname'])[0][0]
        u_sql=f"update administrators set nickname='{nickname}',name='{name}',sex='{sex}',email='{email}' where Admin_id={user_id};"
    ans=sql_api.update_db(u_sql)
    session['nickname']=nickname
    return ans
#进入简介页面
@app.route('/introduce/',methods=['GET','POST'])
def introduce():
    return render_template('introduce.html')

#处理参数中的每一行，变量名懒得改了，并不是对应变量名
def eachline(ans):
    answers=[]
    for eachline in ans:
        user_id=eachline[0]
        nickname=eachline[1]
        post_id=eachline[2]
        title=eachline[3]
        content=eachline[4]
        nowtime=eachline[5].strftime("%Y-%m-%d %H:%M:%S")#将datetime类型转成str
        answers.append((user_id,nickname,post_id,title,content,nowtime))
    return answers

if __name__ == '__main__':
    app.run(debug=True)