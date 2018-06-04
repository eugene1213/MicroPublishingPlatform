function title2header(read_or_write){            // 글 읽기,쓰기 페이지에서 제목에 입력된 값이 헤더 로고에 박힌다.

    if(read_or_write == "write"){                                 // 글쓰기

        var background = $(".site-name").css('background-image');     

        $(".title").focusout(function(){

            var titleText = "";

            if($(".title").text() != "") {

                titleText = $(".title").text();
                $(".site-name").text(titleText);
                $(".site-name").css('background-image','none');

            } else {
                $(".site-name").text("");
                $(".site-name").css('background-image',background);
            }
        });
    } else if(read_or_write == "read"){                           // 글읽기

        var background = $(".site-name").css('background-image');
        titleText = $(".column-title").text();

        $(window).scroll(function(){

            var st = $(document).scrollTop();
            if(st == 0) {
                $(".site-name").text("");      
                $(".site-name").css('background-image',background);
            } else {
                $(".site-name").text(titleText);
                $(".site-name").css('background-image','none');
            }
        });
    }
}
function hidingHeader(){            // 글읽기 페이지에서 스크롤다운 시 헤더 로고가 사라진다.

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
                $("header").slideUp();
                $("#nav-container").slideUp();    
                $(".btn-point").slideUp();                
                $(".profile-img").slideUp();                                
                $("#profile-container").slideUp();                
    
            } else {
                // Scroll Up
                if(st + $(window).height() < $(document).height()) {
                    $("header").slideDown();
                    $("#nav-container").slideDown();
                    $(".btn-point").slideDown();                    
                    $(".profile-img").slideDown();                    
                    $("#profile-container").slideDown();                    
                    
                }
            }
        lastScrollTop = st;
    }
}