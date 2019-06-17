'''
XMJ的bbs用户信息管理系统
start_date:2019-6-17
'''
import pymysql
import time
from check import check_db
import sql_api
import index

now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

def main():
    check_db()

