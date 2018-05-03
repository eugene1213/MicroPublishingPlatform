$(window).resize(function (){
    $(".modal_window").css("left", (window.innerWidth-944)/2 + "px");
    $(".modal_window").css("top", (window.innerHeight-600)/2 + "px");
});

// 로그인 버튼 클릭시 모달창 온, 오프
function modal_on(){
    $(".modal_block_wrap").show();
    $(".modal_window").css("left", (window.innerWidth-944)/2 + "px");
    $(".modal_window").css("top", (window.innerHeight-600)/2 + "px");
    $(".signin").hide();
    $(".findPass").hide();
    $(".signup").hide();
    $(".check_email").hide();
    $(".term").hide();
    $(".privacy").hide();
    $(".btn-menu > ul").slideUp();
    $(".signinWith").show();
}

function modal_off(){
    $(".modal_block_wrap").hide();
}

// 모달창에서 로그인, 회원가입 탭 클릭시 탭 전환
function signinWith(){
    $(".signin").hide();
    $(".findPass").hide();
    $(".signup").hide();
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
function findPass(){
    $(".signinWith").hide();
    $(".signin").hide();
    $(".findPass").show();
}
function signup(){
    $(".signinWith").hide();
    $(".findPass").hide();
    $(".signin").hide();
    $(".term").hide();
    $(".privacy").hide();
    $(".signup").show();
    checkbox();
    btn_activation();
}
function check_email(){
    signup_api();
    $(".welcome2 > span").text($("#email-signup").val());
    $(".signup").hide();
    $(".check_email").show();
}
function term(){
    $(".signup").hide();
    $(".term").show();
}
function privacy(){
    $(".signup").hide();
    $(".privacy").show();
}

function checkbox(){
    
    $(".checkbox").click(function(){

        $(".checked").addClass("unchecked");  // vx x (x vx)
        $(".checked").removeClass("checked"); // x  x (x x)
        $(this).addClass("checked");          // x  vx(vx x)
        $(this).removeClass("unchecked");     // x  v (v x)
        
        if($(".checked").is("#business")){
            $(".name_wrap > .name > span").text("기업이름");
            $(".name_wrap > .name > input[type=text]").attr("id","businessName-signup");
        }else if($(".checked").is("#normal")){
            $(".name_wrap > .name > span").text("이름");
            $(".name_wrap > .name > input[type=text]").attr("id","nickName-signup");
        }
    });
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