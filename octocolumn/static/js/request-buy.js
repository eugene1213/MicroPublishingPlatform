function buy(post_id){

    var current_url = window.location.href;
    var tmpStr = current_url.split("/");
        isPreviewPage = tmpStr[tmpStr.length-3]=='preview';

    if(isPreviewPage){
        var post_id = current_url.split("-");
            post_id = post_id[post_id.length-1];
    }

    var author = $('#preview-author').text();
    var title = $('#preview-title').text();
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
            alert("글을 구매했습니다.");
            window.location.href = "/@"+author+'/'+urlTitle+'-'+post_id;
        },
        error: function(error) {
            console.log(error);
        }
    });
}