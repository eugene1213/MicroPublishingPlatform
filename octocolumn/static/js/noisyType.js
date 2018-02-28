var playing = ['paused','paused','paused','paused','paused'];

$(document).keydown(function(event) {

    if($("#btn-on").is(":visible") && ($(event.target).hasClass('editable') || $(event.target).hasClass('title') || $(event.target).hasClass('tag-input'))){
        if ( (event.keyCode > 64 && event.keyCode < 91) || (event.keyCode > 47 && event.keyCode < 58) || (event.keyCode > 95 && event.keyCode < 112) || (event.keyCode > 185 && event.keyCode < 223) || event.keyCode == 229 ) {

            if ( $("#audio_1")[0].paused )      $("#audio_1")[0].play();
            else if ( $("#audio_2")[0].paused ) $("#audio_2")[0].play();
            else if ( $("#audio_3")[0].paused ) $("#audio_3")[0].play();
            else if ( $("#audio_4")[0].paused ) $("#audio_4")[0].play();
            else if ( $("#audio_5")[0].paused ) $("#audio_5")[0].play();
            else if ( $("#audio_6")[0].paused ) $("#audio_6")[0].play();
            else if ( $("#audio_7")[0].paused ) $("#audio_7")[0].play();
            else if ( $("#audio_8")[0].paused ) $("#audio_8")[0].play();
            else if ( $("#audio_9")[0].paused ) $("#audio_9")[0].play();
            
        }else if(event.keyCode == 13) {

            if ( $("#audio_return_1")[0].paused )      $("#audio_return_1")[0].play();
            else if ( $("#audio_return_2")[0].paused ) $("#audio_return_2")[0].play();
            else if ( $("#audio_return_3")[0].paused ) $("#audio_return_3")[0].play();
            else if ( $("#audio_return_4")[0].paused ) $("#audio_return_4")[0].play();

        }else if(event.keyCode == 32) { 

            if ( $("#audio_space_1")[0].paused )      $("#audio_space_1")[0].play();
            else if ( $("#audio_space_2")[0].paused ) $("#audio_space_2")[0].play();
            else if ( $("#audio_space_3")[0].paused ) $("#audio_space_3")[0].play();
            
        }else if(event.keyCode == 8) {

            if ( $("#audio_backspace_1")[0].paused )      $("#audio_backspace_1")[0].play();
            else if ( $("#audio_backspace_2")[0].paused ) $("#audio_backspace_2")[0].play();
            else if ( $("#audio_backspace_3")[0].paused ) $("#audio_backspace_3")[0].play();
        }
    }
});

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

    if($("#btn-on").is(":visible")){
        if (st > lastScrollTop && st > navbarHeight){
            // Scroll Down
            if ( $("#audio_scrollDown")[0].paused ) $("#audio_scrollDown")[0].play();

        } else {
            // Scroll Up
            if(st + $(window).height() < $(document).height()) {
                if ( $("#audio_scrollUp")[0].paused ) $("#audio_scrollUp")[0].play();
            }
        }
    }
    
    lastScrollTop = st;
}