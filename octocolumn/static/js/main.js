$(document).ready(function() {

    var opts = {
        lines: 12             // The number of lines to draw
        , length: 7             // The length of each line
        , width: 5              // The line thickness
        , radius: 10            // The radius of the inner circle
        , scale: 1.0            // Scales overall size of the spinner
        , corners: 1            // Roundness (0..1)
        , color: '#ffffff'         // #rgb or #rrggbb
        , opacity: 1/4          // Opacity of the lines
        , rotate: 0             // Rotation offset
        , direction: 1          // 1: clockwise, -1: counterclockwise
        , speed: 1              // Rounds per second
        , trail: 100            // Afterglow percentage
        , fps: 20               // Frames per second when using setTimeout()
        , zIndex: 2e9           // Use a high z-index by default
        , className: 'spinner'  // CSS class to assign to the element
        , top: '75%'            // center vertically
        , left: '50%'           // center horizontally
        , shadow: false         // Whether to render a shadow
        , hwaccel: false        // Whether to use hardware acceleration (might be buggy)
        , position: 'absolute'  // Element positioning
        }
        var target = document.getElementById('container');
        var spinner = new Spinner(opts).spin(target);

    getData();
    popBalloon();

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        var readtime = $('#readtime'+post_id).text();
        var bookmark_className = $('#bookmark_'+post_id +'> i').attr('class');
        var bookmark_status = false;
        bookmark_className == 'icon-bookmark'?bookmark_status = true:bookmark_status = false;

        if(post_id > 0){

            isBought(post_id, readtime, bookmark_status);
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
    $('.container').delegate('.bookmark>i','click',function(e){

        var bookmark_id = $(e.target).closest('.bookmark').attr("id").replace("bookmark_",'');        
        bookmark(bookmark_id,false);
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