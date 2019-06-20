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
            create_db(conn)
            conn.close()
        else:
            use_db(conn)
            conn.close()

def create_db(conn):
    cursor = conn.cursor()
    now=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    c_sql=f"""
        CREATE DATABASE IF NOT EXISTS userprogram;

        USE userprogram;

        CREATE TABLE `Users` (
            `user_id` int(11) unsigned unique NOT NULL AUTO_INCREMENT,
            `nickname` char(20) unique NOT NULL,
            `passwd` char(20) NOT NULL,
            `name` char(20),
            `sex` char(1),
            `email` char(20),
            `permission_level` tinyint(1) default 3,
            PRIMARY KEY (`user_id`)
        )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;

        insert  into `Users`(`user_id`,`nickname`,`passwd`,`name`,`sex`,`email`,`permission_level`) values (1,'雷霆咆哮','qwer','沃利贝尔','男',null,5),(2,'1','1','1','男',null,5);
        
        CREATE TABLE `Administrators`(
            `Admin_id` int(11) unsigned unique NOT NULL AUTO_INCREMENT,
            `nickname` char(20) unique NOT NULL,
            `passwd` char(20) NOT NULL,
            `name` char(20),
            `permission_level` tinyint(1) default 1,
            PRIMARY KEY (`Admin_id`)
            )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        insert  into `Administrators`(`Admin_id`,`nickname`,`passwd`,`name`,`permission_level`) values (1,'至高管理员','justlovesmile','谢明杰',0),(2,'1','1','JJ',1);

        CREATE TABLE `Posts` (
            `post_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `title` char(20) NOT NULL,
            `content` text NOT NULL,
            `author_id` int(11) unsigned NOT NULL,
            `time` datetime not null,
            PRIMARY KEY (`post_id`),
            foreign key (`author_id`) references users(`user_id`)
            )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        insert  into `Posts`(`post_id`,`title`,`content`,`author_id`,`time`) values (1,"Welcome to XMJ_BBS!","Here you can write your ideas and share with others easily.Let's start it!",1,'{now}');
        
        CREATE TABLE `Comments` (
            `comment_id` int(11) AUTO_INCREMENT,
            `post_id` int(11) unsigned NOT NULL,
            `content` tinytext NOT NULL,
            `author_id` int(11) unsigned NOT NULL,
            `time` datetime not null,
            PRIMARY KEY (`comment_id`),
            foreign key (`author_id`) references users(`user_id`),
            foreign key (`post_id`) references posts(`post_id`)
            )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        insert into `Comments`(`comment_id`,`post_id`,`content`,`author_id`,`time`) values (1,1,"Oh,This's so nice!I will use this BBS!",1,'{now}');
        
        create view users_post_info as select user_id,nickname,post_id,title,content,posts.time from users,posts where author_id=user_id order by post_id desc;
        create view users_comment_info as select user_id,nickname,post_id,comment_id,content,comments.time from users,comments where author_id=user_id order by comment_id desc;
        create view users_info as select user_id,nickname,sex,email from users;"""
    try:
        a=c_sql.split(';')
        for i in a[:-1]:
            i=i+';'
            cursor.execute(i)
    except:
        conn.rollback()
        print('(check)创建失败！')
    else:
        print('(check)创建成功！')
        use_db(conn)

def use_db(conn):
    cursor = conn.cursor()
    u_sql='use userprogram;'
    try:
        cursor.execute(u_sql)
    except:
        conn.rollback()
        dbreturn='(check)使用失败！'
        print(dbreturn)
    else:
        dbreturn="(check)使用成功！"
        print(dbreturn)

