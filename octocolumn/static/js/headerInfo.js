function info2header() {

    $.ajax({
        url: "/api/member/userInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var username = json.username;
            var profile_image = json.profile_image;
            var point = json.point;

            $(".btn-right-wrap > btn-user > span").text(username);
            $(".btn-right-wrap > btn-user > img").text(profile_image);
            $(".btn-point > .point").text(point + "p");
        },
        error: function(error) {
            console.log(error);
        }
    });
}