$(document).ready(function(){

    $(document).click(function(e){

        var post_id = e.target.getAttribute("id");
        
        isBought(post_id);
    });
    
});

function isBought(post_id) {

    var post_id = post_id

    $.ajax({
        url: "/api/column/post-isbuy/"+post_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            
            if(json.detail.isBuy) {
                window.location.href = "/column/read/"
            }else {
                var preview_img = json.detail.preview_img;
                // var tag = json.detail.tag;  //미구현
                // var reply = json.detail.reply; //미구현
            }

            console.log("isBought 통신성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}