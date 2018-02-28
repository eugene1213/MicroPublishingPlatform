$(document).ready(function(){

    /* 발행버튼 클릭시 발행메뉴 드롭다운 */
    $(".btn-publish").click(function(event) {

        if($(".arrow-box").is(":visible")){

            $(".arrow-box").hide();
            $(".css-arrow").css("transform","rotate(360deg)");
        } else {

            if( $(".editable").text().length > 543 ){
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

    $(".agreement-checkbox").click(function(){
        btn_activation();
    });

    $(".done-publish").click(function(){

        var cover_img = $("#preview-cover-img").attr("src");
        var preview_img = $("#preview-main-content > img").attr("src");
        var tag = '';
            tag = $("#tag_all").text();
        var code = $("#octo-code-1").val() + $("#octo-code-2").val() + $("#octo-code-3").val() + $("#octo-code-4").val();
        var price = $(".preview-br-list-wrap > .price-set-decimal").text();
        var temp_id = localStorage.getItem("temp_id");

        publish(temp_id, cover_img, preview_img, tag, code, price);

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
function btn_activation(){

    if($(".agreement-checkbox").is(":checked")){
        $(".done-publish").removeAttr("disabled");
        $(".done-publish").removeClass("btn_disabled");
    }else{
        $(".done-publish").attr("disabled", "true");
        $(".done-publish").addClass("btn_disabled");
    }
}

/* 최종적으로 발행을 결정하면 실행되는 함수 */
function publish(temp_id, cover_img, preview_img, tag, code, price) {
    
    $.ajax({
        url: "http://127.0.0.1:8000/api/column/post-create/",
        async: false,
        type: 'POST',
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        headers: {
            'Authorization' : 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImV1Z2VuZTJAb2N0b2NvbHVtbi5jb20iLCJleHAiOjE1MjAyMjUyMzcsIm9yaWdfaWF0IjoxNTE5NjIwNDM3fQ.dB-EHzQg3h1CyyTDIJPkyrn0ydNgdACvbQJvYxYxENk'
        },
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