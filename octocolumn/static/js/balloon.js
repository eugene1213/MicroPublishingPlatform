//프로필 사진에 마우스 오버하면 비어있는 풍선에 내용이 추가됨(ajax사용)과 동시에 프로필 사진 위에 나타남.

function controllBalloonCoord(id){
    //마우스 오버된 사진의 좌표를 구해서 풍선 위치를 잡아준다.

    var coord = $(id).offset();
    console.log(id)

    $(".arrow_box_1").css("left", coord.left-112);
    $(".arrow_box_2").css("left", coord.left-112);
    $(".arrow_box_1").css("top",  coord.top -300);
    $(".arrow_box_2").css("top",  coord.top -300);

    return XY = coord;
}

//마우스 오버되면 풍선을 노출시키고 마우스가 일정 영역 밖으로 이동하면 사라진다.

function popBalloon() { //getPostList.js 에서 호출한다.

    $(".profile_img").mouseenter(function(e){

        var pk = $(this).attr("id").replace('author_','');
        
        $.ajax({
            url: "/api/member/"+ pk +"/followStatus/",
            async: true,
            type: 'GET',
            dataType: 'json',
            success: function(jsons) {
    
                console.log(jsons);
    
                var followers = jsons.follower_count;
                var follow_status = jsons.follow_status;
                var author_id = pk;

                if(follow_status) {
                    $(".btn-follow").text("Following");
                }
                $(".num_of_followers").text(followers);
        
                // if(!$(this).attr("id")){
                //     var ranId = Math.ceil(Math.random()*99999999);
                //     $(this).attr("id",ranId);
                // }
                var whichProfile = $(this).attr('id');
                var authorName = jsons.user.username;
                var profileImage = jsons.user.img.profile_image;
                var coverImage = jsons.user.img.cover_image;
                var profileIntro = jsons.user.intro;

                $(".card_profile_img_wrap").css("background-image","url(" +profileImage+ ")");
                $(".card_background_img").css("background","url(" +coverImage+ ")")
                $(".card_profile_info").text(profileIntro);
                $(".card_profile_name").text(authorName);
                
                controllBalloonCoord(e.target);
        
                $(".arrow_box_1").show();
                
                $(".more-info").click(function(){
                    
                    $( ".arrow_box_1" ).hide();
                    $( ".arrow_box_2" ).show();
                });
        
                $(".more-info2").click(function(){
        
                    $( ".arrow_box_2" ).hide();
                    $( ".arrow_box_1" ).show();
                });
        
                //창 크기가 변화하면 위치 재조정
                $(window).resize(function(){
        
                    controllBalloonCoord(whichProfile);
                });
        
                $(document).mousemove(function(pointerCoord){
                    var x = pointerCoord.pageX;     // 마우스 좌표
                    var y = pointerCoord.pageY;
        
                    //마우스가 일정 좌표를 벗어나면 말풍선이 사라진다.
                    if(x > XY.left + 190 || x < XY.left - 130 || y > XY.top + 80 || y < XY.top - 330) {
        
                        $(".arrow_box_1").hide();
                        $(".arrow_box_2").hide();
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

            console.log(json.author.follow_status);
            json.author.follow_status ? $(".btn-follow").text("Following") : $(".btn-follow").text("Follow");
            
            json.author.follow_status ? $(".num_of_followers").text($(".num_of_followers").text()*1+1) : $(".num_of_followers").text() >= 1 ? $(".num_of_followers").text($(".num_of_followers").text()*1-1) : 0;
        },
        error: function(error) {
            console.log(error);
        }
    });
}