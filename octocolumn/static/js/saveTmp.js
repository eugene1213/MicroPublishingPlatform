//타이핑을 멈추고 5초간 입력이 없으면 작성중인 내용 임시저장
$(document).ready(function(){

    localStorage.setItem("temp_id", '');

    loadTemp();

    $(".modal-extend > .btn-yes").click(function(){
        $(".editable > p").remove();
        $(".editable > div").remove();
        viewTemp( loadTemp() );
        
        $(".modal-extend-wrap").hide();
    });
    $(".modal-extend > .btn-no").click(function(){
        $(".modal-extend-wrap").hide();
    });
    

    title2header("write");
    saveHandler();

    var placeholderCoord = $("#title").offset().left; // 에디터 placeholder 부분에서 마우스 커서가 변하지 않고 위치가 맞지 않는 문제 해결.가상요소(:after)라서 style태그를 추가하는 방식으로만 해결 가능
    var addStyle = "<style>.editable.medium-editor-placeholder:after{left: "+placeholderCoord+"px;top: 0;padding:0!important;cursor:text;z-index:-1;}.medium-insert-buttons{left:"+(placeholderCoord-35)+"px!important;margin-top:-7px!important;}.medium-insert-embeds-placeholder:after{left:"+placeholderCoord+"px;}</style>";

    $('head').append(addStyle);
    $(".title").focus();                          // 페이지 로드가 완료되면 제목 input박스에 포커스

});

/* 윈도우 리사이즈에 따른 placeholder위치 조정 */
$(window).resize(function(){

    placeholderCoord = $("#title").offset().left; // 에디터 placeholder 부분에서 마우스 커서가 변하지 않고 위치가 맞지 않는 문제 해결.가상요소(:after)라서 style태그를 추가하는 방식으로만 해결 가능
    addStyle = "<style>.editable.medium-editor-placeholder:after{left: "+placeholderCoord+"px;top: 0;padding:0!important;cursor:text;z-index:-1;}.medium-insert-buttons{left:"+(placeholderCoord-35)+"px!important;margin-top:-7px!important;}.medium-insert-embeds-placeholder:after{left:"+placeholderCoord+"px;}</style>";

    $('style').replaceWith(addStyle);
});

/* 임시저장 */
function saveTmp(auto){
        
    var main_content = editor.getContent();
    var temp_id = "";
        temp_id = localStorage.getItem("temp_id");
    var title = "";

    $(".title").html() == "" ? title = "제목없음" :title = $(".title").text();        // 제목이 빈 값이면 제목없음으로 대체
    
    title = $.trim(title);
    if(auto == true){
        if($(".editable").text().length < 543) return console.log("분량 미달");       // 분량 미달이면 자동저장x
    }

    $.ajax({
        url: "/api/column/temp/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            title: title,
            main_content: main_content,
            temp_id : temp_id
        },
        success: function(json) {
            localStorage.setItem("temp_id", json.temp.temp_id);
            $(".state").text("저장됨");
        },
        error: function(error) {
            console.log(error);
        }
    });
}
/* 임시저장 이벤트 리스너 */
function saveHandler(){
    $(document).keyup(function(event) {     // 자동저장

        if($(event.target).hasClass('editable')) {

            $(".state").text("작성중");

            var timer = setTimeout(function(){

                saveTmp(true);              // 타이머가 실행되고 5초가 지나면 임시 저장 함수를 호출한다.
            },2000);

            $(document).keydown(function(){

                clearTimeout(timer);        // 타이머가 실행중인 도중 다시 타이핑을 시작하면 타이머 중지.
            });
        }
    });
                                            // 저장 버튼 클릭시
    $(".btn-save").click(function(event) {

        saveTmp(false);
    });
                                            // 발행 버튼 클릭시 (미리보기 블러이미지 생성과 동시에 진행됨)
    $(".btn-publish-final").click(function(){

        saveTmp(false);
    });
}