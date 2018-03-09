
function signup_api(){

    var nickName = $("#nickName-signup").val().trim();
    var email = $("#email-signup").val().trim();
    var password1 = $("#password1-signup").val().trim();
    var password2 = $("#password2-signup").val().trim();

    $.ajax({
        url: "http://127.0.0.1:8000/api/member/signup/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            nick_name: nickName,
            username : email,
            password1 : password1,
            password2 : password2
        },
        success: function(json) {
            console.log("통신성공");
            check_email();
        },
        error: function(error) {
            console.log(error);
        }
    });
}