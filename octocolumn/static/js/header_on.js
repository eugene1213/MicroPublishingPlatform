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
            var point = json.point;
            var username = json.username;
            var first_name = json.first_name;
            var last_name = json.last_name;
            var profileImg = json.profileImg;

            $(".btn-point .point").text(point);
            $(".btn-user > span").text(first_name + " " + last_name);
        }
    });
}