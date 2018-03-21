$(document).ready(function(){

    get_profile();                                  // profile 페이지 첫 로딩 시 데이터 받아옴

    $(".profile_tab1").click(function(){
        
        $(".active").removeClass("active");
        $(this).addClass("active");

                                                    // 개인정보 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-userInfo").css("display","flex");
        $(".currentView").removeClass("currentView");
        $(".profile-userInfo").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab2").click(function(){
        
        $(".active").removeClass("active");
        $(this).addClass("active");

        $(".point-history-wrap tr").not("#tr-header").remove();
        getPointHistory();                          // 포인트내역 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-point-history").show();
        $(".currentView").removeClass("currentView");
        $(".profile-point-history").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab3").click(function(){

        $(".flip").remove();
        $(".active").removeClass("active");
        $(this).addClass("active");

        getUserCard("Following");                              // 관계 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-relationship").show();
        $(".currentView").removeClass("currentView");
        $(".profile-relationship").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();

        $('.tab:contains(Following)').click(function(){
            $(".flip").remove();
            getUserCard("Following");
        });
        $('.tab:contains(Follower)').click(function(){
            $(".flip").remove();
            getUserCard("Follower");
        });
        // $("#1:contains(Following)").click().bind(function(){
        //     var user_id = $(e.target).attr("id");
        //     console.log(1);
        //     follow(user_id);
        // });
    });
    $(".profile_tab4").click(function(){
        
        alert("준비중입니다.")
        // $(".active").removeClass("active");
        // $(this).addClass("active");

                                                    // 업적 탭 클릭 시 보여줄 팔로잉 목록 호출

        // $(".profile-userInfo").css("display","flex");
        // $(".currentView").removeClass("currentView");
        // $(".profile-userInfo").addClass("currentView");
        // $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab5").click(function(){
        
        $(".active").removeClass("active");
        $(this).addClass("active");

                                                    // 계정정보 탭 클릭 시 보여줄 팔로잉 목록 호출

        $(".profile-userInfo").css("display","flex");
        $(".currentView").removeClass("currentView");
        $(".profile-userInfo").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });
    $(".profile_tab6").click(function(){

        $(".active").removeClass("active");
        $(this).addClass("active");

        get_my_posts("post");                       // 내 글 탭 클릭 시 보여줄 글 목록

        $(".profile_history").show();
        $(".currentView").removeClass("currentView");
        $(".profile_history").addClass("currentView");
        $(".profile-infomations").not(".currentView").hide();
    });

    $(".pro_his_tit1").addClass("on");

    $(".pro_his_tit2").click(function(){

        if($(".pro_his_tit1").hasClass("on")){
            $(".history_date2").remove();
            $(".history_date3").remove();
            get_my_posts("temp");
        }
        $(".pro_his_tit1").removeClass("on");
        $(".pro_his_tit2").addClass("on");
        
    });
    $(".pro_his_tit1").click(function(){
        
        if($(".pro_his_tit2").hasClass("on")){
            $(".history_date2").remove();
            $(".history_date3").remove();
            get_my_posts("post");
        }
        $(".pro_his_tit2").removeClass("on");
        $(".pro_his_tit1").addClass("on");

        
    });
/* start 커버, 프로필 이미지 업로드 처리 */

    $("#coverImgInput").change(function() {

        readURL(this,".profile_mainbanner");
    });

    $("#profileImgInput").change(function() {

        if($("#profileImg").parents().hasClass("tmpWrap")) $("#profileImg").unwrap();
        readURL(this,"#profileImg");
        
        //$(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
        
        $("#profileImg").unbind("load").load(function(){
            
            $(".profileimg_save").show();
            
        });
        $(".profileimg_save").unbind('click').click(function(){

            uploadProfileImg("profile");
            $(".profileimg_save").hide();
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

/* start 자기소개 수정 및 업로드 */
    $(".pro_intro_btn").click(function(){

        $("#profileIntro").prop("contenteditable","true");
        //$("#profileIntro").text().length
        $(".pro_intro_btn").hide();
        $("#profileIntro").focus();

        $('div[contenteditable="true"]').keypress(function(event) {
            
            if (event.which != 13)
                return true;
        
            var docFragment = document.createDocumentFragment();
        
            //add a new line
            var newEle = document.createTextNode('\n');
            docFragment.appendChild(newEle);
        
            //add the br, or p, or something else
            newEle = document.createElement('br');
            docFragment.appendChild(newEle);
        
            //make the br replace selection
            var range = window.getSelection().getRangeAt(0);
            range.deleteContents();
            range.insertNode(docFragment);
        
            //create a new range
            range = document.createRange();
            range.setStartAfter(newEle);
            range.collapse(true);
        
            //make the cursor there
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        
            return false;
        });
    });
    $("#profileIntro").focusout(function(){

        $("#profileIntro").prop("contenteditable","false");
        $(".pro_intro_btn").show();

        var userIntro = $("#profileIntro").html();
        updateUserIntro(userIntro);
    });
/* end 자기소개 수정 및 업로드 */
    $(".btn-modify").click(function(){
        
        if($(this).hasClass("btn-save")){
            
            modifyProfile();
        }else{
            
            $(".table-wrap td:nth-child(2)").not("#email, #subject").prop("contenteditable","true");
            $(".btn-modify > img").attr("src","example/save.svg");
            $(".btn-modify").addClass("btn-save");
        
            $('td[contenteditable="true"]').keypress(function(event) {
                
                if (event.which == 13)
                    return false;
            });
        }
    });
});

/* 커버이미지, 프로필이미지, 이름, 기다림, 팔로워, 팔로잉, 출판 글 수 */
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
            var username = json.nickname;
            var waiting = json.waiting;
            // var stamp = json.stamp;
            var userIntro = json.intro;
            var following = json.following;
            var follower = json.follower;
            var posts = json.post_count;

            var birthYear = json.birthYear;
            var birthMonth = json.birthMonth;
            var birthDay = json.birthDay;
            var gender = json.sex;
            var age = json.age;

            var hpNumber = json.phone;
            var location = json.region;
            var email = json.email;

            var job = json.jobs;
            var website = json.web;
            var fb = json.facebook;
            var ins = json.instagram;
            var tw = json.twitter;
            var subject = json.subjects;
            
            $(".profile_mainbanner").css("background",'url(' +cover_img+ ')');
            $(".profile_img > img").attr("src",profile_img);
            $(".content_title1 > span").text(username);
            $(".profile_con_icon").text(waiting);
            $("#profileIntro").html(userIntro);
            $("#following").text(following);
            $("#follower").text(follower);
            $("#posts").text(posts);

            if(birthYear)       $(".base-table :contains(태어난 년도) + td").text(birthYear);
            if(birthMonth)      $(".base-table :contains(생일) + td").text(birthMonth + "월" + birthDay + "일");
            if(gender)          $(".base-table :contains(성별) + td").text(gender);
            if(age > 0)         $(".base-table :contains(나이) + td").text(age);

            if(hpNumber)        $(".contact-table :contains(휴대폰) + td").text(hpNumber);
            if(location)        $(".contact-table :contains(지역) + td").text(location);
            if(email)           $(".contact-table :contains(이메일) + td").text(email);

            if(job)             $(".private-table :contains(직업) + td").text(job);
            if(website)         $(".private-table :contains(웹사이트) + td").text(website);
            if(fb)              $(".private-table :contains(facebook) + td").text(fb);
            if(ins)             $(".private-table :contains(instagram) + td").text(ins);
            if(tw)              $(".private-table :contains(twitter) + td").text(tw);
            if(subject)         $(".private-table :contains(관심분야) + td").text(subject);

            historyBarHeight();

            // $("#coverImg").load(function(){
            //     loadCropImage("#coverImg");
            // });
            $("#profileImg").load(function(){
                loadCropImage("#profileImg");
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
}
function modifyProfile() {

    var birthYear = $("#birthYear").text().replace("년","");
    var birthMonth = $("#birthMonthDate").text().replace("월","").replace("일","");
    var birthDay = $("#birthMonthDate").text().replace("월","").replace("일","");
    var gender = $("#gender").text();
    var age = $("#age").text();
    var hpNumber = $("#hpNumber").text();
    var location = $("#location").text();   
    var job = $("#job").text();
    var website = $("#website").text();
    var fb = $("#fb").text();
    var ins = $("#ins").text();
    var tw = $("#tw").text();
    var subject = $("#subject").text();

    $.ajax({
        url: "/api/member/updateProfile/",
        async: false,
        type: 'POST',
        data: {
            birthYear: birthYear*1,           // 태어난 년도
            birthMonth: birthMonth*1,         // 생월
            birthDay: birthDay*1,             // 생일
            sex: gender,                      // 성별
            age: age*1,                       // 나이
            hpNumber: hpNumber,               // 폰번호
            region: location,                 // 지역
            job: job,                         // 직업
            web: website,                     // 웹사이트
            fb: fb,                           // 페북
            ins: ins,                         // 인스타
            tw: tw,                           // 트윗
            subject: subject                  // 관심분야
        },
        dataType: 'json',
        success: function() {

            $(".btn-modify > img").attr("src","example/write.png");
            $(".table-wrap td:nth-child(2)").not("#email, #subject").prop("contenteditable","false");
            $(".btn-save").removeClass("btn-save");
        },
        error: function(error) {
            console.log(error);
        }
    });
}
/* 수정된 자기소개를 업로드한다. */
function updateUserIntro(userIntro) {             

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
/* 프로필 이미지 업로드 */
function uploadProfileImg(whichImg) {

    if(whichImg == "cover") {
        var img = $(".profile_mainbanner").css("background");
            img = img.split("url(")[1].split(")")[0];
        var url = "/api/member/usercover-image/";
        var percentage = '';
        console.log(img);

    } else if(whichImg == "profile") {

        img = $("#profileImg").attr("src");


        var marginTop = $("#profileImg").css("top");  //tmpWrap 기준
            marginTop = marginTop.replace("px","");

        var imgHeight = $("#profileImg").height();

        var overflowY = imgHeight - $("#profileImg").closest(".profile-image-upload-wrap").height();
        var topPercentage = (overflowY - marginTop) / $("#profileImg").closest(".profile-image-upload-wrap").height() * 100;

        var marginLeft = $("#profileImg").css("left");
            marginLeft = marginLeft.replace("px","");

        var imgWidth = $("#profileImg").width();

        var overflowX = imgWidth - $("#profileImg").closest(".profile-image-upload-wrap").width();
        var leftPercentage = (overflowX - marginLeft) / $("#profileImg").closest(".profile-image-upload-wrap").width() * 100;
         
        if(marginTop > 0)var percentage = "y" + topPercentage;
        else             var percentage = "x" + leftPercentage;

        percentage = percentage.replace('.','d');
        url = "/api/member/profile-image/";
    }
    $.ajax({
        url: url,
        async: false,
        type: 'POST',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify({
            img: img,
            margin: percentage
        }),
        success: function(json) {
            console.log("이미지 업로드 성공!");
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

            if(id == "#profileImg"){
                $(id).attr('src', e.target.result).load(function(){
                    setMargin(id);
                });     // 이미지가 로드 된 후 setMargin 함수 호출
            }else {
                $(id).css('background', 'url(' +e.target.result+ ')');
                uploadProfileImg('cover');
            }
        }

        reader.readAsDataURL(input.files[0]);
    }
}

/* 포인트 내역을 불러온다. */
function getPointHistory() {

    $.ajax({
        url: "/api/member/getPointHistory/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {
            
            console.log(jsons);
            if(jsons.results.length == 0){
                $("th").remove();
            }

            var havePoint = jsons.point;

            for(i in jsons.results){
                
                var point = jsons.results[i].point;
                var detail = jsons.results[i].history;
                var type = jsons.results[i].point_use_type;
                var date = jsons.results[i].created_at;
                var plus_minus = jsons.results[i].plus_minus;

                    date = date.split("T");

                    yyyy = date[0].split("-")[0];
                    mm   = date[0].split("-")[1];
                    dd   = date[0].split("-")[2];

                    HH   = date[1].split(":")[0];
                    MM   = date[1].split(":")[1];


                var str =   "<tr> \
                                <td>" + yyyy + "년 " + mm*1 + "월 " + dd*1 + "일 " + HH + ":" + MM + "</td> \
                                <td>" + point*plus_minus + "point</td> \
                                <td>" + detail + " <span id=\"stat\">" + type + "</span></td> \
                            </tr>";
                
                $(".point-history-wrap").append(str);
            }
            $("#point-amount").text(havePoint);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
