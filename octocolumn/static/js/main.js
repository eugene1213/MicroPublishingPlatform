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
    // popBalloon();

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
/* =================================
   TYPING EFFECT
=================================== */
(function($) {
    "use strict";

    $('[data-typer-targets]').typer();
    $.typer.options.clearOnHighlight=false;

})(jQuery);

// http://cosmos.layervault.com/typer-js.html
// https://www.paulund.co.uk/create-typing-effect
// https://www.mattboldt.com/demos/typed-js/
$(function(){
    $('.container').delegate('.bookmark>i','click',function(e){

        var bookmark_id = $(e.target).closest('.bookmark').attr("id").replace("bookmark_",'');        
        bookmark(bookmark_id,false);
    });
});
$(window).unbind('scroll touchmove').on('scroll touchmove',function() { 
    if ($(window).scrollTop() != 0) {
        $('.mouse').hide();
        $('.mouse + p').hide();
    } else {
        $('.mouse').show();
        $('.mouse + p').show();
    }
});
var lastScrollTop = 0;
var imgHeight = $('.main-container').height();
var imgWidth = $('.main-container').width();
var mainImageTextCoord = $('.main-container').offset().top;
var opacity1 = 0;

$(window).scroll(function(){

    var st = $(document).scrollTop();

    opacity1 = (mainImageTextCoord+imgHeight-st*2)/(mainImageTextCoord+imgHeight);

    $('.main-container').css('opacity',opacity1);
});