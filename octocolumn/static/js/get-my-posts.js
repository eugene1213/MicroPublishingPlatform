/* 내 글 탭에서 히스토리바(가운데 선) 높이 지정 */
function historyBarHeight() {
    
    var n = $(".history_date2").length + $(".history_date3").length // 말풍선 갯수
    $(".history_bar").height(n * 120);
}

function get_my_posts(which){    //프로필 페이지에서 자신이 쓴 글들을 보여준다.

    $(".history_date2, .history_date3").remove(); // 초기화

    var url = '';

    if(which == "post"){

        url = "/api/member/getMyPost/";

        var date_div_right_2 = "</span><div class=\"date_box\" onclick=\"window.location.href=\'\/read\/";                         // 작성일 오른쪽 태그 + 이미지 소스 왼쪽 태그
        var date_div_right_3 = "\'\"><div class=\"date_img\"><img src=\"";

        var date_div_left_2 = "</span><div class=\"date_box\" onclick=\"window.location.href=\'\/read\/";
        var date_div_left_3 = "\'\"><div class=\"date_img\"><img src=\"";

    }else if(which == "temp") {

        url = "/api/member/getMyTemp/";

        var date_div_right_2 = "</span><div class=\"date_box\" onclick=\"window.location.href=\'\/write\/";                         // 작성일 오른쪽 태그 + 이미지 소스 왼쪽 태그
        var date_div_right_3 = "\'\"><div class=\"date_img\"><img src=\"";

        var date_div_left_2 = "</span><div class=\"date_box\" onclick=\"window.location.href=\'\/write\/";
        var date_div_left_3 = "\'\"><div class=\"date_img\"><img src=\"";
    }
    $.ajax({
        url: url,
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            if(json != ''){
                var posts = json.post;
                var posts_num = json.post.length;

                /* 오른쪽에 배치 될 태그 */
                var date_div_right_1 = "<div class=\"history_date2\"><span>";                               // 작성일 왼쪽 태그
                var date_div_right_4 = "\" alt=\"\"></div><span>";                                          // 이미지 소스 오른쪽 태그 + 타이틀 왼쪽 태그
                var date_div_right_5 = "</span></div><div class=\"bordertip_left\"></div></div>";           // 타이틀 오른쪽 태그
                /* 왼쪽에 배치 될 태그 */
                var date_div_left_1 = "<div class=\"history_date3\"><span>";
                var date_div_left_4 = "\" alt=\"\"></div><span>";
                var date_div_left_5 = "</span></div><div class=\"bordertip_right\"></div></div>";

                

                if(which == 'post'){
                    var join_date = json.join_date.split("T")[0];
                        join_date = join_date.split("-")[1] + "." + join_date.split("-")[2];

                    $(".history_date1 > span").text(join_date);
                }
                
                var n = 0;
                for( post in posts ) {

                    var created_date = posts[post].created_date.split("T")[0];
                        created_date = created_date.split("-")[1] + "." + created_date.split("-")[2];
                    var pk = posts[post].pk;
                    var title = posts[post].title;

                    if(which == 'post'){
                        cover_image = posts[post].cover_image;
                    } else {
                        cover_image = '';
                    }

                    if( n%2 == 0 ) {

                        var tag = date_div_right_1 + created_date + date_div_right_2 + pk + date_div_right_3 + cover_image + date_div_right_4 + title + date_div_right_5;
                        
                        $(".history_bar").append( tag );

                    } else {

                        var tag = date_div_left_1 + created_date + date_div_left_2 + pk + date_div_right_3 + cover_image + date_div_left_4 + title + date_div_left_5;
                        
                        $(".history_bar").append( tag );
                    }                                   // 짝수번째에 오른쪽에 넣고 홀수번째에 왼쪽에 넣는다.

                    n++;
                }
                historyBarHeight();
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}