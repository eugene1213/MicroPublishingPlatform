$(document).ready(function(){

    get_profile();
    getProfileIntro();
    historyBarHeight();

/* start 커버, 프로필 이미지 처리 */
    $("#coverImgInput").change(function() {
        readURL(this,"#coverImg");
        
        //$(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
        
        $("#coverImg").load(function(){
            
            uploadProfileImg("cover");
        });
    });
    $("#profileImgInput").change(function() {
        readURL(this,"#profileImg");
        
        //$(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
        
        $("#profileImg").load(function(){
            
            uploadProfileImg("profile");
        });
    });

    var fl1 = document.getElementById('coverImgInput');
    var fl2 = document.getElementById('profileImgInput');

    /* 이미지인지 확인 */
    fl1.onchange = function(e){
        var ext = this.value.match(/\.(.+)$/)[1];
        switch(ext) {
            case 'jpg':
            case 'jpeg':
            case 'png':
                break;
            default:
                this.value='';
        }
    }
    fl2.onchange = function(e){
        var ext = this.value.match(/\.(.+)$/)[1];
        switch(ext) {
            case 'jpg':
            case 'jpeg':
            case 'png':
                break;
            default:
                this.value='';
        }
    }
/* end 커버, 프로필 이미지 처리 */


    $(".pro_intro_btn").click(function(){

        $("#profileIntro").prop("contenteditable","true");
        //$("#profileIntro").text().length
        $(".pro_intro_btn").hide();

        setCaretAtEnd("#profileIntro");
        $(".pro_intro_btn").hide();
    });
    $("#profileIntro").focusout(function(){

        $("#profileIntro").prop("contenteditable","false");
        $(".pro_intro_btn").show();

        var userIntro = $("#profileIntro").text();
        updateUserIntro(userIntro);
    });
});


function historyBarHeight() {

    var n = $(".history_date2").length + $(".history_date3").length // 말풍선 갯수
    $(".history_bar").height(n * 120);
}
function get_profile() {

    $.ajax({
        url: "/api/member/getProfileInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {
            console.log(json);

            var cover_img = json.image.cover_image;
            var profile_img = json.image.profile_image;
            var username = json.username;
            var waiting = json.waiting;
            // var stamp = json.stamp;
            var userIntro = json.intro;
            var following = json.following;
            var follower = json.follower;
            var posts = json.post_count;

            $(".profile_mainbanner > img").attr("src",cover_img);
            $(".profile_img > img").attr("src",profile_img);
            $(".content_title1 > span").text(username);
            $(".profile_con_icon").text(waiting);
            $("#profileIntro").text(userIntro);
            $("#following").text(following);
            $("#follower").text(follower);
            $("#posts").text(posts);

            historyBarHeight();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function getProfileIntro() {                    // 자기소개 받아온다.

    $.ajax({
        url: "/api/member/getProfileInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var userIntro = json.intro;
            $("#profileIntro").text(userIntro);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function updateUserIntro(userIntro) {             // 수정된 자기소개를 업로드한다.

    $.ajax({
        url: "/api/member/updateProfileIntro/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            userIntro: userIntro
        },
        success: function(json) {

            console.log("자기소개 업데이트 성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function uploadProfileImg(whichImg) {

    if(whichImg == "cover") {
        img = $("#coverImg").attr("src");
        url = "/api/member/usercover-image/";
    } else if(whichImg == "profile") {
        img = $("#profileImg").attr("src");
        url = "/api/member/profile-image/";
    }
    $.ajax({
        url: url,
        async: false,
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(img),
        success: function(json) {
            console.log("이미지 업데이트 성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
}

/* 이미지 파일 미리보기 */
function readURL(input,id) {
    
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $(id).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

function setCaretAtEnd(elem) {
    var elemLen = $(elem).text().length;
    if(elemLen == 0){
     $(elem).focus();
     return;
    }
    // For IE Only
    if (document.selection) {
        console.log(document.selection);
        // Set focus
        $(elem).focus();
        // Use IE Ranges
        var oSel = document.selection.createRange();
        // Reset position to 0 & then set at end
        oSel.moveStart('character', -elemLen);
        oSel.moveStart('character', elemLen);
        oSel.moveEnd('character', 0);
        oSel.select();
    }
    else if (document.selection == undefined || elem.selectionStart || elem.selectionStart == '0') {
        // Firefox/Chrome
        $(elem).focus().text($(elem).text());
    } // if
} // SetCaretAtEnd()