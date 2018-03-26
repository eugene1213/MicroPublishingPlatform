function setMargin(img) {                         // img: 이미지 태그 셀렉터

    $(img).removeAttr("style");
    $(img).css("position","relative");

    var direction = '';                           // 드레그 허용할 방향

    var divHeight = $(img).closest(".profile-image-upload-wrap").height();         // 이미지를 감싼 부모 요소의 높이
    var divWidth = $(img).closest(".profile-image-upload-wrap").width();           // 이미지를 감싼 부모 요소의 너비

    if($(img)[0].naturalHeight/$(img)[0].naturalWidth < divHeight/divWidth) {      // 원본 이미지의 비율과 출력될 비율을 비교해서 횡,종 이동을 결정

        direction = 'x';
        $(img).height(divHeight);
        $(img).css("cursor","ew-resize");

        var width = divHeight / $(img)[0].naturalHeight * $(img)[0].naturalWidth;
        
        $(img).wrap("<div class='tmpWrap' style='height:100%;width:" + (width+(width-divWidth)) + "px;position:relative;left:-"+ (width - divWidth) +"px'></div>");
    }else {

        direction = 'y';
        $(img).width(divWidth);
        $(img).css("cursor","ns-resize");

        var height = divWidth/$(img)[0].naturalWidth*$(img)[0].naturalHeight;
        
        $(img).wrap("<div class='tmpWrap' style='width:100%;height:" + (height+(height-divHeight)) + "px;position:relative;top:-"+ (height - divHeight) +"px'></div>");
        //드레그 영역을 제한할 부모요소 생성
    }
    $(img).draggable({axis: direction,containment : $(".tmpWrap")});
}
/* 프로필 이미지를 로드하는 곳에서 반드시 이 함수로 사이즈를 조절해줘야함 */
function loadCropImage(img) {
    
    var divHeight = $(img).closest(".profile-image-upload-wrap").height();         // 이미지를 감싼 부모 요소의 높이
    var divWidth = $(img).closest(".profile-image-upload-wrap").width();           // 이미지를 감싼 부모 요소의 너비

    var src = $(img).attr("src");
    if(src == null) return;
    var position_strtmp = src.split("_")[1];
    var direction = position_strtmp.substr(0,1);                                   // x or y
    var uploadPosition = position_strtmp.substr(1,position_strtmp.length-1);

    var fileWidth = $(img)[0].naturalWidth;
    var fileHeight = $(img)[0].naturalHeight;

    $(img).css("position","relative");

    if(direction == 'x') {

        var position = uploadPosition;
        if(position > 0) position = "-"+position+"%";
        else position = position+"%";

        $(img).height("100%");
        $(img).css("left",position);
        
    }else {

        var position = uploadPosition;
        if(position > 0) position = "-"+position+"%";
        else position = position+"%";
        
        $(img).width("100%");
        $(img).css("top",position);
    }
}