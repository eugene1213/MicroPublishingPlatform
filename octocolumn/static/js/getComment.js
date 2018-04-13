function getComment(post_id) {

    $.ajax({
        url: "/api/column/"+post_id+"/commentList/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            var results = json.results;
            for(result in results) {
                console.log(results[result])
                var content = results[result].content;
                var created_date = results[result].created_date;
                var date = '';
                var isMyComment = results[result].my_comment;
                var replyCount = results[result].reply_count;
                var username = results[result].username;
                var profile_img = results[result].image.profile_image;
                var pk = results[result].pk;
                
                if(isMyComment) {
                    var optionStr = '\
                        <div class="more_option_me">\
                            <div class="more_option_modify">수정</div>\
                            <div class="more_option_delete">삭제\
                                <div class="more_option_triangle"></div>\
                            </div>\
                        </div>\
                    ';
                } else {
                    var optionStr = '\
                        <div class="more_option_you">\
                            <div class="more_option_accuse more_hover">신고\
                                <div class="more_option_triangle"></div>\
                            </div>\
                        </div>\
                    ';
                }
                var mainCommentStr = '\
                    <li>\
                        <div class="comment-main-level">\
                            <div class="comment-avatar" style="background-image:url(\''+ profile_img +'\')"></div>\
                            <div id="'+ pk +'" class="comment-box">\
                                <div class="comment-head">\
                                    <h6 class="comment-name by-author"><a href="">'+ username +'</a></h6>\
                                    <div class="more">\
                                        <div class="more_icon">\
                                            <span class="dot"></span>\
                                            <span class="dot"></span>\
                                            <span class="dot"></span>\
                                        </div>\
                                        '+ optionStr +'\
                                    </div>\
                                    <span>'+ date +'</span>\
                                </div>\
                                <div class="comment-content">\
                                    '+ content +'\
                                </div>\
                                <div class="comment-foot">\
                                    <div class="re-comment">\
                                        <div class="re-comment-icon"></div>\
                                        <span class="re-comment-count">'+ replyCount +'</span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    </li>\
                ';
                $('#comments-list').append(mainCommentStr);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function insertComment(insertType, content, postID, commentID) {

    // insertType: PUT or POST
    // 댓글=>PUT 대댓글=>POST

    $.ajax({
        url: "/api/column/comment/",
        async: false,
        type: insertType,
        dataType: 'json',
        data: { 
            'comment_id': commentID,
            'content'   : content,
            'post_id': postID
        },
        success: function(json) {

            var profile_img = $('.profile-img').css('background-image');
            var username = $('.profile-text').text();
            if(insertType == 'POST'){
                var mainCommentStr = '\
                    <li>\
                        <div class="comment-main-level">\
                            <div class="comment-avatar" style=\'background-image:'+ profile_img +'\'></div>\
                            <div id="'+ json.detail +'" class="comment-box">\
                                <div class="comment-head">\
                                    <h6 class="comment-name by-author"><a href="">'+ username +'</a></h6>\
                                    <div class="more">\
                                        <div class="more_icon">\
                                            <span class="dot"></span>\
                                            <span class="dot"></span>\
                                            <span class="dot"></span>\
                                        </div>\
                                        <div class="more_option_me">\
                                            <div class="more_option_modify">수정</div>\
                                            <div class="more_option_delete">삭제\
                                                <div class="more_option_triangle"></div>\
                                            </div>\
                                        </div>\
                                    </div>\
                                    <span>1분전</span>\
                                </div>\
                                <div class="comment-content">\
                                    '+ content +'\
                                </div>\
                                <div class="comment-foot">\
                                    <div class="re-comment">\
                                        <div class="re-comment-icon"></div>\
                                        <span class="re-comment-count"></span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    </li>\
                ';
            }

            if(insertType == 'POST') $('#comments-list > li:first').after(mainCommentStr);
            else if (insertType == 'DELETE') {
                
                $('#'+commentID+ '> .re-comment-count').text() != 0
                ? $('#'+commentID+ '> .comment-content').text('deleted content')
                : $('#'+commentID).parent().parent().remove();
            }
            $('.input_comment').val('');
        },
        error: function(error) {
            console.log(error);
        }
    });
}