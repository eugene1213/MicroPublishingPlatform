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
    console.log(id)
    switch(id){
        case 1: break;
        case 2: timeline(); break;
        case 3: point();
    }
    $('.item-detail').removeClass('active');
    $('.item-detail#item-' + id).addClass('active');
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

function timeline(){
    $.ajax({
        url: "/api/member/getMyAllPost/",        
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            console.log(json);

        },
        error: function(error) {
            console.log(error);
        }
    });
}

function point(){
    $.ajax({
        url: "/api/member/getProfileSubInfo/",        
        async: true,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            console.log(json);

        },
        error: function(error) {
            console.log(error);
        }
    });
}