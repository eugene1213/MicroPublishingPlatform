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
            console.log(json.user);
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