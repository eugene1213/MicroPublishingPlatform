$(document).ready(function(){
    
    var current_url = window.location.href;
    var post_id = current_url.split("/");
        post_id = post_id[post_id.length-1];

    hidingHeader();

    $(window).resize(function() {
        coverImgController();
    });
    // 글 로딩
    $.ajax({
        url: "/api/column/postView/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            console.log(json);
            var cover_img = json.detail.cover_img;
            var title = json.detail.title;
            var author = json.detail.author.username;
            var main_content = json.detail.main_content;
            var tagArray = json.detail.tag;
            var created_datetime = json.detail.created_datetime;
            var post_id = json.detail.post_id;

            for(var i in tagArray) {
                
                var tagText = tagArray[i].tag;
        
                $(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tagText+"</div>");
            }
            
            $(".mainImg").css("background-image","url("+cover_img+")");
            $(".read_wrap > h2").text(title);
            $(".date").text(created_datetime);
            $(".main_content_wrap").append(json.detail.main_content);
            $(".writer > span").text(author);

            //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            coverImgController();

        },
        error: function(error) {
            console.log(error);
            // window.location.href = "/"
        }
    });
    // 댓글 로딩
    getComment(post_id);
    
    // 댓글 입력
    $('.comment_button').click(function() {

        var content = $('.input_comment').val();
        insertComment('POST', content, post_id, '');
    });
    // 대댓글 버튼
    $('.re-comment').on('click',function(){

    });
    // 댓글 수정
    $('.comments-list').delegate('.more_option_modify', 'click', function(e) {

        var commentID = $(e.target).closest('.comment-box').attr('id');
        $('#'+commentID+'> .comment-content').prop('contenteditable','true');
        $('#'+commentID+'> .comment-content').focus();
        $('#'+commentID+' .more').hide();
        $('#'+commentID).append('<button type="button" class="modify_button">수정</button>');
    });

    $('.comments-list').delegate('.modify_button','click',function(e) {

        var commentID = $(e.target).closest('.comment-box').attr('id');
        var content = $('#'+commentID+'> .comment-content').text();

        insertComment('PUT', content, post_id, commentID);

        $('.modify_button').remove();
        $('#'+commentID+' .more').show();
        $('#'+commentID+'> .comment-content').prop('contenteditable','false')
    });
    // 댓글 삭제
    $('.comments-list').delegate('.more_option_delete', 'click', function(e) {
        
        var commentID = $(e.target).closest('.comment-box').attr('id');
        console.log(e.target)
        insertComment('DELETE','' , post_id, commentID);
    });

    title2header("read");
});

function coverImgController(){
    
    var imgHeight = window.innerHeight - $(".read_wrap").height() - 32 - 40;

    $(".mainImg").height(imgHeight);
}