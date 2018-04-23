$(document).ready(function(){

    $(".priceBtn .btn").click(function() {
        buy();
    });
    $(".preview_purchaseBtn").click(function(){
        buy();
    });
});

function buy(){

    var post_id = $(".priceBtn .btn").attr("id").replace("post","");
    var author = $('.preview-author').text();
    var urlTitle = $('.preview-title').text().replace(' ','_').replace('-','_');  
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