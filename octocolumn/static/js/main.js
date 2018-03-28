$(document).ready(function() {

    var data = getData();
    popBalloon(data);

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        if(post_id > 0){

            var card_id = $("#"+post_id).closest(".feedbox").attr("id").substr(5,1);
            var cover_img = data[card_id-1].post.cover_img;
            var title = data[card_id-1].post.title;
            var date = data[card_id-1].post.created_datetime;
            var author = data[card_id-1].post.author;
            var tag = data[card_id-1].post.tag;
            var price = data[card_id-1].post.price;
            var preview = data[card_id-1].post.preview;
            var readtime = $("#card_" + card_id + " .profile_readtime").text();

            isBought(post_id, cover_img, title, date, author, tag, readtime, price, preview);
            
        }
    });
    $(".profile_mark").click(function(e){
        
        var post_id = $(e.target).closest(".fb1_txt_2").attr("id");
    });
    $(".btn-cancel-wrap").click(function(){
        $(".preview-wrap").hide();
    });
});