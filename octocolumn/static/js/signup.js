
function signup_api(){

    var nickName = $("#nickName-signup").val().trim();
    var email = $("#email-signup").val().trim();
    var password1 = $("#password1-signup").val().trim();
    var password2 = $("#password2-signup").val().trim();

    $.ajax({
        url: "/api/member/signup/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            nickname: nickName,
            username : email,
            password1 : password1,
            password2 : password2
        },
        success: function(json) {
            console.log("통신성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}