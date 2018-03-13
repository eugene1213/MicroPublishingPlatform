$(document).ready(function(){

    //get_profile();

    historyBarHeight();

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

    $(".pro_intro_btn").click(function(){

        $(".profile_introduce").prop("contenteditable","true");
        $(".pro_intro_btn").hide();
    });
    $(".profile_introduce").focusout(function(){

        $(".profile_introduce").prop("contenteditable","false");
        $(".pro_intro_btn").show();

        var userInfo = $(".profile_introduce").text();
        //updateUserInfo(userInfo);
    });
});


function historyBarHeight() {

    var n = $(".history_date2").length + $(".history_date3").length // 말풍선 갯수
    $(".history_bar").height(n * 120);
}
function get_profile() {

    $.ajax({
        url: "/profile/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            cover_img = json.cover_img;
            profile_img = json.profile_img;
            username = json.username;
            user_info = json.user_info;
            waiting = json.waiting;
            stamp = json.stamp;
            following = json.following;
            follower = json.follower;
            posts = json.posts;
            
            $(".profile_mainbanner > img").attr("src",cover_img);
            $(".profile_img > img").attr("src",profile_img);
            $(".content_title1 > span").text(username);
            $(".profile_introduce").text(user_info);
            $(".profile_con_icon").text(waiting);
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
function getUserInfo(userInfo) {

    $.ajax({
        url: "/api/member/profileIntro/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var userIntro = json.userIntro;
            $(".profile_introduce > span").text();
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function updateUserIntro(userIntro) {             // 수정된 자기소개를 업로드한다.

    $.ajax({
        url: "/api/member//",
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