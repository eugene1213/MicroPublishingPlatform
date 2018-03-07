$(document).ready(function(){

    var menuText = $(".btn-menu > div").text();
    var windowHeight = window.innerHeight;

    $(".btn-menu > ul").css("height", windowHeight + "px");

    $(".btn-logo-wrap").click(function(e){

        if(e.clientX < 153) {
            if( $(".btn-menu > ul").is(":visible") ){
                $(".btn-menu > ul").slideUp();
                $(".btn-menu > div").text(menuText);
            }else{
                $(".btn-menu > ul").slideDown();
                $(".btn-menu > div").text("Menu");
            }
        }
    });
});