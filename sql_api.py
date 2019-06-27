import pymysql
import time

#用于下面每个函数链接数据库的函数，会返回conn
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

#选出 * 的函数
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

#通过value选出数据的函数，value是字符串
def select_str_db(table,need,key,value):
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select {need} from {table} where {key}=binary'{value}';" 
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

#通过value选出数据的函数，value是数值
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

#通过value选出符合条件的所有,value是字符串
def select_all_bystr(table,key,value):
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select * from {table} where {key}=binary'{value}';" 
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

#通过value选出符合条件的所有，value是数值
def select_all_bynum(table,key,value):
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select * from {table} where {key}={value};" 
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

#模糊查找
def select_mohu(table,key,value):
    conn=connect_db()
    cursor=conn.cursor()
    s_sql=f"select * from {table} where {key} like '%{value}%';" 
    #print(s_sql)
    try:
        ans=cursor.fetchmany(cursor.execute(s_sql))
        #print(ans)
    except:
        conn.close()
        #print('error')
        return "error"
    else:
        conn.close()
        return ans

#添加用户函数
def insert_users(nickname,passwd,name,sex,email):
    # insert into {table} {**data.keys()}vaule {**data.values()}
    conn=connect_db()
    cursor=conn.cursor()
    i_sql=f"insert into users (nickname,passwd,name,sex,email) values ('{nickname}','{passwd}','{name}','{sex}','{email}');"
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

#向数据库中添加帖子函数    
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

#向数据库中添加评论函数
def insert_comments(post_id,content,author_id):
    # insert into {table} {**data.keys()}vaule {**data.values()}
    now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    conn=connect_db()
    cursor=conn.cursor()
    i_sql=f"insert into comments (post_id,content,author_id,time) values ({post_id},'{content}',{author_id},'{now}');"
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

#删除数据的函数
def delete_db(table,key,value):
    #删除data={'key':'value'}中当key=value的元组
    conn=connect_db()
    cursor=conn.cursor()
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

#更新数据函数，暂时还没用上
def update_db(u_sql):
    #修改数据
    conn=connect_db()
    cursor=conn.cursor()
    #print(u_sql)
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

#登陆时检查用户是否存在的函数
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