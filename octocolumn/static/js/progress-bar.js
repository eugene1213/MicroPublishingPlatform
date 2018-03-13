$(document).ready(function() {
    progressBar();
});

function progressBar(){
    $('#draggable-point').draggable({
        axis: 'x',
        containment: "#audio-progress"
    });

    $('#draggable-point').draggable({
        drag: function() {
            var maxPrice = 200;             // 최대 가격 변경 시 이 변수 수정
            var smallestUnit = 50;          // 가격 설정 최소 단위 변경 시 이 변수 수정
            var xPos = ( 100 * parseFloat($(this).css("left")) ) / ( parseFloat($(this).parent().css("width"))) - 17 + "%";
            var price = parseInt( maxPrice * (( parseFloat( $(this).css("left") ) - 40 ) / 214 ));
            $('#audio-progress-bar').css({
                'width': xPos
            });
            price = Math.round( price / smallestUnit ) * smallestUnit;
            $(".price-set-decimal").text(price);
        }
    });
}