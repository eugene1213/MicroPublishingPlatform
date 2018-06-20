$(document).ready(function() {
    progressBar();
});

function progressBar(){

    $('#draggable-point').draggable({
        axis: 'x',
        containment: "#audio-progress",
        drag: function() {
            var maxPrice = 1000;             // 최대 가격 변경 시 이 변수 수정
            var smallestUnit = 100;          // 가격 설정 최소 단위 변경 시 이 변수 수정
            // var xPos = ( 100 * parseFloat($(this).css("left")) ) / ( parseFloat($(this).parent().css("width"))) - 20 + "%";
            var price = parseInt( maxPrice * (( parseFloat( $(this).css("left").replace('px','')-20 ) ) / 254 ));
            var xPos = price/10 + "%";
            $('#audio-progress-bar').css({
                'width': xPos
            });
            price = Math.round( price / smallestUnit ) * smallestUnit;
            $(".price-set-decimal").text(price);
        }
    });
}