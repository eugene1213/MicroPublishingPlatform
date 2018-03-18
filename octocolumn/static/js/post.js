$(document).ready(function(){

    var data = isAuthor();
    
    /* 발행버튼 클릭시 발행메뉴 드롭다운 */
    $(".btn-publish").click(function(event) {

        if($(".arrow-box").is(":visible")){     // 발행메뉴와 버튼에 화살표 방향 변경

            $(".arrow-box").hide();
            $(".css-arrow").css("transform","rotate(360deg)");
        } else {

            if( $(".editable").text().length > 543 ){       // 글자 수 체크 후 발행버튼 활성화
                $(".btn-publish-final").removeAttr("disabled");
                $(".btn-publish-final").removeClass("btn_disabled");
            }else{
                $(".btn-publish-final").attr("disabled", "true");
                $(".btn-publish-final").addClass("btn_disabled");
            }
            
            $(".arrow-box").show();
            $(".css-arrow").css("transform","rotate(180deg)");
        }
    });

    $(".agreement-checkbox").click(function(){              // 동의 체크 여부 확인 후 버튼 활성화
        btn_activation(this,".done-publish");
    });

    $(".done-publish").click(function(){                    // 출판 버튼 누르면 작가인지 판단해서 출판/작가신청 진행. 아래 if문에서 data는 boolean타입

        var cover_img = $("#preview-cover-img").attr("src");
        var preview_img = $("#preview-main-content > img").attr("src");
        var tag = '';
            tag = $("#tag_all").text();
        var code = $("#octo-code-1").val() + $("#octo-code-2").val() + $("#octo-code-3").val() + $("#octo-code-4").val();
        var price = $(".preview-br-list-wrap > .price-set-decimal").text();
        var temp_id = localStorage.getItem("temp_id");

        if(data) {

            publish(temp_id, cover_img, preview_img, tag, code, price);
        } else {

            $("#authorApply").show();
            $("#preview").hide();

            window.location.href = "#top";

            $("#btn-author-apply").unbind('click').click(function(){
        
                var intro = $(".author-intro").html();
                var url = $("#inputUrl").val();

                authorApply(temp_id, cover_img, preview_img, tag, code, price, intro, url);
                
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

/* 최종적으로 발행을 결정하면 실행되는 함수*/
function publish(temp_id, cover_img, preview_img, tag, code, price) {
    
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
            "preview" : preview_img,
            "tag" : tag,
            "code" : code,
            "price" : price
        }),
        success: function(json) {
            console.log("발행됨");
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
console.log(data)
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
function authorApply(temp_id, cover_img, preview_img, tag, code, price, intro, url) {
    
    $.ajax({
        url: "/api/member/author-apply/",
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
            "preview" : preview_img,
            "tag" : tag,
            "code" : code,
            "price" : price,
            "intro" : intro,
            "blog" : url
        }),
        success: function(json) {
            console.log("신청됨");
            $(".modal-success-wrap").show();
            localStorage.setItem("temp_id", '');
        },
        error: function(error) {
            
            console.log(error);

            if(error.responseJSON.detail == "Already attempted author") {

                $(".modal-success-wrap").show();
                localStorage.setItem("temp_id", '');
            }
        }
    });
}