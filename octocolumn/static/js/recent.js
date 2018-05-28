$(document).ready(function(){

    var opts = {
        lines: 12               // The number of lines to draw
        , length: 7             // The length of each line
        , width: 5              // The line thickness
        , radius: 10            // The radius of the inner circle
        , scale: 1.0            // Scales overall size of the spinner
        , corners: 1            // Roundness (0..1)
        , color: '#ffffff'      // #rgb or #rrggbb
        , opacity: 1/4          // Opacity of the lines
        , rotate: 0             // Rotation offset
        , direction: 1          // 1: clockwise, -1: counterclockwise
        , speed: 1              // Rounds per second
        , trail: 100            // Afterglow percentage
        , fps: 20               // Frames per second when using setTimeout()
        , zIndex: 2e9           // Use a high z-index by default
        , className: 'spinner'  // CSS class to assign to the element
        , top: '105%'           // center vertically
        , left: '50%'           // center horizontally
        , shadow: false         // Whether to render a shadow
        , hwaccel: false        // Whether to use hardware acceleration (might be buggy)
        , position: 'absolute'  // Element positioning
        }
    var target = document.getElementById('container');
    var spinner = new Spinner(opts).spin(target);

    var currentUrl = window.location.href;
    var requestType = currentUrl.split('/');
        requestType = requestType[requestType.length-2];
    var requestUrl = '';

    switch( requestType ){

        case 'recent': requestUrl = '/api/column/postRecentMore/';
            $('.sub-content-title').text('All Latest Updated Posts');
            break;
        case 'bookmark': requestUrl = '/api/column/bookmarkList/';
            $('.sub-content-title').text('All Your Bookmarked Posts');        
            break;
        case 'buyList': requestUrl = '/api/column/buyList/';
            $('.sub-content-title').text('All Your Purchased Posts');
            break;
        case 'feed': requestUrl = '/api/column/postRecentMore/';
            $('.sub-content-title').text('All Your followers posts');
    }
    getRecent(requestUrl);
    popBalloon();

    $(document).click(function(e){
        
        var post_id = e.target.getAttribute("id");
        var readtime = $('#readtime'+post_id).text();        

        if(post_id > 0){

            isBought(post_id, readtime);
        }
    });

    $(".bookmark").click(function(e){
        
        var bookmark_id = $(e.target).attr("id").replace("bookmark_",'');
        bookmark(bookmark_id);
    });
    $('.image-loader').imageloader({
        background: true,
        callback: function (elm) {
            $(elm).fadeIn();
        }
    });
});
$(function(){
    $('.container').delegate('.bookmark>span','click',function(e){

        var bookmark_id = $(e.target).closest('.bookmark').attr("id").replace("bookmark_",'');        
        bookmark(bookmark_id);
    });
});

function getRecent(url){

    $.ajax({
        beforeSend: function() {
            if(localStorage.getItem('loading') && localStorage.getItem('loading') == true){
                return false;
            }else localStorage.setItem('loading',true);
        },
        url: url,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {

            var posts = jsons.results;
            
            console.log(jsons)
            var next = jsons.next;

            var postsHtml = '';
            var postHtml = '';
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
                            <div class="user full-right">\
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
            $('.blog-posts').append(postsHtml);
            if(next==null) {
                $(window).off('scroll');
                return $('.spinner').remove();   
            }

            $(window).unbind('scroll touchmove').on('scroll touchmove',function() { 
                if ($(window).scrollTop() == $(document).height() - window.innerHeight) {
                    if(next!=null) getRecent(next);
                } 
            });
        },
        error: function(error) {
            console.log(error);
        },
        complete: function() {
            localStorage.setItem('loading',false);
        }
    });
}