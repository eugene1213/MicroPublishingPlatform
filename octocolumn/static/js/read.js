$(document).ready(function(){
    
    var current_url = window.location.href;
    var post_id = current_url.split("-");
        post_id = post_id[post_id.length-1];

    hidingHeader();

    $(window).resize(function() {
        coverImgController();
    });
    // 글 로딩
    $.ajax({
        url: "/api/column/postView/"+post_id,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            console.log(json);
            var cover_img = json.detail.cover_img;
            var title = json.detail.title;
            var urlTitle = title.replace(/~|₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|'|"|,|\.|\/|<|>|\?/g,'').replace(/\s/g,'-');
            var author = json.detail.author.username;
            var intro = json.detail.author.intro;
            var author_image = json.detail.author.image.profile_image;
            var main_content = json.detail.main_content;
            var tagArray = json.detail.tag;
            var created_datetime = json.detail.created_datetime;
            var post_id = json.detail.post_id;
            var url = '/@'+ author+'/'+urlTitle+'-'+post_id;
            var href = 'https://www.octocolumn.com'+url;

            if(window.location.href != href) history.pushState(null,null,url);   // 유저가 임의로 url 변경시 올바른 url로 조정

            for(var i in tagArray) {
                
                var tagText = tagArray[i].tag;
        
                $(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tagText+"</div>");
            }
            $('meta[property="og:url"]').attr('content',href);
            $('meta[property="og:image"]').attr('content',cover_img);
            $('meta[property="og:title"]').attr('content',title);
            
            
            $('.fb-share-button').attr('data-href', href);
            $(".mainImg").css("background-image","url("+cover_img+")");
            $(".read_wrap > h2").text(title);
            $(".date").text(created_datetime);
            $(".main_content_wrap").html(json.detail.main_content);
            $(".writer > span").text(author);
            $('.picture').css('background-image','url('+author_image+')');
            $('.name').text(author);
            $('.contents > .text').html(intro);
            var descText = $(".main_content_wrap").text().substr(0,100)+'...';
            $('meta[property="og:description"]').attr('content',descText);
            //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
            coverImgController();

        },
        error: function(error) {
            console.log(error);
            // window.location.href = "/";
        }
    });
    // 댓글 로딩
    getComment(post_id,'');
    
    // 댓글 입력
    $('.comment_button').click(function() {

        var content = $('.input_comment').val();
        console.log(content)

        content.length > 0 && content.length <= 1500
        ? insertComment('POST', content, post_id, '')
        : alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.')
    });
    // 대댓글 펼치는 버튼
    $('.comments-list').delegate('.re-comment','click',function(e){

        var commentID = $(e.target).closest('.comment-box').attr('id');
        
        if($(e.target).closest('.comment-main-level').siblings('.reply-list').css('display') == 'none'){

            getComment(post_id, commentID);
            $('#'+commentID).closest('.comment-main-level').siblings('.reply-list').show();
        } else {

            $('#'+commentID+'[class="reply-list"] li .reply-box').remove();
            $(e.target).closest('.comment-main-level').siblings('.reply-list').hide();
        }
    });
    // 대댓글 입력
    $('.comments-list').delegate('.reply_button','click',function(e) {
        
        var content = $(e.target).siblings('.input_reply').val();
        var commentID = $(e.target).closest('.reply-list').attr('id');

        content.length > 0 && content.length <= 1500        
        ? insertComment('POST', content, post_id, commentID)
        : alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.')        
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

        if(content.length > 0 && content.length <= 1500) {
            insertComment('PUT', content, post_id, commentID);
            $('.modify_button').remove();
            $('#'+commentID+' .more').show();
            $('#'+commentID+'> .comment-content').prop('contenteditable','false')
        }else {
            alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.');
        }
    });
    // 대댓글 수정
    $('.reply-list').delegate('.more_option_modify', 'click', function(e) {

        var commentID = $(e.target).closest('.reply-box').attr('id');

        $('#'+commentID+'> .reply-content').prop('contenteditable','true');
        $('#'+commentID+'> .reply-content').focus();
        $('#'+commentID+' .more').hide();
        $('#'+commentID).append('<button type="button" class="modify_button">수정</button>');
    });

    $('.reply-list').delegate('.modify_button','click',function(e) {
        
        var commentID = $(e.target).closest('.reply-box').attr('id');
        var content = $('#'+commentID+'> .reply-content').text();

        if(content.length > 0 && content.length <= 1500) {
            insertComment('PUT', content, post_id, commentID);
            $('.modify_button').remove();
            $('#'+commentID+' .more').show();
            $('#'+commentID+'> .reply-content').prop('contenteditable','false')
        }else {
            alert('댓글을 0 ~ 1500 글자 이내로 입력해주세요.');
        }           
    });

    // 댓글 삭제
    $('.comments-list').delegate('.more_option_delete', 'click', function(e) {
        
        var commentID = $(e.target).closest('.comment-box').attr('id');
        insertComment('DELETE','' , post_id, commentID);
    });
    // 대댓글 삭제
    $('.reply-list').delegate('.more_option_delete', 'click', function(e) {
        
        var commentID = $(e.target).closest('.reply-box').attr('id');
        insertComment('DELETE','' , post_id, commentID);
    });

    title2header("read");

    $('.image-loader').imageloader({
        background: true,
        callback: function (elm) {
            $(elm).fadeIn();
        }
    });
});

function coverImgController(){
    
    var imgHeight = window.innerHeight - $(".read_wrap").height() - 32 - 40;

    $(".mainImg").height(imgHeight);
}
//  우클릭 방지
$(function() {
	$(document).on('contextmenu', function() {
        return false;
    });
});
$(function() {
	$('.main_content_wrap').on('mousedown', function() {
        return false;
    });
});