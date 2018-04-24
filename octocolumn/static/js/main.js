$(document).ready(function() {
    // var opts = {
    //     lines: 12             // The number of lines to draw
    //   , length: 4             // The length of each line
    //   , width: 3              // The line thickness
    //   , radius: 10            // The radius of the inner circle
    //   , scale: 0.7            // Scales overall size of the spinner
    //   , corners: 1            // Roundness (0..1)
    //   , color: '#000'         // #rgb or #rrggbb
    //   , opacity: 1/4          // Opacity of the lines
    //   , rotate: 0             // Rotation offset
    //   , direction: 1          // 1: clockwise, -1: counterclockwise
    //   , speed: 1              // Rounds per second
    //   , trail: 100            // Afterglow percentage
    //   , fps: 20               // Frames per second when using setTimeout()
    //   , zIndex: 2e9           // Use a high z-index by default
    //   , className: 'spinner'  // CSS class to assign to the element
    //   , top: '50%'            // center vertically
    //   , left: '50%'           // center horizontally
    //   , shadow: false         // Whether to render a shadow
    //   , hwaccel: false        // Whether to use hardware acceleration (might be buggy)
    //   , position: 'absolute'  // Element positioning
    // }
    // var target = document.getElementById('spinner');
    // var spinner = new Spinner(opts).spin(target);
    // target.appendChild(spinner.el);

    var data = getData();

    popBalloon();

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        var title = $('#'+post_id+',h1').text();
        var username = $(e.target).closest('.post').children('.user-info').children('h1').text();
        var readtime = $(e.target).closest('.post').children('.full-right').text();
        console.log($('#'+post_id+',h1'))
        if(post_id > 0){
            // var card_id = $("#"+post_id).closest(".feedbox").attr("id").substr(5,1);
            // var cover_img = data[card_id-1].cover_image;
            // var title = data[card_id-1].title;
            // var date = data[card_id-1].all_status.created_datetime;
            // var username = data[card_id-1].all_status.username;
            // var price = data[card_id-1].price;
            // var preview = data[card_id-1].preview;
            // var readtime = $("#card_" + card_id + " .profile_readtime").text();

            isBought(post_id, title, username, readtime);
            
        }
    });
    $(".profile_mark").click(function(e){
        
        var bookmark_id = $(e.target).attr("id").replace("bookmark_",'');
        bookmark(bookmark_id);
    });
    $(".btn-cancel-wrap").click(function(){
        $(".preview-wrap").hide();
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
    // width = ((imgHeight-st)/imgHeight)*100;
    $('.main-content-title').css('opacity',opacity1);
    $('.main-content-sub').css('opacity',opacity2);
    $('.main-content-btn').css('opacity',opacity3);
    $('.main-content-img').css('opacity',opacity4);
    // $('.main-content-img').css('width',width+'%');    
    
    // if (st > lastScrollTop){
    //     // Scroll Down
    //     console.log('scroll down');
    //     $('.main-img-text-container').css('opacity',1)
    // } else {
    //     // Scroll Up
    //     console.log('scroll up');
    //     $('.main-img-text-container').css('opacity',1)        
    // }
    // lastScrollTop = st;
});