jQuery(document).ready(function(){

	var clicked = 0;
	var menuBtn = $('.menuBtn');
	var sidebar = $('.sidebar');
	var bg = $('.mBg');

	menuBtn.click(function(){
		var tg = $(this);

		if( clicked == 0) {
			sidebar.stop().animate({height:'100%'},700,'swing');
			bg.stop().animate({opacity:1},500).show();
			clicked = 1;
			return clicked;

		} else if( clicked == 1){
			sidebar.stop().animate({height:0},700,'swing');
			bg.animate({opacity:0},500).hide(300);
			clicked = 0;
			return clicked;
		}

	});

	bg.click(function(){

		sidebar.stop().animate({height:0},700,'swing');
		bg.animate({opacity:0},500).hide(300);
		clicked = 0;
	});
	//sidebar.slideUp(0);
}); //ready
