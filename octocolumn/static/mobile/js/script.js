/*jQuery(document).ready(function(){
	$(".menuBtn").click(function(event){
		$('.sidebar').stop().css('display','block').animate({opacity : 1});
		// 클릭이벤트는 아래 코드를 사용하지 않으면 클릭이벤트가 상위로 점점 퍼져가는 이벤트버블링이 생기므로 아래 body클릭이벤트코드가 실행된다.
		event.stopPropagation();
		//$('html').stop().css('overflow-y', 'hidden');
	});
	$('body').click(function(e){
		// 클릭된 Dom의 클래스네임이 무엇인지 확인한다.
		var clickClassName = e.target.className;
		// 클릭된 Dom의 클레스 네임이 없거나
		// 또는 클릭된 Dom의 클래스명이 있고 부모중에 sidebar클래스를 가진Dom이 없을경우 메뉴를 hide 해준다.
		if(e.target.className == ""
		|| (e.target.className != "" && $(e.target).closest(".sidebar").length == 0)) {
			//$('.sidebar').hide();
			$('.sidebar').stop().css('display','none').css('opacity',0);
		}
		//$('html').stop().css('overflow-y', 'scroll');
	});*/

  // button

		/*$('.menuBtn').click(
			function(){
				$('.sidebar').animate({height:'100%'},700,'swing');
				$('.mBg').css('display','block');
				$('.mBg').animate({opacity:1},500);
				//$('.mM_close').fadeIn(600);
			});

		$('.mM_close > a').click(
			function(){
				$('.sidebar').animate({height:0},700,'swing');
				$('.mBg').animate({opacity:0},500);
				$('.mBg').css('display','none');
				//$('.mM_close').fadeOut(600);
			})

});*/

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
