$(document).ready(function(){

    $(".priceBtn .btn").click(function() {
        buy();
    });
    $(".preview_purchaseBtn").click(function(){
        buy();
    });
});

function buy(){

    var current_url = window.location.href;
    var tmpStr = current_url.split("/");
        isPreviewPage = tmpStr[tmpStr.length-3]=='preview';

    if(isPreviewPage){
        var post_id = current_url.split("-");
            post_id = post_id[post_id.length-1];
    }else {
        var post_id = $(".priceBtn .btn").attr("id").replace("post","");        
    }

    var author = $('.preview-author').text();
    var title = $('.preview-title').text();
    var urlTitle = title.replace(' ','-').replace(/~|₩|!|@|#|\$|%|\^|&|\*|\(|\)|_|\+|-|=|[|]|\\|\||;|:|'|"|,|.|\/|<|>|\?/g,''); 
    $.ajax({
        url: "/api/column/post-buy/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            post_id: post_id
        },
        success: function(json) {
            console.log("구매됨");
            alert("글을 구매했습니다.");
            window.location.href = "/@"+author+'/'+urlTitle+'-'+post_id;
        },
        error: function(error) {
            console.log(error);
        }
    });
}