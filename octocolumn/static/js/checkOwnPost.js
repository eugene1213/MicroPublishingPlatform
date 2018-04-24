/* 구매했는지 체크 */
function isBought(post_id, cover_img, title, date, username, readtime, price, preview) {

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            console.log(json)
            if(json.detail.isBuy) {
                var urlTitle = title.replace(' ','-').replace(/~|₩|!|@|#|\$|%|\^|&|\*|\(|\)|_|\+|-|=|[|]|\\|\||;|:|'|"|,|.|\/|<|>|\?/g,'');

                window.location.href = "/@"+username+'/'+urlTitle+'-'+post_id;
            }else {
                // var preview_image = json.detail.preview;

                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현

                // var img = new Image();
                // img.src = json.detail.preview;

                var previewHtml = '\
                    <div class="preview-wrap">\
                        <div class="preview" id="preview">\
                            <div class="btn-cancel-wrap">\
                                <div class="btn-cancel"></div>\
                                <div class="preview_purchaseBtn">구매</div>\
                            </div>\
                            <div class="ready2publish">Preview</div>\
                            <div class="preview-cover-img">\
                                <img id="preview-cover-img" src="" alt="">\
                            </div>\
                            <div class="preview-title"></div>\
                            <div class="preview-content-info">\
                                <div class="preview-read-time"></div>\
                                <div class="preview-by">by</div>\
                                <div class="preview-author"></div>\
                                <div class="preview-create-date">2018. 01. 01 00:00</div>\
                            </div>\
                            <div class="preview-main-content" id="preview-main-content">\
                                <!-- <img src="" alt=""> -->\
                                <div class="previewElementsWrap"></div>\
                                <!-- preview-image -->\
                            </div>\
                            <div class="priceBtn">\
                                <div class="btn">P로 구매</div>\
                            </div>\
                        </div> \
                    </div>\
                '







                $("#preview-main-content > .previewElementsWrap").replaceWith(preview);
                $(".previewElementsWrap").children(":last").css("filter","blur(4px)");

                $("#preview-cover-img").attr("src",cover_img);
                $(".preview-title").text(title);
                $(".preview-create-date").text(date);
                $(".preview-read-time").text(readtime);
                $(".preview-author").text(username);
                $(".priceBtn > .btn").text(price + "P로 구매");
                $(".priceBtn .btn").attr("id","post"+post_id);

                //$(".preview-tag-wrap").append("<div class=\"preview-tag\" id=\"preview-tag-"+i+"\">"+tag+"</div>");
                $(".preview-wrap").height(1500);
                $(".preview-wrap").show();
                $(document).scrollTop($('#preview').offset().top-100);
                $(window).scroll(function(){
                    if($(".preview-wrap").css('display')=='block'){
                
                        if($(document).scrollTop()>$('#preview').offset().top+$('#preview').height()-600){

                            $(document).scrollTop($('#preview').offset().top+$('#preview').height()-600);
                        }
                    }
                });             
            }
            console.log("isBought: "+json.detail.isBuy);
        },
        error: function(error) {
            console.log(error);
        }
    });
}