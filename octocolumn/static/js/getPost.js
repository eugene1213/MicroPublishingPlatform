$(document).ready(function(){

    var current_url = window.location.href;
    var post_id = current_url.split("/");
        post_id = post_id[post_id.length-1];

    $.ajax({
        url: "/api/column/post-view/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            console.log(json);
            var cover_img = json.detail.cover_img;
            var title = json.detail.title;
            var author = json.detail.author.username;
            var main_content = json.detail.main_content;
            var tag = json.detail.tag;
            var created_datetime = json.detail.created_datetime;
            var post_id = json.detail.post_id;
            
            $(".mainImg > img").attr("src",cover_img);
            $(".read_wrap > h2").text(title);
            $(".date").text(created_datetime);
            $(".main_content_wrap").append(json.detail.main_content);
            $(".writer > span").text(author);

            //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            coverImgController();

        },
        error: function(error) {
            console.log(error);
            window.location.href = "/"
        }
    });
});
function coverImgController(){

    var imgHeight = window.innerHeight - $(".read_wrap").height() - 32 - 40;

    $(".mainImg > img").height(imgHeight);
}