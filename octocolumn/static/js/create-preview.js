$(document).ready(function() {
    
    $(".btn-publish-final").unbind('click').click(function(){

        // var target = document.getElementById('container');
		// var spinner = new Spinner().spin(target);
        // target.appendChild(spinner.el);

        $(".medium-insert-buttons").hide();     // 에디터 이미지 툴바 숨김(안숨기면 이미지에 '+' 모양 찍힘)
        // setTimeout(function(){

        $("#tmp").replaceWith("<div id='tmp'>" + $(".editable").html() + "</div>");
        $(".container").css("position", "fixed");
        if($(".container").width() < 960) $(".container").css({"left": "50%","margin-left": $(".container").width()/(-2)});

        previewContentInfo();                   // 설정된 값들 미리보기에 출력

        $("#previewPrice").text($("#setPrice").text());
        // },100)
        $(".arrow-box").hide();
        $(".css-arrow").css("transform","rotate(360deg)");
        saveTmp(false); // 임시저장

        var mainContent = $(".editable").html();
        var imgSrc = $("#blah").attr("src");
        var title = $(".title").text();
        var readTime = $(".read-time").text();
        var author = $(".username").text();
        var numOfTag = 0;
        var lastTagId = $(".added-tag-wrap:nth-last-child(1)").attr("id");
        var tagHtml = "";
        var price = $("#setPrice").text();
        var recommend1, recommend2, recommend3;
        var recommendHtml = "";
        data = isAuthor();
        if(data) {
            previewBtn = "출판";
            
        }
        else {
            previewBtn = "다음 단계";
        }


        if($("#recommend1").val()) {
            recommend1 = $("#recommend1").val();
            recommendHtml += "<p><span class=\"icon-ok\"></span>"+recommend1+"</p>";
        }
        if($("#recommend2").val()){
            recommend2 = $("#recommend2").val();
            recommendHtml += "<p><span class=\"icon-ok\"></span>"+recommend2+"</p>";
        }
        if($("#recommend3").val()){
            recommend3 = $("#recommend3").val();
            recommendHtml += "<p><span class=\"icon-ok\"></span>"+recommend3+"</p>";            
        }

        if(lastTagId != undefined){
            numOfTag = lastTagId.replace("tag_","");
        }

        for(let i=1; i<=numOfTag; i++) {
            
            var tag = $("#tag_"+i).text();
    
            tagHtml += "<li>"+tag+"</li>";
        }

        previewHtml = "\
            <div id=\"preview-container\">\
                <div class=\"preview-content\">\
                    <div class=\"close\"></div>\
                    <div class=\"warning-phrase\">\
                    출판하려는 칼럼의 정보를 확인하시고, 칼럼을 출판해주세요.<br>칼럼을 출판한 후에는 수정, 삭제가 불가능합니다.\
                    </div>\
                    <!-- Column Preview -->\
                    <div class=\"column-preview\">\
                        <div class=\"preview-cover-img\" style=\"background-image:url("+imgSrc+");\"></div>\
                        <div class=\"column-title\">"+title+"</div>\
                        <div class=\"columnist-info\">\
                            <div class=\"columnist-name\">\
                                by <span class=\"user-name\"><i>"+author+"</i></span>\
                            </div>\
                            <div class=\"column-read-time\">\
                                <span class=\"read-time\">"+readTime+"</span>\
                            </div>\
                        </div>\
                        <!-- Main Contents -->\
                        <div class=\"column-content\">\
                        "+mainContent+"\
                        </div>\
                        <div class=\"column-tags\">\
                            <p>Tags</p>\
                            <ul>\
                                "+tagHtml+"\
                            </ul>\
                        </div>\
                        <div class=\"recommendation\">\
                            <p>이런 분들께 추천해요.</p>\
                            <div class=\"recommendation-list-wrap\">\
                                "+recommendHtml+"\
                            </div>\
                        </div>\
                    </div>\
                    <div class=\"preview-writer-button-wrap\">\
                        <div class=\"price-set-decimal\" id=\"previewPrice\">\
                            <p>칼럼 가격</p>\
                            <span>"+price+"</span>&nbsp;Point\
                        </div>\
                        <div class=\"preview-agreement-wrap\">\
                            <input type=\"checkbox\" class=\"agree_checkbox\">\
                            <div class=\"agree_text\">본인은&nbsp;<span onClick=\"term()\">환불불가정책</span>에 동의합니다.</div>\
                        </div>\
                        <div class=\"preview-writer-button\">\
                            <button class=\"done-publish btn_disabled\" disabled=\"disabled\">"+previewBtn+"</button>\
                            <button class=\"cancel-publish\" id=\"cancel-publish\">취소</button>\
                        </div>\
                        <div class=\"preview-terms-wrap\">\
                            <span class=\"preview-terms\">대가성 콘텐츠 표기</span>,&nbsp;\
                            <span class=\"preview-terms\">사용자 아이디 정책</span>,&nbsp;\
                            <span class=\"preview-terms\">서비스 운영정책</span>,&nbsp;\
                            <span class=\"preview-terms\">서비스 이용약관</span>,&nbsp;\
                            <span class=\"preview-terms\">저작권법</span>을 참고하세요.\
                        </div>\
                    </div>\
                </div>\
            </div>\
        ";
        $(".container").after(previewHtml);
    });
    $(".cancel-publish").click(function(){
        $(".preview-wrap").hide();
        $(".container").css({"position": "static","left":"","margin-left":""});
    });
    $(".btn-cancel-wrap").click(function(){
        $(".preview-wrap").hide();
        $(".container").css({"position": "static","left":"","margin-left":""});
    });

    /* read time 계산기 */
    $(function() {

        $('#editable').keyup(function (e){

            var content = $(this).text().trim();                            // 전체 글자수
            var countSpace = ((content.match(/\s/g) || []).length)/2;       // 띄어쓰기를 0.5글자 계산
            var sum = content.length - 3.5 - countSpace;                    // 전체 글자수에서 띄어쓰기 갯수*0.5 뺀 값
            var time = Math.floor(sum / 500);                               // 1분/500자 so림

            if(time > 0) {                                                  // 글을 1분 분량 이상 작성하면 read time 출력해서 보여줌
                $(".read-time").replaceWith("<div class=\"read-time\">" + time + " min read</div>");
            }
        });
    });
    countTitle();   // 제목 글자수 체크
}); // $(document).ready(function()

$(function(){
    $(document).on('click','.close',function(){
        $("#preview-container").detach();
    });
    $(document).on('click','#cancel-publish',function(){
        $("#preview-container").detach();
    });
})

/* 설정된 커버 이미지 preview에 출력 */
function previewCoverImg() {
    var imgSrc = $("#blah").attr("src");
    $(".preview-cover-img").css("background-image", 'url('+imgSrc+')');

    var imgHeight = $("#preview-cover-img").height();
    // 이미지 높이가 401보다 크면 위,아래 부분을 넘는 만큼 자름
    if(imgHeight>401){
        var margin = (imgHeight - 401) / 2;
        $("#preview-cover-img").css("margin-top",(-1)*margin+"px");
    }
}

/* 발행 미리보기에 글의 정보들을 출력 */
function previewContentInfo() {

    var title = $(".title").text();
    var readTime = $(".read-time").text();
    var author = $(".username").text();
    var tag_all = "";
    var numOfTag = 0;

    $(".preview-title").text(title);
    $(".preview-read-time").text(readTime);
    $(".preview-author").text(author);

    var lastTagId = $(".added-tag-wrap:nth-last-child(1)").attr("id");
    
    if(lastTagId != undefined){
        numOfTag = lastTagId.replace("tag_","");
    }

    $(".preview-tag").remove();

    for(let i=1; i<=numOfTag; i++) {

        var tag = $("#tag_"+i).text();

        $(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
        
        tag_all += (tag + ", ");
    }
    tag_all = tag_all.substr(0,tag_all.length-2);

    $("#tag_all").text(tag_all);
}

/* 제목 60글자 제한 */
function countTitle(){

    var content_id = 'title';  
    var max = 60;
    
    $('#'+content_id).keyup(function(e){ check_charcount(content_id, max, e); });
    $('#'+content_id).keydown(function(e){ check_charcount(content_id, max, e); });
    
    function check_charcount(content_id, max, e)
    {   
        if(e.which != 8 && $('#'+content_id).text().length > max)
        {
            $('#'+content_id).text($('#'+content_id).text().substring(0, max));
            e.preventDefault();
        }
    }
}
function creatPreviewElements() {

    var count = 0;
    var i = 0;
    var previewRule = 500;                                  // octocolumn 미리보기에서 보여주는 글자 수. 정책이 바뀌면 이 부분 수정
    var previewElements = document.createElement('div');    // 미리보기에서 보여줄 내용

    var appendEl = '';
    $(previewElements).addClass('previewElementsWrap');

    while( count < previewRule ) {

        if( $("#editable").children(":eq("+i+")")[0].localName == 'div' ){
            count += 125;                                                       // 500글자 -> 1분 기준 이미지가 대응하는 글자수.(15초 분량)

            appendEl = $("#editable").children(":eq("+i+")").clone()[0];
        
            previewElements.append( appendEl );
            i++;

            continue;
        }
        
        count += $("#editable").children(":eq("+i+")").text().length;

        appendEl = $("#editable").children(":eq("+i+")").clone()[0];
        previewElements.append( appendEl );

        i++;
    }
    var lastLocalName = $("#editable").children(":eq("+(i-1)+")")[0].localName; // 500글자 넘는 부분이 어떤 태그인지
    if( lastLocalName != 'div' ) {

        var overText = count - previewRule;                                     // 500글자에서 얼마나 초과됐는지
        var lastText = $("#editable").children(":eq("+(i-1)+")").text();        // 500글자가 넘어가는 부분
        var textForReplace = lastText.substr( 0, lastText.length - overText );
        var lastElement = document.createElement(lastLocalName);

        $(lastElement).text(textForReplace);
        $(previewElements).children(':last').replaceWith(lastElement);
    }
    return previewElements;
}
/* 텍스트와 이미지를 블러처리 */
function blurText(){

    var previewLength = 0;

    for(var child=1; child < 10; child++){
        // 10줄까지의 글자수를 센다. 300글자가 넘으면 세는 것을 멈춘다.
        previewLength += $(".editable :nth-child("+child+")").text().length;
        if(previewLength>300) break;
    }

    var lastIdx = $(".editable p").index($('.editable p:nth-last-of-type(1)')); // textarea의 자식요소 갯수

    $("#tmp").append($(".editable").html());                                    // #tmp에 .editable 내용을 임시로 추가한다.(이미지로 렌더링 후 지움)

    for(let i=child+1;i<lastIdx+30;i++){
        $("#tmp :nth-child("+i+")").css("filter","blur(4px)");                  // 300자가 넘거나 10줄이 넘는 자식요소부터 마지막 자식요소까지 모두 블러처리
    }
}

/* .editable 내용을 이미지로 렌더링*/
function dom2img(){

    blurText();

    var srcEl = document.getElementById("tmp");

    domtoimage.toPng(srcEl).then(function (dataUrl) {

        var img = new Image();
        img.src = dataUrl;
        $("#preview-main-content > img").replaceWith(img);

    }).then(function(){

        $("#tmp").replaceWith("<div id=\"tmp\"></div>");                    // blurText()에서 임시로 추가했던 요소 초기화
    }).then(function(){
        // $('.spinner').remove();
        $(".preview-wrap").show();
    });
}