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
            nickname  : nickName,
            username  : email,
            password1 : password1,
            password2 : password2
        },
        success: function(json) {
            $(".welcome2 > span").text($("#email-signup").val());
            var msgTitle = 'Check your inbox';
            var msg = '<span>'+ email +'</span>에 대한 확인 링크를 이메일로 보내 드렸습니다.<br>해당 이메일의 받은 편지함을 열어서, 메일에 포함된 링크를 클릭하여 계정 설정을 완료하세요.<br>';
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: msgTitle, //Modal Title
                text: msg, //Modal HTML Content
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

$(function(){
    $(".agree_checkbox").click(function(){

        if($(".agree_checkbox").is(":checked")){
            $(".btn_signup").removeAttr("disabled");
            $(".btn_signup").removeClass("btn_disabled");
        }else{
            $(".btn_signup").attr("disabled", "true");
            $(".btn_signup").addClass("btn_disabled");
        }
    });
});