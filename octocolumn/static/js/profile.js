$(document).ready(function(){

    var current_url = window.location.href;
    var pk = current_url.split("/");
        pk = pk[pk.length-1];

    $.ajax({
        url: "/api/member/getProfileMainInfo/",
        async: true,
        type: 'POST',
        dataType: 'json',
        data: {
            pk: pk
        },
        success: function(json) {

            console.log(json);
            var cover_img = json.image.cover_image;
            var profile_img = json.image.profile_image;
            var username = json.nickname;
            var waiting = json.waiting;
            
            var userIntro = json.intro;
            var following = json.following;
            var follower = json.follower;
            var posts = json.post_count;
            
            var website = json.web;
            var fb = json.facebook;
            var ins = json.instagram;
            var tw = json.twitter;

            $("#cover").css("background-image",'url(' +cover_img+ ')');
            $("#profileImg").css("background-image",'url(' +profile_img+ ')');
            $(".userName").text(username);
            $(".waiting-wrap > p > span").text(waiting);
            $("#profileIntro").html(userIntro);
            $("#Following").text(following);
            $("#Follower").text(follower);
            $("#posts").text(posts);

            /* setting */
            $(".introduce").html(userIntro);
            $("#myfacebook").val(fb.split('/')[1]);
            $("#myinstagram").val(ins.split('/')[1]);
            $("#mytwitter").val(tw.split('/')[1]);
            $("#mywebsite").val(website);

            if(website)         $(".personal-website a").attr('href','https://'+website);
            if(fb)              $(".facebook a").attr('href','https://'+fb);
            if(ins)             $(".instagram a").attr('href','https://'+ins);
            if(tw)              $(".twitter a").attr('href','https://'+tw);

        },
        error: function(error) {
            console.log(error);
        },
        complete: about()
    });
});

$( function() {
    $( "#datepicker" ).datepicker();
} );

$('.item').on('click', function(e) {
    // toggle arrow
    $('.item').removeClass('active');
    $(this).toggleClass('active');
    
    // toggle content
    var id = $(this).data('id');

    $('.item-detail').removeClass('active');
    $('.item-detail#item-' + id).addClass('active');
});

$('.item').one('click', function(e) {
    var id = $(this).data('id');
    
    switch(id){
        case 1: break;
        case 2: timeline("/api/member/getMyAllPost/"); break;
        case 3: point("/api/member/getPointHistory/");
    }
});

function about(){
    $.ajax({
        url: "/api/member/getProfileSubInfo/",        
        async: true,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            console.log(json);
            var phone = json.phone;
            var email = json.username;

            var birth = json.birthday;
            var gender = json.sex;
            var job = json.jobs;
            var interests = json.subjects;

            $("#phone").text(phone);
            $("#email").text(email);
            $("#birth").text(birth);
            $("#gender").text(gender);
            $("#job").text(job);
            $("#interests").text(interests);

            /* setting */
            $("#HPhone1").val(phone.split('-')[1]);
            $("#HPhone2").val(phone.split('-')[2]);
            $("#datepicker").val(birth);
            $("#myjob").val(job);
            $("#myinterests").val(interests);
            $("#myemail").text(email);
            
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function timeline(url){
    $.ajax({
        url: url,        
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            console.log(json);
            var created_at = json.created_at;
            var results = json.results;
            var next = json.next;
            var previous = json.previous;
            var timelineHtml = '<li class="event">\
                                    <div class="event-title">'+ created_at +'</div>\
                                    <div class="event-content">\
                                        <h3>byCAL 가입</h3>\
                                        <p>byCAL과 함께 새로운 지식을 탐험해보세요. :)</p>\
                                    </div>\
                                </li>';
            if(previous!=null){
                timelineHtml = '';
            }
            for(result in results){
                var pk = results[result].pk;
                var created_date = results[result].created_date;
                var title = results[result].title;
                var msg = '';
                var msg2 = '';
                var href = '';

                if(results[result].is_temp ){
                    msg = '\''+ title + '\' ' + ' 작성중';
                    msg2 = '칼럼을 완성해주세요!';
                    href="/write/"+pk;
                }else if(!results[result].is_temp){
                    msg = '\''+ title + '\' ' + ' 출판';
                    msg2 = '칼럼 보러가기'
                    href="/@author/published-post-"+pk;
                }
                timelineHtml += '<li class="event" id="'+result+'">\
                                    <div class="event-title">'+ created_date +'</div>\
                                    <div class="event-content">\
                                        <h3>'+ msg +'</h3>\
                                        <p><a href="'+href+'">'+ msg2 +'</a></p>\
                                    </div>\
                                </li>';

            }
            $(".timeline").append(timelineHtml);

            if(next==null) {
                $(window).off('scroll');
                return $('.spinner').remove();   
            }

            $(window).unbind('scroll touchmove').on('scroll touchmove',function() { 
                if ($(window).scrollTop() == $(document).height() - window.innerHeight) {
                    if(next!=null) timeline(next);
                } 
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function point(url){
    $.ajax({
        url: url,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {
            
            console.log(jsons);

            var havePoint = jsons.point;
            var pointHtml = '';
            for(i in jsons.results){
                
                var point = jsons.results[i].point;
                var detail = jsons.results[i].history;
                var type = jsons.results[i].point_use_type;
                var date = jsons.results[i].created_at;
                var plus_minus = jsons.results[i].plus_minus;

                date = date.split("T");
                HH   = date[1].split(":")[0];
                MM   = date[1].split(":")[1];

                pointHtml +='<li>\
                                <ul>\
                                    <li class="spend-time">'+date[0]+' '+HH+':'+MM+'</li>\
                                    <li class="spend-amount"><span>'+plus_minus*point+'</span>&nbsp;Point</li>\
                                    <li class="spend-cont">'+detail+'&nbsp;<span>'+type+'</span></li>\
                                </ul>\
                            </li>';
            }
            $('.point-full-sub').append(pointHtml);
            $("#point-amount").text(havePoint);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$( function() {
    $('.btn-send').unbind('click').click(function(){

        var email = $("#emailAddr").val();

        $.ajax({
            url: "/api/member/invite/",
            async: true,
            type: 'POST',
            dataType: 'json',
            data: {email:email},
            success: function(json) {
                var successMsgTitle = '메일이 발송됐습니다.';
                var successMsg = email+'님을 octocolumn Closed-Beta에 초대하셨습니다.';
                modal({
                    type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                    title: successMsgTitle, //Modal Title
                    text: successMsg, //Modal HTML Content
                    size: 'normal', //Modal Size (normal | large | small)
                    center: true, //Center Modal Box?
                    autoclose: false, //Auto Close Modal Box?
                    callback: null, //Callback Function after close Modal (ex: function(result){alert(result);})
                    onShow: function(r) {}, //After show Modal function
                    closeClick: true, //Close Modal on click near the box
                    closable: true, //If Modal is closable
                    theme: 'atlant', //Modal Custom Theme
                    animate: false, //Slide animation
                    background: 'rgba(0,0,0,0.35)', //Background Color, it can be null
                    zIndex: 1050, //z-index
                    template: '<div class="modal-box"><div class="modal-inner"><div class="modal-title"><a class="modal-close-btn"></a></div><div class="modal-text"></div></div></div>',
                    _classes: {
                        box: '.modal-box',
                        boxInner: ".modal-inner",
                        title: '.modal-title',
                        content: '.modal-text',
                        closebtn: '.modal-close-btn'
                    }
                });
            },
            error: function(error) {
                console.log(error);         
            }
        });
    })
});
$("#coverImgInput").change(function() {
    
    readURL(this,"#cover");
});
$("#profileImgInput").change(function() {

    if($("#profileImg").parents().hasClass("tmpWrap")) $("#profileImg").unwrap();
    readURL(this,"#profileImg");
    
    //$(".toggle-wrap .arrow-box .cover-wrap .cover-img-wrap input").css("margin-top","0px");
    
    // $("#profileImg").unbind("load").load(function(){
        
    //     $(".profileimg_save").show();
    // });
    // $(".profileimg_save").unbind('click').click(function(){

    //     uploadProfileImg("profile");
    //     $(".profileimg_save").hide();
    // });
});
function uploadProfileImg(whichImg) {
    
    if(whichImg == "cover") {
        var img = $("#cover").css("background-image");
            img = img.split("url(")[1].split(")")[0];
        var url = "/api/member/usercover-image/";
        var percentage = '';
        console.log(img);

    } else if(whichImg == "profile") {

        var img = $("#profileImg").css("background-image");
        img = img.split("url(")[1].split(")")[0];
        // var marginTop = $("#profileImg").css("top");  //tmpWrap 기준
        //     marginTop = marginTop.replace("px","");

        // var imgHeight = $("#profileImg").height();

        // var overflowY = imgHeight - $("#profileImg").closest(".profile-image-upload-wrap").height();
        // var topPercentage = (overflowY - marginTop) / $("#profileImg").closest(".profile-image-upload-wrap").height() * 100;

        // var marginLeft = $("#profileImg").css("left");
        //     marginLeft = marginLeft.replace("px","");

        // var imgWidth = $("#profileImg").width();

        // var overflowX = imgWidth - $("#profileImg").closest(".profile-image-upload-wrap").width();
        // var leftPercentage = (overflowX - marginLeft) / $("#profileImg").closest(".profile-image-upload-wrap").width() * 100;
            
        // if(marginTop != 0)          var percentage = "y" + topPercentage;
        // else if(marginLeft != 0)    var percentage = "x" + leftPercentage;
        // else {
            // if(overflowY>0) percentage = "y" + topPercentage;
            // else percentage = "x" + leftPercentage;
        // }

        url = "/api/member/profile-image/";
    }
    $.ajax({
        url: url,
        async: true,
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
                $(id).css('background-image', 'url(' +e.target.result+ ')');
                uploadProfileImg('profile');
            }else {
                $(id).css('background-image', 'url(' +e.target.result+ ')');
                uploadProfileImg('cover');
            }
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$(function(){
    $(".btn_save").click(function(){

        var introduce = $(".introduce").html();
        var hpNumber = $(".setting-content > select").val() +'-'+ $("#HPhone1").val() +'-'+ $("#HPhone2").val();
        var website = $("#mywebsite").val();
        var fb = "www.facebook.com/" + $("#myfacebook").val();
        var ins = "www.instagram.com/" + $("#myinstagram").val();
        var tw = "twitter.com/" + $("#mytwitter").val();
        var birthDay = $("#datepicker").val();
        var job = $("#myjob").val();
        var interests = $("#myinterests").val();
        var gender = $(".gender[checked]").val();
        if(gender==1) gender="Male";
        else if(gender==2) gender="Female";
        
        $.ajax({
            url: "/api/member/updateProfile/",
            async: true,
            type: 'POST',
            dataType: 'json',
            data: {
                intro: introduce,                 // 자기소개
                birthday: birthDay,               // 생일
                sex: gender,                      // 성별
                hpNumber: hpNumber,               // 폰번호
                jobs: job,                        // 직업
                web: website,                     // 웹사이트
                fb: fb,                           // 페북
                ins: ins,                         // 인스타
                tw: tw,                           // 트윗
                subject: interests                // 관심분야
            },
            success: function(json) {
                var successMsgTitle = '저장';
                var successMsg = '';
                modal({
                    type: 'inverted', //Type of Modal Box (alert | confirm | prompt | success | warning | error | info | inverted | primary)
                    title: successMsgTitle, //Modal Title
                    text: successMsg, //Modal HTML Content
                    size: 'normal', //Modal Size (normal | large | small)
                    center: true, //Center Modal Box?
                    autoclose: true, //Auto Close Modal Box?
                    callback: null, //Callback Function after close Modal (ex: function(result){alert(result);})
                    onShow: function(r) {}, //After show Modal function
                    closeClick: true, //Close Modal on click near the box
                    closable: true, //If Modal is closable
                    theme: 'atlant', //Modal Custom Theme
                    animate: false, //Slide animation
                    background: 'rgba(0,0,0,0.35)', //Background Color, it can be null
                    zIndex: 1050, //z-index
                    template: '<div class="modal-box"><div class="modal-inner"><div class="modal-title"><a class="modal-close-btn"></a></div><div class="modal-text"></div></div></div>',
                    _classes: {
                        box: '.modal-box',
                        boxInner: ".modal-inner",
                        title: '.modal-title',
                        content: '.modal-text',
                        closebtn: '.modal-close-btn'
                    }
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});