$(document).ready(function() {

    var data = getRecent("/api/column/bookmarkList/");
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

            var readtime = $("#card_" + card_id + " .profile_readtime").text();

            isBought(post_id, cover_img, title, date, author, tag, readtime, price);
            
        }
    });
    $(".btn-cancel-wrap").click(function(){
        $(".preview-wrap").hide();
    });
    $(".profile_mark").click(function(e){
        
        var bookmark_id = $(e.target).attr("id").replace("bookmark_",'');
        bookmark(bookmark_id);
    });
});

function getRecent(url){
    
    var data = {};
    var count = 0;

    if($(".flip").length != 0){

        count = $(".flip").length;
    }

    $.ajax({
        url: url,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            data = json;
            var usernameArray = [];

            console.log(json)
            next = json.next;
            for(var i in json.results){

                var post_id = json.results[i].pk;
                var readTime = Math.round(json.results[i].typo_count / 500);                               // 1분/500자 반올림
                var cover_img = json.results[i].cover_image;
                var title = json.results[i].title;
                var main_content = json.results[i].main_content.substr(0,100);
                var created_date = json.results[i].created_date;
                var username = json.results[i].author.username;
                var profile_image = json.results[i].author.img.profile_image;
                var bookmarkElement = '';
                json.results[i].bookmark_status ? bookmarkElement = '<div id="bookmark_' + post_id + '" class="icon-bookmark"></div>' : bookmarkElement = '<div id="bookmark_' + post_id + '" class="icon-bookmark-empty"></div>';
                
                usernameArray.push(username);
                var str =  '<div class="feedbox4 feedbox" id="card_'+ i +'">              \
                                <div class="fb1_img profile-image-upload-wrap" style="background-image:url(\''+ cover_img +'\')" id="'+ post_id+'"></div>           \
                                <div class="fb1_txt">                   \
                                    <div class="fb1_txt_1" id="'+ post_id+'">             \
                                        '+ title +'                     \
                                    </div>                              \
                                    <div class="fb1_txt_2" id="'+ post_id+'">             \
                                        '+ main_content +'              \
                                    </div>                              \
                                    <div class="profile_box">           \
                                        <div class="profile_img profile-image-upload-wrap"><img id="'+ username +'" src="'+ profile_image +'" alt="프로필 사진"></div>  \
                                        <div class="profile_name">'+ username +'</div>                 \
                                        <div class="profile_date">'+ created_date +'</div>             \
                                        <div class="profile_readtime">'+ readTime +' min read</div>    \
                                        <div class="profile_mark">'+bookmarkElement+'</div>\
                                    </div>                              \
                                </div>                                  \
                            </div>';
                $(".main_title").append(str)
                // $(".main_title").append(str).find("#" + username).load(function(){loadCropImage("#" + username);});

                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가
                
                // $("#" + username).load(function(e){
                //     loadCropImage("#" + username);
                // });
            }
            $(window).scroll(function() { 
                if ($(window).scrollTop() == $(document).height() - $(window).height()) {
                    getRecent(next);
                } 
            });
            // for( i in usernameArray){
            //     console.log("#" + usernameArray[i]);
            //     $("#" + usernameArray[i]).imagesLoaded().then(function(){
            //         loadCropImage("#" + usernameArray[i]);
            //     });
            // }
        },
        error: function(error) {
            console.log(error);
        }
    });
    return data;
}