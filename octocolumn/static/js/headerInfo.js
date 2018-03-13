$(document).ready(function(){
    info2header();
});
function info2header() {

    $.ajax({
        url: "/api/member/userInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var username = json.user.nickname;
            var profile_image = json.profileImg.profile_image;
            var point = json.user.point;

            $(".btn-right-wrap > .btn-user > span").text(username);
            $(".btn-right-wrap > .btn-user > img").attr("src", profile_image);
            $(".btn-point > .point").text(point + "p");
        },
        error: function(error) {
            console.log(error);
        }
    });
}