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


@app.route('/input/', methods=['GET', 'POST'])
def test():
    a = request.form.get('input')
    print(a)
    return '我是后端'

@app.route('/login/',methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/user/')
def show_user_profile():
    # show the user profile for that user
    return render_template('user.html')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == '__main__':
    app.run(debug=True)