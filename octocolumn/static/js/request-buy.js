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
        },
        error: function(error) {
            console.log(error);
        }
    });
}