function get_my_posts(){    //프로필 페이지에서 자신이 쓴 글들을 보여준다.

    $.ajax({
        url: "/api/member/getMyPost/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            console.log(json);
            join_date = 0//json.join_date;
            posts = json;
            posts_num = json.length;

            /* 오른쪽에 배치 될 태그 */
            date_div_right_1 = "<div class=\"history_date2\"><span>";                               // 작성일 왼쪽 태그
            date_div_right_2 = "</span><div class=\"date_box\"><div class=\"date_img\"><img src=\"";// 작성일 오른쪽 태그 + 이미지 소스 왼쪽 태그
            date_div_right_3 = "\" alt=\"\"></div><span>";                                          // 이미지 소스 오른쪽 태그 + 타이틀 왼쪽 태그
            date_div_right_4 = "</span></div><div class=\"bordertip_left\"></div></div>";           // 타이틀 오른쪽 태그
            /* 왼쪽에 배치 될 태그 */
            date_div_left_1 = "<div class=\"history_date3\"><span>";
            date_div_left_2 = "</span><div class=\"date_box\"><div class=\"date_img\"><img src=\"";
            date_div_left_3 = "\" alt=\"\"></div><span>";
            date_div_left_4 = "</span></div><div class=\"bordertip_right\"></div></div>";

            $(".history_date1 > span").text(join_date);
            var n = 0;
            for( post in posts ) {

                               
                if( n%2 == 0 ) {

                    var tag = date_div_right_1 + post.created_date + date_div_right_2 + post.cover_image + date_div_right_3 + post.title + date_div_right_4;
                    
                    $(".history_bar").append( tag );

                } else {

                    var tag = date_div_left_1 + post.created_date + date_div_left_2 + post.cover_image + date_div_left_3 + post.title + date_div_left_4;
                    
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