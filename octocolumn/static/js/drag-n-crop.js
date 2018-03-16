function setMargin(img) {                         // img: 이미지 태그 셀렉터, elRatio: 엘리먼트 비율

    var elRatio = 0;
    var direction = '';
    var marginDirect = '';

    elRatio = $(img).parents().width()/$(img).parents().height();
    console.log($(img)[0].naturalWidth/$(img)[0].naturalHeight +" : "+elRatio);
    if($(img)[0].naturalWidth/$(img)[0].naturalHeight > elRatio) {
        direction = 'x';
        $(img).heigth("100%");

    }else {
        direction = 'y';
        $(img).width("100%");
    }

    console.log(direction);
    $(img).draggable({axis: direction});
}