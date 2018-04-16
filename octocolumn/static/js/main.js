$(document).ready(function() {

    var data = getData();

    popBalloon();

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        if(post_id > 0){

            var card_id = $("#"+post_id).closest(".feedbox").attr("id").substr(5,1);
            var cover_img = data[card_id-1].cover_image;
            var title = data[card_id-1].title;
            var date = data[card_id-1].created_datetime;
            var author = data[card_id-1].author;
            var tag = data[card_id-1].tag;
            var price = data[card_id-1].price;
            var preview = data[card_id-1].preview;
            var readtime = $("#card_" + card_id + " .profile_readtime").text();

            isBought(post_id, cover_img, title, date, author, tag, readtime, price, preview);
            
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