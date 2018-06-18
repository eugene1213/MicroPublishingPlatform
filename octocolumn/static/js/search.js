var searchHtml = '\
                    <div id=\'search-container\'>\
                        <div class="search-close"></div>\
                        <div class="search-input">\
                            <input class="input-search" placeholder="Search" type="text">\
                        </div>\
                        <div class="search-result"><div class="search-posts"></div></div>\
                    </div>\
                ';
$(".control").click( function(){
    $(".input-search").focus();
    $(".page").css("position", "fixed"); 
    $(".page").after(searchHtml);
});
$(function(){
    $(document).on('click','.search-close',function(e){
        $(".input-search").val('');
        $("#search-container").detach();
        $(".page").css("position", "static"); 
    });
});
$(function(){    
    $(document).on('keypress',".input-search",function(e){

        if(e.keyCode == 13){
            $(".search-posts").empty();
            $(".search-input").css('top','5%');
            var keyword = $(this).val();
            var url = "/api/column/search/?keyword="+keyword;
            search(url);
        }
    });
});
$(function(){    
    $('#search-container').on('click','.bookmark>i',function(e){
        
        var bookmark_id = $(e.target).closest('.bookmark').attr("id").replace("bookmark_",'');        
        bookmark(bookmark_id,false);
    });
});
function search(url){
        
    $.ajax({
        url: url,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {

            var posts = jsons.results;
            
            console.log(jsons)
            var next = jsons.next;

            var postsHtml = '';
            var rowHtmlOpen = '<div class="row cf">';
            var rowHtmlClose = '</div>';

            for(post in posts){

                var postHtml = '';
                var readTime = Math.round(posts[post].all_status.typo_count / 500);  // 1분/500자 반올림
                var pk = posts[post].pk;
                var author_id = posts[post].all_status.author_id;
                var cover_image = posts[post].thumbnail;
                var title = posts[post].title;
                var price = posts[post].price;                
                var main_content = posts[post].all_status.main_content;
                var created_date = posts[post].all_status.created_date;
                var date = created_date.split(' ')[1];
                var month = created_date.split(' ')[0];
                var username = posts[post].all_status.username;
                var profile_image = posts[post].all_status.img.profile_image;
                var bookmark_status = posts[post].all_status.bookmark_status;
                var bookmarkClass = 'icon-bookmark';

                bookmark_status ? {/*pass*/} : bookmarkClass += '-empty';

                postHtml += '\
                    <div class="post">\
                        <div class="image image-loader" id="'+pk+'" style="background-image:url('+cover_image+')">\
                            <div class="time">\
                                <div class="date">'+date+'</div>\
                                <div class="month">'+month+'</div>\
                            </div>\
                        </div>\
                        <div class="content">\
                            <h1 id="'+pk+'">'+title+'</h1>\
                            <p id="'+pk+'">'+main_content+'</p>\
                            <div class="meta">\
                                <div class="icon-comment">'+price+'P</div>\
                                <ul class="tags">\
                                    <li></li>\
                                    <li></li>\
                                </ul>\
                            </div>\
                            <div class="user-container">\
                                <div class="bookmark" id="bookmark_'+pk+'"><i class="'+bookmarkClass+'"></i></div>\
                                <div class="user full-right" onclick="window.location.href=\'/profile/'+author_id+'\'">\
                                    <div class="user-pic image-loader" id="author_'+author_id+'" style="background-image:url('+profile_image+')"></div>\
                                    <div class="user-info">\
                                        <h1>'+username+'</h1>\
                                        <p class="full-right" id="readtime'+pk+'">'+readTime+' min read</p>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>\
                    </div>\
                ';
                if(post){
                    postHtml = postHtml.replace('class="post"','class="post featured"');
                    postsHtml += postHtml;
                    postHtml = '';
                }
                // $(".main_title").append(str).find("#" + username).load(function(){loadCropImage("#" + username);});

                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가
                
                // $("#" + username).load(function(e){
                //     loadCropImage("#" + username);
                // });
            }
            $('.search-posts').append(postsHtml);
            if(next==null) {
                $('#search-container').off('scroll');
                return $('.spinner').remove();   
            }
            var padding = $(".search-result").css("padding-top").replace('px','')*1+$(".search-result").css("padding-bottom").replace('px','')*1;
            
            $("#search-container").unbind('scroll touchmove').on('scroll touchmove',function() { 
                if ($("#search-container").scrollTop() == $(".search-result").height() - window.innerHeight + padding) {

                    if(next!=null) search(next);
                } 
            });
        },
        error: function(err){
            console.log(err);
        }
    });
}