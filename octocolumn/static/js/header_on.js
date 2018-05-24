$(document).ready(function(){
    getUserInfo();
});
$(function(){
    $('#header-profile-image').click(function(){
        
        $('.account-info').is(":visible")?$('.account-info').hide():$('.account-info').show();
    });
    //다른곳 클릭 시 닫힘
    $(document).mouseup(function(e) {
        
        var container = $(".account-info");
        
        if (!container.is(e.target) && container.has(e.target).length === 0){
        
            container.css("display","none");
        }	
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
            var pk = json.user.pk;

            $("#profile-container > .profile-text").text(nickname);
            $("#header-profile-image").css("background-image", "url("+profile_image+")");
            $('.point > .text > span').text(point);
            $(".setting").attr('onclick','window.location.href=/profile/'+pk);
        }
    });
}