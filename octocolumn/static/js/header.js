$(document).ready(function(){
    $(".btn-logo-wrap").click(function(e){
        if(e.clientX > window.innerWidth - 160) {
            if($(".btn-user > img").length == 0){
                modal_on();
            }
        }
    });
});