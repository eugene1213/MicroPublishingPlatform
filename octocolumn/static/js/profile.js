$(document).ready(function(){

    $.ajax({
        url: "/api/member/getProfileMainInfo/",
        async: true,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            console.log(json);
            var cover_img = json.image.cover_image;
            var profile_img = json.image.profile_image;
            var username = json.nickname;
            var email = json.username;
            var waiting = json.waiting;
            
            var userIntro = json.intro;
            var following = json.following;
            var follower = json.follower;
            var posts = json.post_count;
            
            var website = json.web;
            var fb = json.facebook;
            var ins = json.instagram;
            var tw = json.twitter;

            $(".profileCover-wrap").css("background-image",'url(' +cover_img+ ')');
            $(".profileImg-wrap > img").attr("src",profile_img);
            $(".userName").text(username);
            $(".waiting-wrap > p > span").text(waiting);
            $("#profileIntro").html(userIntro);
            $("#Following").text(following);
            $("#Follower").text(follower);
            $("#posts").text(posts);

            // if(website)         $(".private-table :contains(웹사이트) + td").text(website);
            // if(fb)              $(".private-table :contains(facebook) + td").text(fb);
            // if(ins)             $(".private-table :contains(instagram) + td").text(ins);
            // if(tw)              $(".private-table :contains(twitter) + td").text(tw);

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
            var interests = json.subject;

            $("#phone").text(phone);
            $("#email").text(email);
            $("#birth").text(birth);
            $("#gender").text(gender);
            $("#job").text(job);
            $("#interests").text(interests);
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
            var timelineHtml = '<li class="event">\
                                    <div class="event-title">'+ created_at +'</div>\
                                    <div class="event-content">\
                                        <h3>octocolumn 가입</h3>\
                                        <p>:)</p>\
                                    </div>\
                                </li>';

            for(result in results){
                var pk = results[result].pk;
                var created_date = results[result].created_date;
                var title = results[result].title;
                var msg = '';
                var href = '';
                results[result].is_temp ? msg = '작성중' : msg = '출판';

                if(results[result].is_temp ){
                    msg = '작성중'
                    href="/write/"+pk;
                }else if(!results[result].is_temp){
                    msg = '출판'
                    href="/@author/published-post-"+pk;
                }
                timelineHtml += '<li class="event" id="'+result+'">\
                                    <div class="event-title">'+ created_date +'</div>\
                                    <div class="event-content">\
                                        <h3>'+ msg +'</h3>\
                                        <p><a href="'+href+'">:)</a></p>\
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

function point(){
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