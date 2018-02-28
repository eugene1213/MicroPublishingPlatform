function title2header(){
    $(".title").focusout(function(){

        var titleText = "";

        if($(".title").text() != "") {

            titleText = $(".title").text();
            $("#header-title").text(titleText);

            headerController();

        } else $("#header-title").text("octocolumn");
    });
}