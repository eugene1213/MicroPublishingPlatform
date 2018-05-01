/* bookmarking / cancel */
function bookmark(post_id) {
    
    $.ajax({
        url: "/api/member/"+post_id+"/bookmark/",
        // async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            console.log(json);
            json.detail == 'created' ? $("#bookmark_" +post_id+'> i').prop("class","icon-bookmark") : $("#bookmark_"+post_id+'> i').prop("class","icon-bookmark-empty");
        },
        error: function(error) {
            console.log(error);
        }
    });
}