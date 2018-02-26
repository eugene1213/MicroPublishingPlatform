$(document).ready(function(){

    $.ajax({
        url: "http://127.0.0.1:8000/api/column/postList/",
        async: false,
        type: 'GET',
        dataType: 'json',
        headers: {
            'Authorization' : 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImV1Z2VuZTJAb2N0b2NvbHVtbi5jb20iLCJleHAiOjE1MjAyMjUyMzcsIm9yaWdfaWF0IjoxNTE5NjIwNDM3fQ.dB-EHzQg3h1CyyTDIJPkyrn0ydNgdACvbQJvYxYxENk'
        },
        success: function(json) {

            var content = json[0].post.main_content.trim();                            // 전체 글자수
            var countSpace = ((content.match(/\s/g) || []).length)/2;       // 띄어쓰기를 0.5글자 계산
            var sum = content.length - 3.5 - countSpace;                    // 전체 글자수에서 띄어쓰기 갯수*0.5 뺀 값
            var time = Math.round(sum / 500);                               // 1분/500자 반올림

            console.log(json);
            $(".fb1_txt_1").text(json[0].post.title);
            $(".fb1_txt_2").text(json[0].post.main_content.substr(0,100));
            $(".profile_name").text(json[0].post.author.username);
            $(".profile_readtime").text(time+" min read");
            
            //$(".profile_date").text(json[0].post.created_date);
            
            $(".fb1_img").css("background","url("+json[0].post.cover_img+")");
            console.log("통신성공");
        },
        error: function(error) {
            console.log(error);
        }
    });
});