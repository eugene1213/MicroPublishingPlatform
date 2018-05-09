/* 구매했는지 체크 */
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
                                <div class="column-tags">\
                                    <p>Tags</p>\
                                    <ul>\
                                        '+tagsHtml+'\
                                    </ul>\
                                </div>\
                            </div>\
                            <div class="purchase-btn" onclick=\'buy('+post_id+');\'><span class="column-price">'+price+'</span>Point로 구매하기</div>\
                        </div>\
                    </div>\
                ';

            //     <div class="rating">\
            //     <input id="star5" name="rating" type="radio" value="5"/>\
            //     <label for="star5" class="full iconbtn-star-full"></label>\
            //     <input id="star4.5" name="rating" type="radio" value="4.5"/>\
            //     <label for="star4.5" class="half iconbtn-star-half"></label>\
            //     <input id="star3" name="rating" type="radio" value="3"/>\
            //     <label for="star3" class="full iconbtn-star-full"></label>\
            //     <input id="star3.5" name="rating" type="radio" value="3.5"/>\
            //     <label for="star3.5" class="half iconbtn-star-half"></label>\
            //     <input id="star2" name="rating" type="radio" value="2"/>\
            //     <label for="star2" class="full iconbtn-star-full"></label>\
            //     <input id="star2.5" name="rating" type="radio" value="2.5"/>\
            //     <label for="star2.5" class="half iconbtn-star-half"></label>\
            //     <input id="star1" name="rating" type="radio" value="1"/>\
            //     <label for="star1" class="full iconbtn-star-full"></label>\
            //     <input id="star1.5"  name="rating" type="radio" value="1.5"/>\
            //     <label for="star1.5" class="half iconbtn-star-half"></label>\
            //     <input id="star0"  name="rating" type="radio" value="0"/>\
            //     <label for="star0" class="full iconbtn-star-full"></label>\
            //     <input id="star0.5"  name="rating" type="radio" value="0.5"/>\
            //     <label for="star0.5" class="half iconbtn-star-half"></label>\
            // </div>\
                // var previewHtml = '\
                //     <div class="preview-wrap">\
                //         <div class="preview" id="preview">\
                //             <div class="btn-cancel-wrap" onclick="javascript:(function(){$(\'.preview-wrap\').remove();$(\'.page\').css(\'position\', \'static\');})();">\
                //                 <div class="btn-cancel"></div>\
                //                 <div class="preview_purchaseBtn" onclick=\'buy();\'>구매</div>\
                //             </div>\
                //             <div class="ready2publish">Preview</div>\
                //             <div class="preview-cover-img" style="background-image:url('+cover_img+')"></div>\
                //             <div class="preview-title">'+title+'</div>\
                //             <div class="preview-content-info">\
                //                 <div class="preview-read-time">'+readtime+'</div>\
                //                 <div class="preview-by">by</div>\
                //                 <div class="preview-author">'+username+'</div>\
                //                 <div class="preview-create-date">'+date+'</div>\
                //             </div>\
                //             <div class="preview-main-content" id="preview-main-content">\
                //                 <!-- <img src="" alt=""> -->\
                //                 <div class="previewElementsWrap">'+preview+'</div>\
                //                 <!-- preview-image -->\
                //             </div>\
                //             <div class="priceBtn">\
                //                 <div class="btn" id="post'+post_id+'" onclick=\'buy();\'>'+price+'P로 구매</div>\
                //             </div>\
                //         </div> \
                //     </div>\
                // ';
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
        }
    });
}