$(document).ready(function(){

    var current_url = window.location.href;
    var post_id = current_url.split("-");
        post_id = post_id[post_id.length-1];

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            console.log(json)
            var title = json.detail.title;
            var username = json.detail.nickname;
            var urlTitle = title.replace(/~|₩|`|!|@|#|\$|%|\^|&|\*|\(|\)|_|-|\+|=|\[|\]|{|}|\\|\||;|:|'|"|,|\.|\/|<|>|\?/g,'').replace(/\s/g,'-');
            var url = '/@'+ username +'/'+urlTitle+'-'+post_id;
            var href = 'https://www.octocolumn.com/preview'+url;

            if(json.detail.isBuy) {
                window.location.href = url;
            }else {
                // var preview_image = json.detail.preview;

                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현

                var cover_img = json.detail.cover_image;
                var preview = json.detail.preview;
                var price = json.detail.price;
                var date = json.detail.created_datetime;
                var previewHtml = '\
                        <div class="mainImg image-loader" style="background-image: url('+cover_img+');">\
                        </div>\
                        <div class="read_wrap">\
                            <h2>'+title+'</h2>\
                            <div class="write">\
                                <div class="writer">\
                                    by <span>'+username+'</span>\
                                </div>\
                                <div class="date">\
                                    '+date+'\
                                </div>\
                            </div>\
                        </div>\
                        <div class="main_content_wrap">\
                            '+ preview +'\
                        </div>\
                        <div class="read_wrap">\
                            <div class="preview-tag-wrap">\
                            </div>\
                            <div class="read_profile">\
                                <div class="click">\
                                    <div class="sns">\
                                        <div class="fb-share-button" data-href="'+href+'" data-layout="button_count" data-size="small" data-mobile-iframe="true"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fplugins%2F&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">공유하기</a></div>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    ';
                $('.read').html(previewHtml);
                
                $('meta[property="og:url"]').attr('content',href);
                $('meta[property="og:image"]').attr('content',cover_img);
                $('meta[property="og:title"]').attr('content',urlTitle);
            }
            // console.log("isBought: "+json.detail.isBuy);
        },
        error: function(error) {
            console.log(error);
        }
    }).then(function(){
        var descText = $(".read").text().substr(0,100)+'...';
        $('meta[property="og:description"]').attr('content',descText);   
    });
});