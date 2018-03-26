$(document).ready(function(){

    $("#btnFindPass").unbind('click').click(function(){

        findPass();
    });
});

function findPass() {

    var username = $('#username').val();
    $.ajax({
        url: "/api/member/passwordResetEmail/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            username: username
        },
        success: function(json) {
            console.log(json)
        },
        error: function(error) {
            console.log(error);
        }
    });
}