$(document).ready(function() {

    getData();
    popBalloon();

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        var readtime = $('#readtime'+post_id).text();

        if(post_id > 0){

            isBought(post_id, readtime);
        }
    });

    $('.image-loader').imageloader({
        background: true,
        callback: function (elm) {
            $('.spinner').remove();
            $(elm).fadeIn();
        }
    });
});
$(function(){
    $('.container').delegate('.bookmark>span','click',function(e){

        var bookmark_id = $(e.target).closest('.bookmark').attr("id").replace("bookmark_",'');        
        bookmark(bookmark_id);
    });
});
var lastScrollTop = 0;
var imgHeight = $('.main-content-img').height();
var imgWidth = $('.main-content-img').width();
var mainImageTextCoord1 = $('.main-content-title').offset().top;
var mainImageTextCoord2 = $('.main-content-sub').offset().top;
var mainImageTextCoord3 = $('.main-content-btn').offset().top;
var mainImageTextCoord4 = $('.main-content-img').height();
var opacity1 = 0;
var opacity2 = 0;
var opacity3 = 0;
var opacity4 = 0;
var width = 0;
$(window).scroll(function(){

    var st = $(document).scrollTop();

    opacity1 = (mainImageTextCoord1-st)/mainImageTextCoord1;
    opacity2 = (mainImageTextCoord2-st)/mainImageTextCoord2;
    opacity3 = (mainImageTextCoord3-st)/mainImageTextCoord3;
    opacity4 = (mainImageTextCoord4-st*1.5)/mainImageTextCoord4;

    $('.main-content-title').css('opacity',opacity1);
    $('.main-content-sub').css('opacity',opacity2);
    $('.main-content-btn').css('opacity',opacity3);
    $('.main-content-img').css('opacity',opacity4);
});