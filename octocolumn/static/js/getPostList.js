function getData(){
    
    $.ajax({
        beforeSend: function(){
            var opts = {
                lines: 12             // The number of lines to draw
              , length: 7             // The length of each line
              , width: 5              // The line thickness
              , radius: 10            // The radius of the inner circle
              , scale: 1.0            // Scales overall size of the spinner
              , corners: 1            // Roundness (0..1)
              , color: '#ffffff'         // #rgb or #rrggbb
              , opacity: 1/4          // Opacity of the lines
              , rotate: 0             // Rotation offset
              , direction: 1          // 1: clockwise, -1: counterclockwise
              , speed: 1              // Rounds per second
              , trail: 100            // Afterglow percentage
              , fps: 20               // Frames per second when using setTimeout()
              , zIndex: 2e9           // Use a high z-index by default
              , className: 'spinner'  // CSS class to assign to the element
              , top: '75%'            // center vertically
              , left: '50%'           // center horizontally
              , shadow: false         // Whether to render a shadow
              , hwaccel: false        // Whether to use hardware acceleration (might be buggy)
              , position: 'absolute'  // Element positioning
              }
              var target = document.getElementById('container');
              var spinner = new Spinner(opts).spin(target);
        },
        url: "/api/column/postList/",
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {

            console.log(jsons);

            posts = jsons.results;

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
                                    <div class="flip"></div>\
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
                if(post==0){
                    postHtml = postHtml.replace('class="post"','class="post featured"');
                    postsHtml += postHtml;
                    postHtml = '';
                }else if(post==1 || post==3){
                    postHtml = rowHtmlOpen + postHtml;
                    postsHtml += postHtml;
                }else if(post==2 || post==4){
                    postHtml = postHtml + rowHtmlClose;
                    postsHtml += postHtml;
                }
            }
            $('.blog-posts').html(postsHtml);
        },
        error: function(error) {
            console.log(error);
        },
        complete: function() {
            $('.spinner').remove();
        }
    });
}