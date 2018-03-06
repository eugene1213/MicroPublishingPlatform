$(document).ready(function(){

    $("#btn-signin").click(function() {
        signin_api();
    });
    $(".form_wrap > input").keydown(function(e){
        if(e.keyCode == 13){
            if($("#email-signin").val() != "" && $("#password-signin").val() != ""){
                signin_api();
            }
        }
    });
});

function signin_api() {

    console.log("signin_api 호출성공")
    var email = $("#email-signin").val();
    var password = $("#password-signin").val();

    $.ajax({
        url: "/api/member/login/",
        async: false,
        type: 'POST',
        dataType: 'json',
        xhrFields: {
            withCredentials: true
        },
        data: {
            username: email,
            password : password
        },
        success: function(json) {
            console.log("통신성공");
            var keepLoginStatus = json.token;
            if($("#checkbox-signin").prop("checked") == true){
                localStorage.setItem("tk",keepLoginStatus);
            }else {
                localStorage.setItem("tk","");
            }
            window.location.href = "/";
        },
        error: function(error) {
            console.log(error);
        }
    });
}