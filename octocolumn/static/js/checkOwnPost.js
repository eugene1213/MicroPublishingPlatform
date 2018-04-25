/* 구매했는지 체크 */
function isBought(post_id, readtime) {

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

                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현

                var cover_img = json.detail.cover_image;
                var preview = json.detail.preview;
                var price = json.detail.price;
                var date = json.detail.created_datetime;
                var previewHtml = '\
                    <div class="preview-wrap">\
                        <div class="preview" id="preview">\
                            <div class="btn-cancel-wrap" onclick="javascript:(function(){$(\'.preview-wrap\').remove();$(\'.page\').css(\'position\', \'static\');})();">\
                                <div class="btn-cancel"></div>\
                                <div class="preview_purchaseBtn" onclick=\'buy();\'>구매</div>\
                            </div>\
                            <div class="ready2publish">Preview</div>\
                            <div class="preview-cover-img" style="background-image:url('+cover_img+')"></div>\
                            <div class="preview-title">'+title+'</div>\
                            <div class="preview-content-info">\
                                <div class="preview-read-time">'+readtime+'</div>\
                                <div class="preview-by">by</div>\
                                <div class="preview-author">'+username+'</div>\
                                <div class="preview-create-date">'+date+'</div>\
                            </div>\
                            <div class="preview-main-content" id="preview-main-content">\
                                <!-- <img src="" alt=""> -->\
                                <div class="previewElementsWrap">'+preview+'</div>\
                                <!-- preview-image -->\
                            </div>\
                            <div class="priceBtn">\
                                <div class="btn" id="post'+post_id+'" onclick=\'buy();\'>'+price+'P로 구매</div>\
                            </div>\
                        </div> \
                    </div>\
                ';
                $('.page').after(previewHtml);
                $(".page").css("position", "fixed");






                // $("#preview-main-content > .previewElementsWrap").replaceWith(preview);
                // $(".previewElementsWrap").children(":last").css("filter","blur(4px)");

                // $("#preview-cover-img").attr("src",cover_img);
                // $(".preview-title").text(title);
                // $(".preview-create-date").text(date);
                // $(".preview-read-time").text(readtime);
                // $(".preview-author").text(username);
                // $(".priceBtn > .btn").text(price + "P로 구매");
                // $(".priceBtn .btn").attr("id","post"+post_id);

                //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
                // $(".preview-wrap").height(1500);
                // $(".preview-wrap").show();
                // $(document).scrollTop($('#preview').offset().top-100);
                // $(window).scroll(function(){
                //     if($(".preview-wrap").css('display')=='block'){
                
                //         if($(document).scrollTop()>$('#preview').offset().top+$('#preview').height()-600){

                //             $(document).scrollTop($('#preview').offset().top+$('#preview').height()-600);
                //         }
                //     }
                // });             
            }
            // console.log("isBought: "+json.detail.isBuy);
        },
        error: function(error) {
            console.log(error);
        }
    });
}