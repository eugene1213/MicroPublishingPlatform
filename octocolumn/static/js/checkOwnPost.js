/* 구매했는지 체크 */
function isBought(post_id, cover_img, title, date, author, tag, readtime, price, preview) {

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            console.log(json)
            if(json.detail.isBuy) {
                window.location.href = "/read/"+post_id;
            }else {
                // var preview_image = json.detail.preview;

                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현

                // var img = new Image();
                // img.src = json.detail.preview;

                $("#preview-main-content > .previewElementsWrap").replaceWith(preview);
                $(".previewElementsWrap").children(":last").css("filter","blur(4px)");

                $("#preview-cover-img").attr("src",cover_img);
                $(".preview-title").text(title);
                $(".preview-create-date").text(date);
                $(".preview-read-time").text(readtime);
                $(".preview-author").text(author.username);
                $(".priceBtn > .btn").text(price + "P로 구매");
                $(".priceBtn .btn").attr("id","post"+post_id);

                //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            
                $(".preview-wrap").height($("html").height());
                $(".preview-wrap").show();
                $("#preview-main-content > img").load(function() {

                    if( $("#preview").height() > $("html").height() ) {
                        $(".preview-wrap").height($("#preview").height() + 256);
                    }else {
                        $(".preview-wrap").height($("html").height() + 256);
                    }
                });
            }
            console.log("isBought: "+json.detail.isBuy);
        },
        error: function(error) {
            console.log(error);
        }
    });
}