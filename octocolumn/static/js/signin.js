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
                var errMsgTitle = 'Sign in Failed';
                var errMsg = '이메일과 비밀번호를 확인해 주시기바랍니다.';
              // alertBoxFocus('이메일과 비밀번호를 확인해 주시기바랍니다.',401)
            }
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: errMsgTitle, //Modal Title
                text: errMsg, //Modal HTML Content
                size: 'normal', //Modal Size (normal | large | small)
                buttons: [{
                    text: 'OK', //Button Text
                    val: 'ok', //Button Value
                    eKey: true, //Enter Keypress
                    addClass: 'btn-light-blue', //Button Classes (btn-large | btn-small | btn-green | btn-light-green | btn-purple | btn-orange | btn-pink | btn-turquoise | btn-blue | btn-light-blue | btn-light-red | btn-red | btn-yellow | btn-white | btn-black | btn-rounded | btn-circle | btn-square | btn-disabled)
                    onClick: function(argument) {
                        console.log(argument);
                        alert('Look in console!');
                    }
                }, ],
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
                buttonText: {
                    ok: 'OK',
                    yes: 'Yes',
                    cancel: 'Cancel'
                },
                template: '<div class="modal-box"><div class="modal-inner"><div class="modal-title"><a class="modal-close-btn"></a></div><div class="modal-text"></div><div class="modal-buttons"></div></div></div>',
                _classes: {
                    box: '.modal-box',
                    boxInner: ".modal-inner",
                    title: '.modal-title',
                    content: '.modal-text',
                    buttons: '.modal-buttons',
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

