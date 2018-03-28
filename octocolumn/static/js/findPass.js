$(document).ready(function(){

    $("#btnFindPass").unbind('click').click(function(){

        findPass();
    });
    $("#btnResetPass").unbind('click').click(function(){
        
        resetPass();
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
function resetPass() {
    
    var url = window.location.href;
    var token = url.split('/')[url.split('/').length-2];
    var uid = url.split('/')[url.split('/').length-3];
    var pass1 = $('#pass1').val();
    var pass2 = $('#pass2').val();

    console.log(uid);
    console.log(token);
    
    $.ajax({
        url: "/api/member/passwordReset/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            uid: uid,
            token: token,
            password1: pass1,
            password2: pass2
        },
        success: function(json) {
            alert('성공적으로 변경 되었습니다.');
            window.location.href = '/signForm/';
        },
        error: function(error) {
            console.log(error);
        }
    });
}