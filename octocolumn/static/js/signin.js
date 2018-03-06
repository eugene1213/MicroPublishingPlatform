
function signin_api() {

    var email = $("#email-signin").val();
    var password = $("#password-signin").val();

    $.ajax({
        url: "http://127.0.0.1:8000/member/login/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            username: email,
            password : password
        },
        success: function(json) {
            console.log("통신성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}