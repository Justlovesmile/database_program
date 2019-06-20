import pymysql
import time


def connect_db():
    database_info={
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'passwd': 'Xmj987536',
        'db': 'userprogram',
        'charset': 'utf8mb4'
        }
    # 打开数据库连接
    try:
        conn = pymysql.connect(**database_info)
    except:
        print("(sql_api)连接失败！")
    else:
        print("(sql_api)连接成功!")
        return conn

def selectall_db(table):
    #select * from {table}
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select * from {table};"
    try:
        ans=cursor.fetchmany(cursor.execute(s_sql))    
    except:
        conn.close()
        return "error"
    else:
        conn.close()
        return ans

def select_str_db(table,need,key,value):
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select {need} from {table} where {key}='{value}';" 
    #print(s_sql)
    try:
        ans=cursor.fetchmany(cursor.execute(s_sql))    
    except:
        conn.close()
        #print('error')
        return "error"
    else:
        conn.close()
        return ans

def select_num_db(table,need,key,value):
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select {need} from {table} where {key}={value};" 
    try:
        ans=cursor.fetchmany(cursor.execute(s_sql))    
    except:
        conn.close()
        return "error"
    else:
        conn.close()
        return ans

def insert_users(nickname,passwd,name,sex,email):
    # insert into {table} {**data.keys()}vaule {**data.values()}
    conn=connect_db()
    cursor=conn.cursor()
    i_sql=f"insert into users (nickname,passwd,name,sex,email) values ('{nickname}','{passwd}','{name}','{sex}','{email}');"
    print(i_sql)
    try:
        cursor.execute(i_sql)
        conn.commit()
    except:
        conn.rollback()
        conn.close()
        return "error"
    else:    
        conn.close()
        return "ok"
    
def insert_posts(title,content,author_id):
    # insert into {table} {**data.keys()}vaule {**data.values()}
    now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    conn=connect_db()
    cursor=conn.cursor()
    i_sql=f"insert into posts (title,content,author_id,time) values ('{title}','{content}',{author_id},'{now}');"
    #print(i_sql)
    try:
        cursor.execute(i_sql)
        conn.commit()
    except:
        conn.rollback()
        conn.close()
        return "error"
    else:    
        conn.close()
        return "ok"

def insert_comments(post_id,content,author_id):
    # insert into {table} {**data.keys()}vaule {**data.values()}
    now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    conn=connect_db()
    cursor=conn.cursor()
    i_sql=f"insert into comments (post_id,content,author_id,time) values ('{post_id}','{content}',{author_id},'{now}');"
    #print(i_sql)
    try:
        cursor.execute(i_sql)
        conn.commit()
    except:
        conn.rollback()
        conn.close()
        return "error"
    else:    
        conn.close()
        return "ok"

def delete_db(table,**data):
    #删除data={'key':'value'}中当key=value的元组
    conn=connect_db()
    cursor=conn.cursor()
    key=tuple(data.keys())[0]
    value=tuple(data.values())[0]
    d_sql=f"delete from {table} where {key}={value};"
    #print(d_sql)
    try:
        cursor.execute(d_sql)
        conn.commit()
    except:
        conn.rollback()
        conn.close()
        return "error"
    else:
        conn.close()
        return "ok"

def update_db(table,**data):
    #修改数据
    conn=connect_db()
    cursor=conn.cursor()
    key1=tuple(data.keys())[0]
    value1=tuple(data.values())[0]
    key2=tuple(data.keys())[1]
    value2=tuple(data.values())[1]
    u_sql=f"update {table} set {key1}={value1} where {key2}={value2};"
    #print(d_sql)
    try:
        cursor.execute(u_sql)
        conn.commit()
    except:
        conn.rollback()
        conn.close()
        return "error"
    else:
        conn.close()
        return "ok"

def logincheck(table,nickname,passwd):
    conn=connect_db()
    cursor=conn.cursor()
    u_sql=f"select passwd from {table} where nickname='{nickname}';"
    #print(u_sql)
    try:
        cursor.execute(u_sql)
        ans=cursor.fetchall()[0][0]
        #print(ans)
        #print(passwd)
        conn.commit()
    except:
        conn.rollback()
        conn.close()
        return "error"
    else:
        if passwd==ans:
            conn.close()
            return "ok"
        else:
            conn.close()
            return "error"