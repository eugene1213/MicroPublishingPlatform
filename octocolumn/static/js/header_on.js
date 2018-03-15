$(document).ready(function(){

    getUserInfo();

    $("body").click(function(e){
        
        validLocate = window.innerWidth - $(".btn-user").width()-17;    // 유저버튼 위치
        if( e.clientX > validLocate && e.clientY < 30 ){
            
            window.location.href = "/profile/"
        }
    });
});

function getUserInfo() {

    $.ajax({
        url: "/api/member/userInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {
            
            var point = json.user.point;
            var username = json.username;
            var first_name = json.user.first_name;
            var last_name = json.user.last_name;
            var profileImg = json.profileImg;

            $(".btn-point .point").text(point + "p");
            $(".btn-user > span").text(first_name + " " + last_name);
        }
    });
}