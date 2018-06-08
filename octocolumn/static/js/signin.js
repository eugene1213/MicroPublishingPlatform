$(document).ready(function(){

    $("#btn-signin").click(function() {
        signin_api();
    });
    $(".signin-main-container > input").keydown(function(e){
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
function modalSignin() {
    $('.welcome-container').css('display','block');
    $(".page").css("position", "fixed"); 
}
/* 로그인 창 좌우로 넘기기 */
function toggle() {
		$(".form-signin").toggleClass("form-signin-left");
        $(".form-signup").toggleClass("form-signup-left");
        $(".frame").toggleClass("frame-long");
        $(".signup-inactive").toggleClass("signup-active");
        $(".signin-active").toggleClass("signin-inactive");
        $(".forgot").toggleClass("forgot-left");   
        $(this).removeClass("idle").addClass("active");
}

$(function() {
	$(".btn-signup").click(function() {
        $(".nav").toggleClass("nav-up");
        $(".form-signup-left").toggleClass("form-signup-down");
        $(".success").toggleClass("success-left"); 
        $(".frame").toggleClass("frame-short");
	});
});

$(function() {
	$(".btn-signin").click(function() {
        $(".btn-animate").toggleClass("btn-animate-grow");
        $(".welcome").toggleClass("welcome-left");
        $(".cover-photo").toggleClass("cover-photo-down");
        $(".frame").toggleClass("frame-short");
        $(".profile-photo").toggleClass("profile-photo-down");
        $(".btn-goback").toggleClass("btn-goback-up");
        $(".forgot").toggleClass("forgot-fade");
	});
});
function signin_api() {
    var current_url = window.location.href;
    var tmpStr = current_url.split("/");
        isPreviewPage = tmpStr[tmpStr.length-3]=='preview';

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
            password: password
        },
        success: function(json) {

            if($("#checkbox-signin").prop("checked") == true){
                localStorage.setItem("id",email);
            }else {
                localStorage.setItem("id","");
            }
            if(isPreviewPage) window.location.href = current_url;
            else window.location.href = current_url;
        },
        error: function(error) {
            var msg = error.responseJSON.content.message
            var title = error.responseJSON.content.title
            error_modal(title, msg, false);
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