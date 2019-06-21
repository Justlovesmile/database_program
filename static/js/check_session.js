//定义所有的函数
//用于清除session
clear_session=function(){
    $.post('/clear-session/',{},function(ans){
        if(ans=='ok'){
            console.log("clear_session执行了")
            alert("退出登陆成功!")
            window.location.replace('/login/');
        }

    })
}

//用于检查session
check_session=function(){
    nickname=$.post('/check-session/',{},function(ans){
        console.log("check_session执行了")
            if (ans==""){
                console.log("获取session失败！")
                    return false
            }
            else{
                nickname=ans
                console.log('获取session成功！')
                $('#right_nav').html("<li  id='session_check_nav'><a href='/user/'> 欢迎: "+nickname+"</a></li>"+"<li><button id='logoutBtn' class='btn btn-default' style='margin-bottom: 10px;margin-left:15px;' onclick='clear_session()'> 注销 </button></li>")
            }  
    })
}

//定义所有的触发事件
window.onload = function(){
    check_session()
}

