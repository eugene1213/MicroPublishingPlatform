$(document).ready(function(){
    $("#imgInp").change(function() {
        readURL(this);
        
        $(".cover-img-css-wrap").hide();
        $(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
        
        $("#blah").load(function(){
            
            var imgHeight = $(".cover-img-wrap").height();
            $(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").height(imgHeight);
        });
    });

    var fl = document.getElementById('imgInp');

    /* 이미지인지 확인 */
    fl.onchange = function(e){
        var ext = this.value.match(/\.(.+)$/)[1];
        switch(ext)
        {
            case 'jpg':
            case 'jpeg':
            case 'png':
                break;
            default:
                this.value='';
        }
    }
});
/* 이미지 파일 미리보기 */
function readURL(input) {
    
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#blah').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}