$(document).ready(function(){

    var current_url = window.location.href;
    var post_id = current_url.split("/");
        post_id = post_id[post_id.length-1];

    console.log(post_id);
    $.ajax({
        url: "/api/column/post-view/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            if(json === false) {
                window.location.href = "/"
            }else {
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
                $(".preview-read-time").text(readtime);
                $(".writer > span").text(author);
    
                //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});
