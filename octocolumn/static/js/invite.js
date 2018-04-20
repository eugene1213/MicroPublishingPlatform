function invite(email) {
    
    $.ajax({
        url: "/api/member/invite/",
        async: true,
        type: 'POST',
        dataType: 'json',
        data: {email:email},
        success: function(json) {
            var successMsgTitle = '메일이 발송됐습니다.';
            var successMsg = email+'님을 octocolumn Closed-Beta에 초대하셨습니다.';
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: successMsgTitle, //Modal Title
                text: successMsg, //Modal HTML Content
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