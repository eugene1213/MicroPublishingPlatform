$(document).ready(function(){

    var current_url = window.location.href;
    var post_id = current_url.split("-");
        post_id = post_id[post_id.length-1];
    var gradientHeight = $('.previewElementsWrap').height();

    $('.gradient').height(gradientHeight);
    coverImgController();
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
            }
        },
        error: function(err){
            console.log(err);
        }
    });
});

function coverImgController(){
    
    var imgHeight = window.innerHeight - $(".read_wrap").height() - 32 - 40;

    $(".mainImg").height(imgHeight);
}