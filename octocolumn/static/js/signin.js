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
/* 로그인 창 좌우로 넘기기 */
// $(function() {
// 	$(".btn").click(function() {
// 		$(".form-signin").toggleClass("form-signin-left");
//         $(".form-signup").toggleClass("form-signup-left");
//         $(".frame").toggleClass("frame-long");
//         $(".signup-inactive").toggleClass("signup-active");
//         $(".signin-active").toggleClass("signin-inactive");
//         $(".forgot").toggleClass("forgot-left");   
//         $(this).removeClass("idle").addClass("active");
// 	});
// });

// $(function() {
// 	$(".btn-signup").click(function() {
//         $(".nav").toggleClass("nav-up");
//         $(".form-signup-left").toggleClass("form-signup-down");
//         $(".success").toggleClass("success-left"); 
//         $(".frame").toggleClass("frame-short");
// 	});
// });

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
$(window).keypress(function(e){
    if(e.keyCode=='13') signin_api();
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
            password: password
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
                var errMsgTitle = 'Sign in Failed';
                var errMsg = '이메일과 비밀번호를 확인해 주시기바랍니다.';
              // alertBoxFocus('이메일과 비밀번호를 확인해 주시기바랍니다.',401)
            }else {
                var errMsgTitle = 'Fatal error';
                var errMsg = '알 수 없는 에러가 발생했습니다. 고객센터에 문의해주세요.';
            }
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: errMsgTitle, //Modal Title
                text: errMsg, //Modal HTML Content
                size: 'normal', //Modal Size (normal | large | small)
                center: true, //Center Modal Box?
                autoclose: false, //Auto Close Modal Box?
                callback: null, //Callback Function after close Modal (ex: function(result){alert(result);})
                onShow: function(r) {}, //After show Modal function
                closeClick: true, //Close Modal on click near the box
                closable: true, //If Modal is closable
                theme: 'atlant', //Modal Custom Theme
                animate: false, //Slide animation
                background: 'rgba(0,0,0,0.35)', //Background Color, it can be null
                zIndex: 1050, //z-index
                template: '<div class="modal-box"><div class="modal-inner"><div class="modal-title"><a class="modal-close-btn"></a></div><div class="modal-text"></div></div></div>',
                _classes: {
                    box: '.modal-box',
                    boxInner: ".modal-inner",
                    title: '.modal-title',
                    content: '.modal-text',
                    closebtn: '.modal-close-btn'
                }
            });
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

