from flask import Flask, render_template, request
import pymysql
import time
from check import check_db
import sql_api
import main

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return  render_template('index.html')


@app.route('/login-check/', methods=['GET', 'POST'])
def logincheck():
    nickname = request.form.get('nickname')
    passwd = request.form.get('passwd')
    print(passwd)
    ans=sql_api.logincheck(nickname,passwd)
    print(ans)
    return ans

@app.route('/login/',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/user/',methods=['GET','POST'])
def show_user_profile():
    # show the user profile for that user
    return render_template('user.html')

@app.route('/signup/',methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route('/newpost/',methods=['GET','POST'])
def newpost():
    return render_template('newpost.html')

@app.route('/search/',methods=['GET','POST'])
def search():
    return render_template('search.html')

@app.route('/introduce/',methods=['GET','POST'])
def introduce():
    return render_template('introduce.html')

if __name__ == '__main__':
    app.run(debug=True)