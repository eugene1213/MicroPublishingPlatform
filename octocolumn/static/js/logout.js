$(document).ready(function(){

    $("#logout").click(function(){
        logout();
    });
});
function logout() {

    $.ajax({
        url: "/api/member/logout/",
        async: false,
        type: 'POST',
        success: function() {
            window.location.href = "/";
        },
        error: function(error) {
            console.log(error);
            // window.location.href = "/"
        }
    });
}