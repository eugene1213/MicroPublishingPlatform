$(document).ready(function() {

    var data = getData();

    popBalloon();

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");

        if(post_id > 0){
            var card_id = $("#"+post_id).closest(".feedbox").attr("id").substr(5,1);
            var cover_img = data[card_id-1].cover_image;
            var title = data[card_id-1].title;
            var date = data[card_id-1].all_status.created_datetime;
            var username = data[card_id-1].all_status.username;
            var price = data[card_id-1].price;
            var preview = data[card_id-1].preview;
            var readtime = $("#card_" + card_id + " .profile_readtime").text();

            isBought(post_id, cover_img, title, date, username, readtime, price, preview);
            
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
            $(elm).fadeIn();
        }
    });
});

var lastScrollTop = 0;
var opacity = 0;
var imgHeight = $('.main-img').height();
var imgWidth = $('.main-img').width();
var mainImageTextCoord1 = $('.main-img-main-text').offset().top;
var mainImageTextCoord2 = $('.main-img-sub-text-container').offset().top;
var mainImageTextCoord3 = $('.main-img-btn').offset().top;


$(window).scroll(function(){

    var st = $(document).scrollTop();

    opacity1 = (mainImageTextCoord1-st)/mainImageTextCoord1;
    opacity2 = (mainImageTextCoord2-st)/mainImageTextCoord2;
    opacity3 = (mainImageTextCoord3-st)/mainImageTextCoord3;
    width = ((imgHeight-st)/imgHeight)*100;
    $('.main-img-main-text').css('opacity',opacity1);
    $('.main-img-sub-text-container').css('opacity',opacity2);
    $('.main-img-btn').css('opacity',opacity3);
    $('.main-img').css('width',width+'%');    
    
    // if (st > lastScrollTop){
    //     // Scroll Down
    //     console.log('scroll down');
    //     $('.main-img-text-container').css('opacity',1)
    // } else {
    //     // Scroll Up
    //     console.log('scroll up');
    //     $('.main-img-text-container').css('opacity',1)        
    // }
    lastScrollTop = st;
});