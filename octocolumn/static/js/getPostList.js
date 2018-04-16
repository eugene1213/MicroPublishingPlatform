$(document).ready(function(){


});

function getData(){

    var data = {};
    $.ajax({
        url: "/api/column/postList/",
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {

            console.log(jsons);

            post = jsons.results;
            data = post;

            for(var i=1; i<=post.length; i++){
                var readTime = Math.round(post[i-1].typo_count / 500);                               // 1분/500자 반올림

                $("#card_"+i+" .fb1_img").attr("id", post[i-1].pk);
                $("#card_"+i+" .fb1_txt_1").attr("id", post[i-1].pk);
                $("#card_"+i+" .fb1_txt_2").attr("id", post[i-1].pk);
                $("#card_"+i+" .profile_img").attr("id", "author_"+post[i-1].author.author_id);
                $("#card_"+i+" .profile_mark > div").attr("id", "bookmark_"+post[i-1].pk);

                // $("#card_"+i+" .fb1_img > img").attr("src",json[i-1].post.cover_img);
                $("#card_"+i+" .fb1_img").css("background","url("+post[i-1].cover_image+")");        // 커버사진
                $("#card_"+i+" .fb1_txt_1").text(post[i-1].title);                                 // 제목
                $("#card_"+i+" .fb1_txt_2").text(post[i-1].main_content.substr(0,100));            // 내용
                $("#card_"+i+" .profile_date").text(post[i-1].created_date);                       // 작성일

                $("#card_"+i+" .profile_name").text(post[i-1].author.username);                    // 작가이름
                $("#card_"+i+" .profile_readtime").text(readTime+" min read");                          // read time
                $("#card_"+i+" .profile_img").css("background-image","url("+post[i-1].author.img.profile_image+")");                          // read time

                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가

                post[i-1].bookmark_status ? $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark") : $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark-empty");
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
    return data;
}