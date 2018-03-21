$(document).ready(function(){
    btn_activation();
});

// 모달창에서 로그인, 회원가입 탭 클릭시 탭 전환
function signinWith(){
    $(".signin").hide();
    $(".findPass").hide();
    $(".signinWith").show();
}
function signin(){
    $(".signinWith").hide();
    $(".findPass").hide();

    var email = localStorage.getItem("id");

    if(email != ''){

        $("#checkbox-signin").prop("checked","true");
        
        $("#email-signin").val(email);
    }
    $(".signin").show();
}
function signup(){
    $(".term").hide();
    $(".privacy").hide();
}
function check_email(){
    signup_api();
    $(".welcome2 > span").text($("#email-signup").val());
    $(".check_email").show();
}
function term(){
    $(".term").show();
}
function privacy(){
    $(".privacy").show();
}
function btn_activation(){
    $(".agree_checkbox").click(function(){

        if($(".agree_checkbox").is(":checked")){
            $(".btn_signup").removeAttr("disabled");
            $(".btn_signup").removeClass("btn_disabled");
        }else{
            $(".btn_signup").attr("disabled", "true");
            $(".btn_signup").addClass("btn_disabled");
        }
    });
}