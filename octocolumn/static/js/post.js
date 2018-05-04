$(document).ready(function(){

    var data = isAuthor();
    $('#blah').change(function(){
        if( $('#blah').attr('src') ){
            $(".btn-publish-final").removeAttr("disabled");
            $(".btn-publish-final").removeClass("btn_disabled");
        }else {
            $(".btn-publish-final").attr("disabled", "true");
            $(".btn-publish-final").addClass("btn_disabled");
        }
    });
        
    /* 출판버튼 클릭시 발행메뉴 드롭다운 */
    $(".btn-publish").click(function(event) {

        if($(".arrow-box").is(":visible")){     // 출판메뉴와 버튼 화살표 방향 변경

            $(".arrow-box").hide();
            $(".css-arrow").css("transform","rotate(360deg)");
        } else {

            btn_activation_checklist();
            
            $(".arrow-box").show();
            $(".css-arrow").css("transform","rotate(180deg)");
        }
    });

    $(".agreement-checkbox").click(function(){              // 동의 체크 여부 확인 후 버튼 활성화
        btn_activation(this,".done-publish");
    });

    $(".done-publish").click(function(){                    // 출판 버튼 누르면 작가인지 판단해서 출판/작가신청 진행. 아래 if문에서 data는 boolean타입

        var cover_img = $("#blah").attr("src");
        var preview_img = $("#preview-main-content > img").attr("src");
        var tag = '';
            tag = $("#tag_all").text();
        var price = $(".preview-br-list-wrap > .price-set-decimal").text();
        var temp_id = localStorage.getItem("temp_id");

        if(data) {

            if(tag==''){
                alert('최소 한 개 이상의 태그를 설정해주세요.');
            }else if(cover_img == '') {
                alert('표지 사진를 추가해주세요.');
            }else {
                publish(temp_id, cover_img, preview_img, tag, price);
            }
        } else {

            $("#authorApply").show();
            $("#preview").hide();

            $("#btn-author-apply").unbind('click').click(function(){
        
                var intro = $(".author-intro").html();
                var url = $("#inputUrl").val();

                if(tag==''){
                    alert('최소 한 개 이상의 태그를 설정해주세요.');
                }else if(cover_img == '') {
                    alert('표지 사진를 추가해주세요.');
                }else {
                    authorApply(temp_id, cover_img, preview_img, tag, price, intro, url);
                }
                $(".btn-confirm").unbind('click').click(function(){

                    window.location.href = "/";
                });
            });
        }
    });
});

$(document).mouseup(function (e) {
    
    var container = $(".arrow-box");
    
    if (!container.is(e.target) && container.has(e.target).length === 0){
    
        if($(".arrow-box").is(":visible")){
            $(".arrow-box").hide();
            $(".css-arrow").css("transform","rotate(360deg)");
        }
    }	
});
/* 버튼 활성화 & 비활성화 */
function btn_activation(handler,target){

    if($(handler).is(":checked")){
        $(target).removeAttr("disabled");
        $(target).removeClass("btn_disabled");
    }else{
        $(target).attr("disabled", "true");
        $(target).addClass("btn_disabled");
    }
}
/**
 * 출판하기 버튼이 활성화 되기 위한 조건
 */
function btn_activation_checklist() {
    if( $(".editable").text().length > 543 ){       // 글자 수 체크 후 발행버튼 활성화
        if( $('.added-tag-wrap').length != 0 ){
            if( $('#blah').attr('src') ){
                $('#errMsg').detach();
                $(".btn-publish-final").removeAttr("disabled");
                $(".btn-publish-final").removeClass("btn_disabled");
            }else {
                $(".btn-publish-final").attr("disabled", "true");
                $(".btn-publish-final").addClass("btn_disabled");
                $('#errMsg').detach();
                $('.btn-publish-final').before('<span id="errMsg" style="font-size:8px;color:#2a292a;opacity:0.5;float:left;margin-left:30px;margin-top:30px;">표지 사진을 설정해 주세요.</span>');       // 분량 미달이면 자동저장x    
            }
        }else {
            $(".btn-publish-final").attr("disabled", "true");
            $(".btn-publish-final").addClass("btn_disabled");
            $('#errMsg').detach();
            $('.btn-publish-final').before('<span id="errMsg" style="font-size:8px;color:#2a292a;opacity:0.5;float:left;margin-left:30px;margin-top:30px;">태그를 한개 이상 설정해 주세요</span>');
        }
    }else{
        $(".btn-publish-final").attr("disabled", "true");
        $(".btn-publish-final").addClass("btn_disabled");
        $('#errMsg').detach();
        $('.btn-publish-final').before('<span id="errMsg" style="font-size:8px;color:#2a292a;opacity:0.5;float:left;margin-left:30px;margin-top:30px;">분량이 부족합니다.</span>');
    }
}

/* 최종적으로 발행을 결정하면 실행되는 함수*/
function publish(temp_id, cover_img, preview_img, tag, price) {

    var preview = creatPreviewElements();

    $.ajax({

        url: "/api/column/post-create/",
        async: false,
        type: 'POST',
        xhrFields: {
            withCredentials: true
        },
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "temp_id" : temp_id,
            "cover" : cover_img,
            "tag" : tag,
            "price" : price,
            "preview" : preview.outerHTML
        }),
        success: function(json) {
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: 'Your column has been published', //Modal Title
                text: '많은 사람들이 읽었으면 좋겠습니다.<br/>좋은 이야기를 들려주셔서 감사드립니다.', //Modal HTML Content
                size: 'normal', //Modal Size (normal | large | small)
                buttons: [{
					text: "별말씀을요.",
					val: true,
					onClick: function(e) {
						window.location.href = '/';
					}
				}],
                center: true, //Center Modal Box?
                autoclose: false, //Auto Close Modal Box?
                callback: function(){window.location.href = '/'}, //Callback Function after close Modal (ex: function(result){alert(result);})
                onShow: function(r) {}, //After show Modal function
                closeClick: true, //Close Modal on click near the box
                closable: true, //If Modal is closable
                theme: 'atlant', //Modal Custom Theme
                animate: false, //Slide animation
                background: 'rgba(0,0,0,0.35)', //Background Color, it can be null
                zIndex: 1050, //z-index
                template: '<div class="modal-box"><div class="modal-inner"><div class="modal-title"></div><div class="modal-text"><div class="modal-buttons"></div></div></div></div>',
                _classes: {
                    box: '.modal-box',
                    boxInner: ".modal-inner",
                    title: '.modal-title',
                    content: '.modal-text',
                    buttons: '.modal-buttons'
                }
            });
            localStorage.setItem("temp_id", '');
        },
        error: function(error) {
            console.log(error);
        }
    });
}
/* 작가인지 확인 */
function isAuthor() {
    var data;       // 작가인지 알려주는 boolean 값
    
    $.ajax({
        url: "/api/column/isauthor/",
        type: 'POST',
        async: false,
        xhrFields: {
            withCredentials: true
        },
        dataType: 'json',
        success: function(json) {

            data = json.author;

            if(data) {
                $(".ready2publish").text("Ready to publish?");      // 작가면 모달창 상단에 보여줄 텍스트
            }
            else {
                $(".ready2publish").text("Become a writer");
                $("#done-publish").text("다음 단계");
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
    return data;
}
/* 작가신청 */
function authorApply(temp_id, cover_img, preview_img, tag, price, intro, url) {
    
    var preview = creatPreviewElements();

    $.ajax({
        url: "/api/member/authorApply/",
        async: false,
        type: 'POST',
        xhrFields: {
            withCredentials: true
        },
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            "temp_id" : temp_id,
            "cover" : cover_img,
            "preview" : preview.outerHTML,
            "tag" : tag,
            "price" : price,
            "intro" : intro,
            "blog" : url
        }),
        success: function(json) {
            modal({
                type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                title: '', //Modal Title
                text: '작성하신 칼럼은 octocolumn의 승인을 거쳐 출판되게 됩니다.<br />이러한 과정은 첫번째 칼럼에만 적용됩니다.<br />두번째 칼럼부터는 바로 출판하실 수 있습니다.<br />감사합니다!', //Modal HTML Content
                size: 'normal', //Modal Size (normal | large | small)
                buttons: [{
					text: "별말씀을요.",
					val: true,
					onClick: function(e) {
						window.location.href = '/';
					}
				}],
                center: true, //Center Modal Box?
                autoclose: false, //Auto Close Modal Box?
                callback: function(){window.location.href = '/'}, //Callback Function after close Modal (ex: function(result){alert(result);})
                onShow: function(r) {}, //After show Modal function
                closeClick: true, //Close Modal on click near the box
                closable: true, //If Modal is closable
                theme: 'atlant', //Modal Custom Theme
                animate: false, //Slide animation
                background: 'rgba(0,0,0,0.35)', //Background Color, it can be null
                zIndex: 1050, //z-index
                template: '<div class="modal-box"><div class="modal-inner"><div class="modal-title"></div><div class="modal-text"><div class="modal-buttons"></div></div></div></div>',
                _classes: {
                    box: '.modal-box',
                    boxInner: ".modal-inner",
                    title: '.modal-title',
                    content: '.modal-text',
                    buttons: '.modal-buttons'
                }
            });
            localStorage.setItem("temp_id", '');
        },
        error: function(error) {
            
            console.log(error);

            // if(error.responseJSON == "Already attempted author") {

            //     $(".modal-success-wrap").show();
            //     localStorage.setItem("temp_id", '');
            // }
        }
    });
}