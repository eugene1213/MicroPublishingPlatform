/* 구매했는지 체크 */
function isBought(post_id, cover_img, title, date, author, tag, readtime, price) {

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            window.location.href = "/column/read/"+post_id;
            if(json.detail.isBuy) {
                window.location.href = "/column/read/"+post_id;
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
                $(".preview-read-time").text(readtime);
                $(".preview-author").text(author.username);
                $(".priceBtn > .btn").text(price + "P로 구매");

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