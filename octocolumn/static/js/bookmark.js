/* bookmarking / cancel */
function bookmark(post_id) {
    
    $.ajax({
        url: "/api/member/"+post_id+"/bookmark/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            console.log(json.author.bookmark_status);
            json.author.bookmark_status ? $("#" +post_id+ ".profile_mark > div").prop("class","icon-bookmark") : $(".profile_mark > div").prop("class","icon-bookmark-empty");
        },
        error: function(error) {
            console.log(error);
        }
    });
}