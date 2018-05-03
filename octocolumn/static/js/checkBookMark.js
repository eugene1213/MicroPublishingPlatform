/* bookmarking / cancel */
function bookmark(post_id,isPreview) {
    
    $.ajax({
        url: "/api/member/"+post_id+"/bookmark/",
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            console.log(json);
            
            if(isPreview){
                json.detail == 'created' ? $('.ribbon').addClass('marked') : $('.ribbon').removeClass('marked');
            }else{
                json.detail == 'created' ? $("#bookmark_" +post_id+'> i').prop("class","icon-bookmark") : $("#bookmark_"+post_id+'> i').prop("class","icon-bookmark-empty");
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}