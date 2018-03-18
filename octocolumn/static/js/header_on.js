$(document).ready(function(){

    getUserInfo();
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