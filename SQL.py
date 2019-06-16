import pymysql

def connect_db():
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
    conn = pymysql.connect(**database_info)
    cursor = conn.cursor()
    sql='show databases;'
    for i in cursor.fetchmany(cursor.execute(sql)):
        databases.append("".join(i))
    if u_db not in databases:
        create_db(cursor)
    else:
        use_db(cursor)
    
def create_db(cursor):
    c_sql="""
        CREATE DATABASE IF NOT EXISTS userprogram;

        USE userprogram;

        CREATE TABLE User (
        `user_id` int(11) NOT NULL,
        `nickname` varchar(50) NOT NULL,
        `passwd` varchar(50) NOT NULL,
        `name` varchar(50),
        `sex` varchar(8),
        `permission_level` int(4) not null,
        PRIMARY KEY (`user_id`)
        );

        insert  into `User`(`user_id`,`nickname`,`passwd`,`name`,`sex`,`permission_level`) values (1001,'1','1','沃利贝尔','男',5);

        CREATE TABLE Administrator(
            `Admin_id` int(11) NOT NULL,
            `nickname` varchar(50) NOT NULL,
            `passwd` varchar(50) NOT NULL,
            `name` varchar(50),
            `sex` varchar(10),
            `permission_level` int(4) not null,
            PRIMARY KEY (`Admin_id`)
            );
        
        insert  into Administrator(`Admin_id`,`nickname`,`passwd`,`name`,`sex`,`permission_level`) values (1,'至高管理员','justlovesmile','谢明杰','男',0);
        
        CREATE TABLE Posts (
            `post_id` int(11) NOT NULL,
            `title` varchar(50) NOT NULL,
            `content` varchar(100) NOT NULL,
            `author_id` int(11) NOT NULL,
            `time` date not null,
            PRIMARY KEY (`post_id`)
            );
        insert  into `Posts`(`post_id`,`title`,`content`,`author_id`,`time`) values (1,"Welcome to XMJ_BBS!","Here you can write your ideas and share with others easily.Let's start it!",1,'2019-6-17');
        
        CREATE TABLE `Comments` (
            `comment_id` int(11) NOT NULL,
            `post_id` int(11) NOT NULL,
            `content` varchar(50) NOT NULL,
            `author_id` int(11) NOT NULL,
            `time` date not null,
            PRIMARY KEY (`comment_id`)
            );"""
    try:
        a=c_sql.split(';')
        for i in a[:-1]:
            i=i+';'
            cursor.execute(i)

    except:
        dbreturn='创建失败！'
        #print(dbreturn)
    else:
        dbreturn='创建成功！'
        #print(dbreturn)
        use_db(cursor)

def use_db(cursor):
    u_sql='use userprogram;'
    try:
        cursor.execute(u_sql)
    except:
        dbreturn='使用失败！'
        #print(dbreturn)
    else:
        dbreturn="使用成功！"
        #print(dbreturn)

if __name__ =="__main__":
    connect_db()