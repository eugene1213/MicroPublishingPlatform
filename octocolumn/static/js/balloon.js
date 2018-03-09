//프로필 사진에 마우스 오버하면 비어있는 풍선에 내용이 추가됨(ajax사용)과 동시에 프로필 사진 위에 나타남.

function controllBalloonCoord(id){
    //마우스 오버된 사진의 좌표를 구해서 풍선 위치를 잡아준다.

    var coord = $("#"+id).offset();

    $(".arrow_box_1").css("left", coord.left-112);
    $(".arrow_box_2").css("left", coord.left-112);
    $(".arrow_box_1").css("top",  coord.top -300);
    $(".arrow_box_2").css("top",  coord.top -300);

    return XY = coord;
}

//마우스 오버되면 풍선을 노출시키고 마우스가 일정 영역 밖으로 이동하면 사라진다.
$(document).ready(function(){
    
});

function popBalloon(data) {

    $(".profile_img").mouseenter(function(){

        var parents_id = $(this).parents().parents().parents().attr("id");  //mouseenter 이벤트가 발생한 요소의 3번째 부모의 id
        var i = parents_id.substr(5,1);
        var followers = data[i-1].post.author.follower_count;

        $(".num_of_followers").text(followers);

        if(!$(this).attr("id")){
            var ranId = Math.ceil(Math.random()*99999999);
            $(this).attr("id",ranId);
        }
        var whichProfile = $(this).attr('id');
        var authorName = $("#" + whichProfile + "+ .profile_name").text();
        $(".card_profile_name").text(authorName);
        
        controllBalloonCoord(whichProfile);

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

        $(".btn-follow").click(function(){

            follow();
        });
    });
}
/* follow / unfollow */
function follow(author_id) {

    $.ajax({
        url: "/api/member/follow/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            user_id: author_id
        },
        success: function(json) {

            json.author.follow_status ? $(".btn-follow").text("Unfollow") : $(".btn-follow").text("Follow");
            
            $(".num_of_followers").text(json.author.follower_count);
        },
        error: function(error) {
            console.log(error);
        }
    });
}