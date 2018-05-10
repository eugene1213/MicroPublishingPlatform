$(function(){//email발송
    $("#btnFindPass").unbind('click').click(function(){
        findPass();
    });
    $("#email-findPW").keypress(function(e){
        
        if(e.keyCode == 13) findPass();
    });
});
$(function(){//패스워드 리셋
    $("#btnResetPass").unbind('click').click(function(){
        
        resetPass();
    });
    $("#pass2").keypress(function(e){
        
        if(e.keyCode == 13) resetPass();
    });
});
function findPass() {
    
    var username = $('#email-findPW').val();
    console.log(username)
    $.ajax({
        url: "/api/member/passwordResetEmail/",
        async: true,
        type: 'POST',
        dataType: 'json',
        data: {
            username: username
        },
        success: function(json) {
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: 'Check your inbox', //Modal Title
                text: '메일을 확인하세요.', //Modal HTML Content
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
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function resetPass() {
    
    var url = window.location.href;
    var token = url.split('/')[url.split('/').length-2];
    var uid = url.split('/')[url.split('/').length-3];
    var pass1 = $('#pass1').val();
    var pass2 = $('#pass2').val();
    
    $.ajax({
        url: "/api/member/passwordReset/",
        async: true,
        type: 'POST',
        dataType: 'json',
        data: {
            uid: uid,
            token: token,
            password1: pass1,
            password2: pass2
        },
        success: function(json) {

            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: '비밀번호 변경 성공', //Modal Title
                text: '클릭하면 로그인 페이지로 이동합니다.', //Modal HTML Content
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
            window.location.href = '/signinForm/';
        },
        error: function(error) {
            console.log(error);
        }
    });
}