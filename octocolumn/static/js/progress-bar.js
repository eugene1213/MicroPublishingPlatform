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
            var xPos = (100 * parseFloat($(this).css("left"))) / (parseFloat($(this).parent().css("width")))-17 + "%";
            var price = parseInt(1000 * ((parseFloat($(this).css("left"))-40) / 214));
            $('#audio-progress-bar').css({
                'width': xPos
            });
            price = Math.round(price/50)*50;
            $(".price-set-decimal").text(price);
        }
    });
}