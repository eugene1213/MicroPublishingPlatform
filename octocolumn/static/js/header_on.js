$(document).ready(function(){
    getUserInfo();
});
$(function(){
    $('#header-profile-image').click(function(){
        $('.account-info').is(":visible")?$('.account-info').hide():$('.account-info').show();
    });
});
function getUserInfo() {

    $.ajax({
        url: "/api/member/userInfo/",
        async: true,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var point = json.user.point;
            var username = json.username;
            var nickname = json.user.nickname;
            var profile_image = json.profileImg.profile_image;

            $("#profile-container > .profile-text").text(nickname);
            $("#header-profile-image").css("background-image", "url("+profile_image+")");
            $('.point > .text > span').text(point);
        }
    });
}