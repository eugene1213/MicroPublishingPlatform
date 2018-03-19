$(document).ready(function(){

    var menuText = $(".btn-menu > div").text();
    var windowHeight = window.innerHeight;

    ($(".btn-user > img").length == 0) ? $(".footer").css("margin-top","600px") : $(".footer").css("margin-top","300px");

    $(".btn-menu > ul").css("height", windowHeight - 32 - 40 + "px");   // 헤더높이 = 32, ul 패딩탑 = 40

    $("body").unbind('click').click(function(e){

        if(e.clientX < 153 && e.clientY < 32) {

            if( $(".btn-menu > ul").is(":visible") ){

                $(".btn-menu > ul").slideUp();
                $(".btn-menu > div").text(menuText);
            }else{

                menuText = $(".btn-menu > div").text();
                $(".btn-menu > ul").slideDown();
                $(".btn-menu > div").text("Menu");
            }
        }else if(e.clientX > 153){
                
            $(".btn-menu > ul").slideUp();
            $(".btn-menu > div").text(menuText);
        }
    });
});