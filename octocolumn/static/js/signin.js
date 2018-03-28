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
    $("#btn2ndInvite").unbind('click').click(function(){

        secondInvite();
    });
});

function signin_api() {

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

            if($("#checkbox-signin").prop("checked") == true){
                localStorage.setItem("id",email);
            }else {
                localStorage.setItem("id","");
            }
            window.location.href = "/";
        },
        error: function(error) {
            if(error.status == 401) {
                modal({
                    type: 'alert',
                    title: '알림',
                    text: '아이디와 비밀번호를 확인해 주십시오',

                });
            }
        }
    });
}


function secondInvite() {

    var email  = $("#email").val();

    $.ajax({
        url: "/api/member/secondInvite/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            email: email
        },
        success: function(json) {

            alert('감사합니다.');
        },
        error: function(error) {
            console.log(error);
        }
    });
}

