/* 구매했는지 체크 */
function isBought(post_id, cover_img, title, date, author) {

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            if(json.detail.isBuy) {
                window.location.href = "/column/read/"
            }else {
                var preview_image = json.detail.preview;

                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현

                var img = new Image();
                img.src = json.detail.preview;

                $("#preview-main-content > img").replaceWith(img);

                $("#preview-cover-img").attr("src",cover_img);
                $(".preview-title").text(title);
                $(".preview-create-date").text(date);
                $(".preview-author").text(author);

                //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            
                $(".preview-wrap").height($("html").height());
                $(".preview-wrap").show();
            }
            console.log("isBought: "+json.detail.isBuy);
        },
        error: function(error) {
            console.log(error);
        }
    });
}