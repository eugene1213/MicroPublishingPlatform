/* bookmarking / cancel */
function bookmark(post_id) {
    
    $.ajax({
        url: "/api/member/"+post_id+"/bookmark/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            console.log(json.author.bookmark_status);
            json.author.bookmark_status ? $(".btn-follow").text("Following") : $(".btn-follow").text("Follow");
        },
        error: function(error) {
            console.log(error);
        }
    });
}