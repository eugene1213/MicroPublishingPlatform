$(document).ready(function(){
    headerController();
});

$(window).resize(function (){
    headerController();
    $(".modal_window").css("left", (window.innerWidth-944)/2 + "px");
    $(".modal_window").css("top", (window.innerHeight-600)/2 + "px");
});
// 헤더가 브라우저 크기에 맞게 조정
function headerController(){

    var windowWidth = window.innerWidth;
    var W = $('.header-wrap').width();
    var menuWidth = $('.btn-menu').width();
    var searchWidth = $('.btn-search').width();
    var pointWidth = $('.btn-point').width();
    var noticeWidth = $('.btn-notice').width();
    var userWidth = $('.btn-user').width();
    var logoWidth = $("#header-title").width();

    var marginWidth = W - menuWidth - searchWidth - pointWidth - noticeWidth - userWidth - 70;
    var logoMarginLeft = (windowWidth - 130)/2;

    if(windowWidth < 605 + logoWidth){

        $(".btn-logo-wrap").width(628 + logoWidth);
        if(logoWidth > 116){
            $(".header-wrap").css("min-width", 628 + (logoWidth - 116));
        }else{
            $(".header-wrap").attr("style","");
        }
    }else{

        $(".btn-logo-wrap").width(windowWidth);
    }
}
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