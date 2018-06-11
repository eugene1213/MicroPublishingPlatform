/* 구매했는지 체크 후 구매하지 않았다면 프리뷰 모달 팝업 */
function isBought(post_id, readtime, bookmark_status) {

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            console.log(json)
            var title = json.detail.title;
            var username = json.detail.nickname;
            if(json.detail.isBuy) {
                var urlTitle = title.replace(/~|₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|'|"|,|\.|\/|<|>|\?/g,'').replace(/\s/g,'-');
                
                window.location.href = "/@"+username+'/'+urlTitle+'-'+post_id;
            }else {
                // var preview_image = json.detail.preview;

                var tags = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현
                var tagsHtml = '';
                for(i in tags){
                    tagsHtml += '<li>'+tags[i].tag+'</li>';
                }
                var cover_img = json.detail.cover_image;
                var preview = json.detail.preview;
                var price = json.detail.price;
                var date = json.detail.created_datetime;
                var point = json.detail.point;
                var ribbonClassName = '';
                
                if(bookmark_status) ribbonClassName = ' marked';

                var previewHtml = '\
                    <div id="preview-container">\
                        <div class="preview-content">\
                            <div class="ribbon'+ribbonClassName+'" onclick="bookmark('+post_id+',true);"></div>\
                            <div class="close" onclick="javascript:(function(){$(\'#preview-container\').remove();$(\'.page\').css(\'position\', \'static\');})();"></div>\
                            <div class="warning-phrase">\
                                이 칼럼의 프리뷰가 마음에 드셨다면 구매 후 완독하여주세요.\
                            </div>\
                            <div class="preview-cover-img" style="background-image:url('+cover_img+')"></div>\
                            <div class="column-preview">\
                                <div class="column-title" id="preview-title">'+title+'</div>\
                                <div class="columnist-info">\
                                    <div class="columnist-name">\
                                        by <span class="user-name"><i id="preview-author">'+username+'</i></span>\
                                    </div>\
                                    <div class="date-published">'+date+'</div>\
                                    <div class="column-read-time">\
                                        <span class="read-time">'+readtime+'</span>\
                                    </div>\
                                </div>\
                                <div class="column-content">\
                                    '+preview+'\
                                <div class="gradient"></div>\
                                </div>\
                                <div class="rating">\
                                    <input id="star10" name="rating" type="radio" value="10"/>\
                                    <label for="star10" class="font-read-star"></label>\
                                    \
                                    <input id="star9" name="rating" type="radio" value="9"/>\
                                    <label for="star9" class="font-read-star-half"></label>\
                                    \
                                    <input id="star8" name="rating" type="radio" value="8"/>\
                                    <label for="star8" class="font-read-star"></label>\
                                    \
                                    <input id="star7" name="rating" type="radio" value="7"/>\
                                    <label for="star7" class="font-read-star-half"></label>\
                                    \
                                    <input id="star6" name="rating" type="radio" value="6"/>\
                                    <label for="star6" class="font-read-star"></label>\
                                    \
                                    <input id="star5" name="rating" type="radio" value="5"/>\
                                    <label for="star5" class="font-read-star-half"></label>\
                                    \
                                    <input id="star4" name="rating" type="radio" value="4"/>\
                                    <label for="star4" class="font-read-star"></label>\
                                    \
                                    <input id="star3"  name="rating" type="radio" value="3"/>\
                                    <label for="star3" class="font-read-star-half"></label>\
                                    \
                                    <input id="star2"  name="rating" type="radio" value="2"/>\
                                    <label for="star2" class="font-read-star"></label>\
                                    \
                                    <input id="star1"  name="rating" type="radio" value="1"/>\
                                    <label for="star1" class="font-read-star-half"></label>\
                                </div>\
                                <div class="column-tags">\
                                <p>Tags</p>\
                                <ul>\
                                    '+tagsHtml+'\
                                </ul>\
                            </div>\
                            </div>\
                            <div class="balance">'+point+'</div>\
                            <div class="purchase-btn" onclick=\'buy('+post_id+');\'><span class="column-price">'+price+'</span>Point로 구매하기</div>\
                        </div>\
                    </div>\
                ';
                
                $('.page').after(previewHtml);
                $(".page").css("position", "fixed"); 
            }
            // console.log("isBought: "+json.detail.isBuy);
        },
        error: function(error) {
            console.log(error);
        },
        complete: function(){
            var contentHeight = $('.column-content').height();
            $('.gradient').height(contentHeight);
            $(window).resize(function(){
                contentHeight = $('.column-content').height();
                $('.gradient').height(contentHeight);
            });
            $('.balance:contains(로그인 해주세요)').click(function(){
                $('#preview-container').remove();
                modalSignin();
            });
        }
    });
}