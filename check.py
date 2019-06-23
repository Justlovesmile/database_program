import pymysql
import time

def check_db():
    databases=[]
    database_info={
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'Xmj987536',
        'db': 'xiemingjiedemo',
        'charset': 'utf8'
        }
    # 打开数据库连接
    u_db='userprogram'
    try:
        conn = pymysql.connect(**database_info)
    except:
        print("(check)连接失败！")
    else:
        print("(check)连接成功！")
        cursor = conn.cursor()
        sql='show databases;'
        for i in cursor.fetchmany(cursor.execute(sql)):
            databases.append("".join(i))
        if u_db not in databases:
            print('数据库未建立，请使用create_db.sql文件建立')
        else:
            print('(check)找到数据库')
            conn.close()

if __name__=='__main__':
    check_db()