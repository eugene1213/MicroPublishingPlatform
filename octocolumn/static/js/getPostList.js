$(document).ready(function(){


});

function getData(){

    var data = {};
    $.ajax({
        url: "/api/column/postList/",
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            console.log(json);

            data = json;
            
            for(var i=1; i<=json.length; i++){
                var readTime = Math.round(json[i-1].post.typo_count / 500);                               // 1분/500자 반올림

                $("#card_"+i+" .fb1_img").attr("id", json[i-1].post.post_id);
                $("#card_"+i+" .fb1_txt_1").attr("id", json[i-1].post.post_id);
                $("#card_"+i+" .fb1_txt_2").attr("id", json[i-1].post.post_id);
                $("#card_"+i+" .profile_mark > div").attr("id", "bookmark_"+json[i-1].post.post_id);

                // $("#card_"+i+" .fb1_img > img").attr("src",json[i-1].post.cover_img);
                $("#card_"+i+" .fb1_img").css("background","url("+json[i-1].post.cover_img+")");        // 커버사진
                $("#card_"+i+" .fb1_txt_1").text(json[i-1].post.title);                                 // 제목
                $("#card_"+i+" .fb1_txt_2").text(json[i-1].post.main_content.substr(0,100));            // 내용
                $("#card_"+i+" .profile_date").text(json[i-1].post.created_date);                       // 작성일

                $("#card_"+i+" .profile_name").text(json[i-1].post.author.username);                    // 작가이름
                $("#card_"+i+" .profile_readtime").text(readTime+" min read");                          // read time
                $("#card_"+i+" .profile_img > img").attr("src",json[i-1].post.author.img.profile_image);                          // read time

                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가

                json[i-1].post.bookmark_status ? $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark") : $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark-empty");
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
    return data;
}