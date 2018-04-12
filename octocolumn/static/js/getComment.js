function getComment(post_id) {
    $.ajax({
        url: "/api/column/"+post_id+"/commentList/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {
            console.log(json);
            console.log(post_id)
        },
        error: function(error) {
            console.log(error);
        }
    });
}