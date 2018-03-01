$(document).ready(function(){

    
    popBalloon(getData());
});

function getData(){

    var data = {};
    $.ajax({
        url: "/api/column/postList/",
        async: false,
        type: 'GET',
        dataType: 'json',
        // headers: {
        //     'Authorization' : 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImV1Z2VuZTJAb2N0b2NvbHVtbi5jb20iLCJleHAiOjE1MjAyMjUyMzcsIm9yaWdfaWF0IjoxNTE5NjIwNDM3fQ.dB-EHzQg3h1CyyTDIJPkyrn0ydNgdACvbQJvYxYxENk'
        // },
        success: function(json) {

            console.log(json);

            data = json;
            
            for(var i=1; i<=json.length; i++){
                var readTime = Math.round(json[i-1].post.typo_count / 500);                               // 1분/500자 반올림
                
                $("#card_"+i+" .fb1_img").css("background","url("+json[i-1].post.cover_img+")");        // 커버사진
                $("#card_"+i+" .fb1_txt_1").text(json[i-1].post.title);                                 // 제목
                $("#card_"+i+" .fb1_txt_2").text(json[i-1].post.main_content.substr(0,100));            // 내용
                $("#card_"+i+" .profile_date").text(json[i-1].post.created_date);                       // 작성일

                $("#card_"+i+" .profile_name").text(json[i-1].post.author.username);                    // 작가이름
                $("#card_"+i+" .profile_readtime").text(readTime+" min read");                          // read time
                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가 
                
            }
            console.log("통신성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
    return data;
}