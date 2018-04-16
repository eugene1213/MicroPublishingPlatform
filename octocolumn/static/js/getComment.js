/* 댓글 불러오기 */
function getComment(post_id, commentID) {

    var url = '/api/column/'+post_id+'/commentList/';

    if(commentID!='') url += commentID + '/' ;
    /*
    * 여기서 commentID는 부모 댓글의 ID다.
    * 이 값이 없으면 부모댓글, 있으면 자식댓글(대댓글)이다.
    * 자식댓글의 경우 url은
    * '/api/column/'+post_id+'/commentList/'+commentID+'/'
    * 가 된다. 
    */
    $.ajax({
        url: url,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            var results = json.results;

            for(result in results) {
                console.log(results[result])
                var content = results[result].content;                  // 내용
                var created_date = results[result].created_date;        // 작성일시 타임스탬프
                var date = '';
                var isMyComment = results[result].my_comment;           // 접속자의 댓글여부
                var replyCount = results[result].reply_count;           // 대댓글 수
                var username = results[result].username;                // 댓글 작성자 이름
                var profile_img = results[result].image.profile_image;  // 댓글 작성자 프로필 사진
                var pk = results[result].pk;                            // 고유키
                
                if(isMyComment) {   // 접속자의 댓글인지 확인
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
                if(content.trim() == '삭제된 댓글입니다.') optionStr = '';

                var commentStr = '';

                if(commentID == ''){
                    commentStr = '\
                        <li>\
                            <div class="comment-main-level">\
                                <div class="comment-avatar image-loader" style="background-image:url(\''+ profile_img +'\')"></div>\
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
                            <ul id="'+ pk +'" class="reply-list">\
                                <li>\
                                </li>\
                                <li>\
                                    <div class="input_reply_container">\
                                        <textarea class="input_reply" placeholder="댓글을 입력해주세요." cols="" rows="1"></textarea>\
                                        <button type="button" class="reply_button">입력</button>\
                                    </div>\
                                </li>\
                            </ul>\
                        </li>\
                    ';
                    $('#comments-list').append(commentStr);
                } else {
                    commentStr = '\
                        <div id="'+ pk +'" class="reply-box">\
                            <div class="reply-head">\
                                <div class="reply-avatar image-loader" style=\'background-image:url('+ profile_img +')\'></div>\
                                <h6 class="reply-name"><a href="">'+ username +'</a></h6>\
                                <div class="more">\
                                    <div class="more_icon">\
                                        <span class="dot"></span>\
                                        <span class="dot"></span>\
                                        <span class="dot"></span>\
                                    </div>\
                                    '+ optionStr +'\
                                </div>\
                                <span></span>\
                            </div>\
                            <div class="reply-content">\
                                '+ content +'\
                            </div>\
                        </div>\
                    ';
                    $('#'+commentID+'[class="reply-list"] > li:first').prepend(commentStr);
                }
                
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}
/* 댓글 작성,수정,삭제하기 */
function insertComment(insertType, content, postID, commentID) {

    // insertType: PUT or POST or DELETE
    // 수정=>PUT 입력=>POST 삭제=>DELETE

    $.ajax({
        url: "/api/column/comment/",
        async: true,
        type: insertType,
        dataType: 'json',
        data: { 
            'comment_id': commentID,
            'content'   : content,
            'post_id'   : postID
        },
        success: function(json) {

            var profile_img = $('.profile-img').css('background-image');
            var username = $('.profile-text').text();
            var commentStr = '';
            
            if(insertType == 'POST' && commentID == ''){
                commentStr = '\
                    <li>\
                        <div class="comment-main-level">\
                            <div class="comment-avatar image-loader" style=\'background-image:'+ profile_img +'\'></div>\
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
                                        <span class="re-comment-count">0</span>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                        <ul id="'+ json.detail +'" class="reply-list">\
                            <li>\
                            </li>\
                            <li>\
                                <div class="input_reply_container">\
                                    <textarea class="input_reply" placeholder="댓글을 입력해주세요." cols="" rows="1"></textarea>\
                                    <button type="button" class="reply_button">입력</button>\
                                </div>\
                            </li>\
                        </ul>\
                    </li>\
                ';
            }else if(insertType == 'POST' && commentID != '') {
                commentStr = '\
                    <div id="'+ json.detail +'" class="reply-box">\
                        <div class="reply-head">\
                            <div class="reply-avatar image-loader" style=\'background-image:'+ profile_img +'\'></div>\
                            <h6 class="reply-name"><a href="">'+ username +'</a></h6>\
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
                        <div class="reply-content">\
                            '+ content +'\
                        </div>\
                    </div>\
                ';
            }

            if(insertType == 'POST') {
                commentID == ''
                ? $('#comments-list > li:first').after(commentStr)
                : $('#'+commentID+'[class="reply-list"] > li:first').append(commentStr);

                $('.input_comment').val('');
                $('.input_reply').val('');
            }
            else if (insertType == 'DELETE') {
                
                $('#'+commentID+ ' .re-comment-count').length
                ? ( $('#'+commentID+ ' .re-comment-count').text() != '0'
                ?   $('#'+commentID+ ' .comment-content').text('삭제된 댓글입니다.')
                :   $('#'+commentID).parent().parent().remove() )
                : $('#'+commentID).remove();
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}