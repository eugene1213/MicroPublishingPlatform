jQuery(document).ready(function(){
	$(".menuBtn").click(function(event){
		$('.sidebar').stop().css('display','block').animate({opacity : 1});
		event.stopPropagation();
	});
	$('body').click(function(e){
		var clickClassName = e.target.className;
		if(e.target.className == ""
		|| (e.target.className != "" && $(e.target).closest(".sidebar").length == 0)) {
			$('.sidebar').stop().css('display','none').css('opacity',0);
		}
	});
});