$(document).ready(function(){

    getUserInfo();

    $(document).click(function(e){
        var windowHeight = window.innerHeight;
        var validLocate = window.innerWidth - $(".btn-user").width()-17;    // 유저버튼 위치
        
        if ( e.clientX > validLocate && e.clientY < 30 ){
            
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
            var nickname = json.user.nickname;
            var profile_image = json.profileImg.profile_image;

            $(".btn-point .point").text(point + "p");
            $(".btn-user > span").text(nickname);
            $(".btn-right-wrap > .btn-user img").attr("src", profile_image);

            loadCropImage("#header-profile-image")
        }
    });
}