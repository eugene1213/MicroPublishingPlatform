$(document).ready(function(){

    $(".tag-input").keydown(function(e){
        tagAppender(e);
    });
    $(".arrow-box").click(function(e){
        tagRemover(e);
    });
});

function tagAppender(e) {
    if(e.keyCode == 13){ // 엔터를 눌렀을 때 태그가 추가된다.

        var tag_html = "<div class=\"added-tag-wrap\"><div class=\"tag-cancel\"></div><div class=\"tag-name\">"; //추가할 html
        var inputValue = $.trim($(".tag-input").val()); // input박스에 써진 값
        var tag = inputValue + "</div></div>";
        var added = $('.added-tag-wrap').length;        // 현재 추가된 태그가 몇개인지 검색한다.

        tag_html += tag;                                // 최종적으로 추가될 태그의 html

        if(inputValue != "" && added < 5 && inputValue.length <= 20) {             // 빈값인지, 현재 추가된 태그가 5개 미만인지 확인.

            $(".tag-added").append(tag_html);           // 태그 추가

            for(var n=1; n<=added+1; n++){
                $(".added-tag-wrap:nth-child(" + n + ")").attr("id","tag_" + n);    // 태그가 추가/삭제 될때마다 고유 id를 지정 (tagRemover()에서 사용하기위함.)
            }
            $(".tag-input").val("");                    // input박스를 비워준다.
        }
    }
    btn_activation_checklist();
}

function tagRemover(e) {
    if(e.target.className == "tag-cancel") {
        // 클릭된 요소가 해당 클래스를 갖고 있으면 id를 불러와서 해당요소 삭제.
        var id = $(e.target).parent().attr("id");
        $("#"+id).remove();
    }
    btn_activation_checklist();
}