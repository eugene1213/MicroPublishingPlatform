function currentPage2header() {

    var current_url = window.location.href;
    var currentPage = current_url.split("/");
        currentPage = currentPage[currentPage.length-2];

        if(currentPage != ""){
            currentPage == "write" ? $(".btn-menu > img + div").text("New Story") : $(".btn-menu > img + div").text(currentPage);
        }else{
            $(".btn-menu > img + div").text("octocolumn");
        }
}
function title2header(){

    $(".title").focusout(function(){

        var titleText = "";

        if($(".title").text() != "") {

            titleText = $(".title").text();
            $(".btn-logo").text(titleText);

            headerController();

        } else $(".btn-logo").text("octocolumn");
    });
}
function hidingHeader(){

    var didScroll;
    var lastScrollTop = 0;
    var delta = 5;
    var navbarHeight = $('header').outerHeight();
    
    $(window).scroll(function(event){
        didScroll = true;
    });
    
    setInterval(function() {
        if (didScroll) {
            hasScrolled();
            didScroll = false;
        }
    }, 250);
    
    function hasScrolled() {
        var st = $(this).scrollTop();
        
        if(Math.abs(lastScrollTop - st) <= delta) return;
    
            if (st > lastScrollTop && st > navbarHeight){
                // Scroll Down
                $(".header").slideUp();
    
            } else {
                // Scroll Up
                if(st + $(window).height() < $(document).height()) {
                    $(".header").slideDown();
                }
            }
        
        lastScrollTop = st;
    }
}