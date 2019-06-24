drop database if exists userprogram;
        /*建立数据库，并使用*/
        CREATE DATABASE IF NOT EXISTS userprogram;
        USE userprogram;
        
        /*创建用户表*/
        CREATE TABLE `Users` (
            `user_id` int(11) unsigned unique NOT NULL AUTO_INCREMENT,
            `nickname` char(20) unique NOT NULL,
            `passwd` char(20) NOT NULL,
            `name` char(20),
            `sex` enum('男','女'),
            `email` char(20),
            `permission_level` tinyint(1) default 3,
            PRIMARY KEY (`user_id`),
            index id(user_id)
        )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        /*创建管理员表*/
        CREATE TABLE `Administrators`(
            `Admin_id` int(11) unsigned unique NOT NULL AUTO_INCREMENT,
            `nickname` char(20) unique NOT NULL,
            `passwd` char(20) NOT NULL,
            `name` char(20),
            `sex` enum('男','女'),
            `email` char(20),
            `permission_level` tinyint(1) default 1,
            PRIMARY KEY (`Admin_id`),
            index id(Admin_id)
            )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        /*创建帖子表*/
        CREATE TABLE `Posts` (
            `post_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
            `title` char(30) NOT NULL,
            `content` text NOT NULL,
            `author_id` int(11) unsigned NOT NULL,
            `time` datetime not null,
            PRIMARY KEY (`post_id`),
            foreign key (`author_id`) references users(`user_id`) on delete cascade,
            index id(post_id)
            )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        /*创建评论表*/
        CREATE TABLE `Comments` (
            `comment_id` int(11) AUTO_INCREMENT,
            `post_id` int(11) unsigned NOT NULL,
            `content` tinytext NOT NULL,
            `author_id` int(11) unsigned NOT NULL,
            `time` datetime not null,
            PRIMARY KEY (`comment_id`),
            foreign key (`author_id`) references users(`user_id`),
            foreign key (`post_id`) references posts(`post_id`) on delete cascade,
            index id(comment_id)
            )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;
        
        /*创建一系列视图*/
        create or replace view users_post_info as select user_id,nickname,post_id,title,content,posts.time from users,posts where author_id=user_id order by post_id desc;
        create or replace view users_comment_info as select user_id,nickname,post_id,comment_id,content,comments.time from users,comments where author_id=user_id order by comment_id desc;
        create or replace view users_info as select user_id,nickname,name,sex,email,permission_level from users;
        create or replace view admins_info as select Admin_id,nickname,name,sex,email,permission_level from administrators;
        create or replace view tongji as select count(DISTINCT user_id) as '用户数量',count(DISTINCT posts.post_id) as '帖子数量',count(DISTINCT comment_id) as '评论数量' from users,posts,comments;
        
        /*创建用户记录表，相当于以用户id分组统计，使用触发器添加数据*/
        create table `users_record_statistics`(
			`user_id` char(20) primary key not null,
            `post_num` int(11) default 0,
            `comment_num` int(11) default 0,
            `signup_time` datetime not null
        )DEFAULT CHARSET=utf8mb4 AUTO_INCREMENT=1;

        /*创建触发器*/
        DELIMITER ||
        create trigger users_signup_record after insert on users for each row
			begin
				insert into users_record_statistics (user_id,signup_time) values (new.user_id,NOW());
			end ||
		create trigger users_post_record after insert on posts for each row
			begin
            /*MySQL的安全模式=1条件下，where条件含主键才能修改*/
				SET SQL_SAFE_UPDATES = 0; 
				update users_record_statistics set post_num=post_num+1 where new.author_id=users_record_statistics.user_id;
                SET SQL_SAFE_UPDATES = 1;
			end ||
		create trigger users_comment_record after insert on comments for each row 
			begin
				SET SQL_SAFE_UPDATES = 0;
                update users_record_statistics set comment_num=comment_num+1 where new.author_id=users_record_statistics.user_id;
                SET SQL_SAFE_UPDATES = 1;
			end ||
		create trigger users_user_delete after delete on users for each row
			begin
				delete from users_record_statistics where users_record_statistics.user_id = old.user_id;
			end ||
		create trigger users_comment_delete after delete on comments for each row 
			begin
				SET SQL_SAFE_UPDATES = 0;
                update users_record_statistics set comment_num=comment_num-1 where old.author_id=users_record_statistics.user_id;
                SET SQL_SAFE_UPDATES = 1;
			end ||
		create trigger users_post_delete after delete on posts for each row
			begin
				SET SQL_SAFE_UPDATES = 0;
                update users_record_statistics set post_num=post_num-1 where old.author_id=users_record_statistics.user_id;
                SET SQL_SAFE_UPDATES = 1;
			end ||
		DELIMITER ;
        
        
        show triggers;
        /*数据初始化*/
        insert  into `Users`(`user_id`,`nickname`,`passwd`,`name`,`sex`,`email`,`permission_level`) values (1,'雷霆咆哮','qwer','沃利贝尔','男',null,5),(2,'1','1','1','男',null,5);
        insert  into `Administrators`(`Admin_id`,`nickname`,`passwd`,`name`,`sex`,`email`,`permission_level`) values (1,'至高管理员','justlovesmile','谢明杰','男','865717150@qq.com',0),(2,'1','1','JJ','男','666666666@qq.com',1);
        insert  into `Posts`(`post_id`,`title`,`content`,`author_id`,`time`) values (1,"Welcome to XMJ_BBS!","Here you can write your ideas and share with others easily.Let's start it!",1,NOW());
        insert into `Comments`(`comment_id`,`post_id`,`content`,`author_id`,`time`) values (1,1,"Oh,This's so nice!I will use this BBS!",1,NOW());