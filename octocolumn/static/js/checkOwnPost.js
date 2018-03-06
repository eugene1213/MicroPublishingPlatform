$(document).ready(function(){

    $(document).click(function(e){

        var post_id = e.target.getAttribute("id");
        
        isBought(post_id);
    });
});

/* 구매했는지 체크 */
function isBought(post_id) {

    var post_id = post_id

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            if(json.detail.isBuy) {
                window.location.href = "/column/read/"
            }else {
                var preview_img = json.detail.preview_img;
                console.log(json);
                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현

                var img = new Image();
                img.src = json.detail.preview_img;

                $("#preview-main-content > img").replaceWith(img);

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