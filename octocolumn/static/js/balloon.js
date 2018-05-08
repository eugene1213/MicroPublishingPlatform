//프로필 사진에 마우스 오버하면 비어있는 풍선에 내용이 추가됨(ajax사용)과 동시에 프로필 사진 위에 나타남.
//마우스 오버되면 풍선을 노출시키고 마우스가 일정 영역 밖으로 이동하면 사라진다.

function popBalloon() { //getPostList.js 에서 호출한다.

    $(".page").delegate('.user-pic','mouseenter', function(e){

        console.log($(e.target).offset());
        var pk = $(this).attr("id").replace('author_','');
        
        $.ajax({
            url: "/api/member/"+ pk +"/followStatus/",
            async: true,
            type: 'GET',
            dataType: 'json',
            success: function(jsons) {
    
                var followers = jsons.follower_count;
                var follow_status = jsons.follow_status;
                var author_id = pk;
                var followText = '';
                var followBtnHtml = '';
                if(follow_status === true){

                    followText="Following"
                    followBtnHtml = '<div class="btn-follow">'+followText+'</div>';
                    
                }else if(follow_status === false){

                    followText = "Follow";
                    followBtnHtml = '<div class="btn-follow">'+followText+'</div>';

                }else if(follow_status === 2){

                    followBtnHtml = '<div class="btn-default"></div>';
                }
                $(".btn-follow").text(followText);

                $(".num_of_followers").text(followers);
        
                var whichProfile = pk;
                var authorName = jsons.user.username;
                var profileImage = jsons.user.img.profile_image;
                var coverImage = jsons.user.img.cover_image;
                var profileIntro = jsons.user.intro;

                var balloonHtml = '';

                balloonHtml = '\
                    <div class="arrow_box_1">\
                        <div class="card_background_img profile-image-upload-wrap" style="background-image:url('+coverImage+')">\
                            <div class="card_profile_img_wrap" style="background-image:url('+profileImage+')">\
                            </div>\
                        </div>\
                        <div class="wrap-followers">\
                            <div class="followers">\
                                Followers\
                            </div>\
                            <div class="num_of_followers">\
                                '+followers+'\
                            </div>\
                        </div>\
                        '+followBtnHtml+'\
                        <div class="card_profile_name">\
                            '+authorName+'\
                        </div>\
                        <div class="card_profile_title">\
                            \
                        </div>\
                        <div class="socialbar">\
                            <a><i class="iconbtn-facebook"></i></a>\
                            <a><i class="iconbtn-twitter-bird"></i></a>\
                            <a><i class="iconbtn-instagram-filled"></i></a>\
                            <a><i class="iconbtn-globe"></i></a>\
                            <a><i class="iconbtn-info-circled-alt more-info"></i></a>\
                        </div>\
                    </div>\
                    <div class="arrow_box_2">\
                        <div class="card_profile_info">\
                            '+profileIntro+'\
                        </div>\
                        <div class="socialbar">\
                            <a><i class="iconbtn-facebook"></i></a>\
                            <a><i class="iconbtn-twitter-bird"></i></a>\
                            <a><i class="iconbtn-instagram-filled"></i></a>\
                            <a><i class="iconbtn-globe"></i></a>\
                            <a><i class="iconbtn-info-circled-alt more-info2"></i></a>\
                        </div>\
                    </div>\
                ';
                $(e.target).siblings('.flip').html(balloonHtml);
                
                $(".more-info").click(function(){
                    
                    $( ".arrow_box_1" ).hide();
                    $( ".arrow_box_2" ).show();
                });
        
                $(".more-info2").click(function(){
        
                    $( ".arrow_box_2" ).hide();
                    $( ".arrow_box_1" ).show();
                });

                var XY = $(e.target).offset();

                $(document).mousemove(function(pointerCoord){
                    var x = pointerCoord.pageX;     // 마우스 좌표
                    var y = pointerCoord.pageY;

                    //마우스가 일정 좌표를 벗어나면 말풍선이 사라진다.
                    if(x > XY.left + 190 || x < XY.left - 130 || y > XY.top + 80 || y < XY.top - 330) {
        
                        $(".arrow_box_1").detach();
                        $(".arrow_box_2").detach();
                        XY = '';
                    }
                });
        
                $(".btn-follow").unbind("click").click(function(e){
                    follow(author_id);
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
}
/* follow / unfollow */
function follow(author_id) {

    $.ajax({
        url: "/api/member/"+author_id+"/follow/",
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            if(json.author.follow_status){
                
                $(".btn-follow").text("Following");
                $(".num_of_followers").text($(".num_of_followers").text()*1+1);
            }else{

                $(".btn-follow").text("Follow");
                $(".num_of_followers").text() >= 1 ? $(".num_of_followers").text($(".num_of_followers").text()*1-1) : 0;
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}