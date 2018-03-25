$(document).ready(function(){

    var data = getData();
    popBalloon(data);

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        if(post_id > 0){

            var card_id = $("#"+post_id).closest(".feedbox").attr("id").substr(5,1);
            var cover_img = data[card_id-1].post.cover_img;
            var title = data[card_id-1].post.title;
            var date = data[card_id-1].post.created_datetime;
            var author = data[card_id-1].post.author;
            var tag = data[card_id-1].post.tag;
            var price = data[card_id-1].post.price;
            var preview = data[card_id-1].post.preview;
            var readtime = $("#card_" + card_id + " .profile_readtime").text();

            isBought(post_id, cover_img, title, date, author, tag, readtime, price, preview);
            
        }
    });
    $(".profile_mark").click(function(e){
        
        var post_id = $(e.target).closest(".fb1_txt_2").attr("id");

    });
    $(".btn-cancel-wrap").click(function(){
        $(".preview-wrap").hide();
    });
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

                // $("#card_"+i+" .fb1_img > img").attr("src",json[i-1].post.cover_img);
                $("#card_"+i+" .fb1_img").css("background","url("+json[i-1].post.cover_img+")");        // 커버사진
                $("#card_"+i+" .fb1_txt_1").text(json[i-1].post.title);                                 // 제목
                $("#card_"+i+" .fb1_txt_2").text(json[i-1].post.main_content.substr(0,100));            // 내용
                $("#card_"+i+" .profile_date").text(json[i-1].post.created_date);                       // 작성일

                $("#card_"+i+" .profile_name").text(json[i-1].post.author.username);                    // 작가이름
                $("#card_"+i+" .profile_readtime").text(readTime+" min read");                          // read time
                $("#card_"+i+" .profile_img > img").attr("src",json[i-1].post.author.img.profile_image);                          // read time

                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가
                
                $("#profile-image"+1).load(function(e){
                    loadCropImage("#profile-image" + 1);
                });
                $("#profile-image"+2).load(function(e){
                    loadCropImage("#profile-image" + 2);
                });
                $("#profile-image"+3).load(function(e){
                    loadCropImage("#profile-image" + 3);
                });
                $("#profile-image"+4).load(function(e){
                    loadCropImage("#profile-image" + 4);
                });
                $("#profile-image"+5).load(function(e){
                    loadCropImage("#profile-image" + 5);
                });
                $("#profile-image"+6).load(function(e){
                    loadCropImage("#profile-image" + 6);
                });
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
    return data;
}