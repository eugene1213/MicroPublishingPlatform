function get_my_posts(){    //프로필 페이지에서 자신이 쓴 글들을 보여준다.

    $.ajax({
        url: "/api/member/getMyPost/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            join_date = json.join_date;
            posts = json.post;
            posts_num = json.post.length;

            /* 오른쪽에 배치 될 태그 */
            date_div_right_1 = "<div class=\"history_date2\"><span>";                               // 작성일 왼쪽 태그
            date_div_right_2 = "</span><div class=\"date_box\" onclick=\"window.location.href=\'\/read\/";                         // 작성일 오른쪽 태그 + 이미지 소스 왼쪽 태그
            date_div_right_3 = "\'\"><div class=\"date_img\"><img src=\""
            date_div_right_4 = "\" alt=\"\"></div><span>";                                          // 이미지 소스 오른쪽 태그 + 타이틀 왼쪽 태그
            date_div_right_5 = "</span></div><div class=\"bordertip_left\"></div></div>";           // 타이틀 오른쪽 태그
            /* 왼쪽에 배치 될 태그 */
            date_div_left_1 = "<div class=\"history_date3\"><span>";
            date_div_left_2 = "</span><div class=\"date_box\" onclick=\"window.location.href=\'\/read\/";
            date_div_left_3 = "\'\"><div class=\"date_img\"><img src=\"";
            date_div_left_4 = "\" alt=\"\"></div><span>";
            date_div_left_5 = "</span></div><div class=\"bordertip_right\"></div></div>";

            join_date = join_date.split("T")[0];
            join_date = join_date.split("-")[1] + "." + join_date.split("-")[2];

            $(".history_date1 > span").text(join_date);
            var n = 0;
            for( post in posts ) {

                if( n%2 == 0 ) {

                    var created_date = posts[post].created_date.split("T")[0];          // 날짜 데이터 문자열 처리
                        created_date = created_date.split("-")[1] + "." + created_date.split("-")[2];
                    var tag = date_div_right_1 + created_date + date_div_right_2 + posts[post].pk + date_div_right_3 + posts[post].cover_image + date_div_right_4 + posts[post].title + date_div_right_5;
                    
                    $(".history_bar").append( tag );

                } else {

                    var created_date = posts[post].created_date.split("T")[0];
                        created_date = created_date.split("-")[1] + "." + created_date.split("-")[2];
                    var tag = date_div_left_1 + created_date + date_div_left_2 + posts[post].pk + date_div_right_3 + posts[post].cover_image + date_div_left_4 + posts[post].title + date_div_left_5;
                    
                    $(".history_bar").append( tag );
                }                                   // 짝수번째에 오른쪽에 넣고 홀수번째에 왼쪽에 넣는다.

                n++;
            }
            historyBarHeight();
        },
        error: function(error) {
            console.log(error);
        }
    });
}