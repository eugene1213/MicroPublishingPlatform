$(document).ready(function(){


});
function getData(){
    
    $.ajax({
        url: "/api/column/postList/",
        async: false,
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
                var cover_image = posts[post].cover_image;
                var title = posts[post].title;
                var main_content = posts[post].all_status.main_content.substr(0,100);
                var created_date = posts[post].all_status.created_date;
                var date = created_date.split(' ')[1];
                var month = created_date.split(' ')[0];
                var username = posts[post].all_status.username;
                var profile_image = posts[post].all_status.img.profile_image;
                var bookmark_status = posts[post].all_status.bookmark_status;

                postHtml += '\
                    <div class="post">\
                        <div class="image image-loader" id="'+pk+'" style="background-image:url('+cover_image+')">\
                            <div class="time">\
                                <div class="date">'+date+'</div>\
                                <div class="month">'+month+'</div>\
                            </div>\
                        </div>\
                        <div class="content" id="'+pk+'">\
                            <h1>'+title+'</h1>\
                            <p>'+main_content+'</p>\
                            <div class="meta">\
                                <div class="icon-comment">0 Comments</div>\
                                <ul class="tags">\
                                    <li></li>\
                                    <li></li>\
                                </ul>\
                            </div>\
                            <div class="user-container">\
                                <div class="user full-right">\
                                    <div class="user-pic image-loader" id="author_'+author_id+'" style="background-image:url('+profile_image+')"></div>\
                                    <div class="user-info">\
                                        <h1>'+username+'</h1>\
                                        <p class="full-right">'+readTime+' min read</p>\
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

                //$("#card_"+i+" .profile_mark > div").attr("id", "bookmark_"+pk);                      // read time

                //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가

                //bookmark_status ? $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark") : $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark-empty");
            }
            $('.blog-posts').html(postsHtml);
        },
        error: function(error) {
            console.log(error);
        }
    });
}
// function getData(){

//     var data = {};
//     $.ajax({
//         url: "/api/column/postList/",
//         async: false,
//         type: 'GET',
//         dataType: 'json',
//         success: function(jsons) {

//             console.log(jsons);

//             post = jsons.results;
//             data = post;

            
//             for(var i=1; i<=post.length; i++){
//                 var readTime = Math.round(post[i-1].all_status.typo_count / 500);                               // 1분/500자 반올림

//                 var pk = post[i-1].pk;
//                 var author_id = post[i-1].all_status.author_id;
//                 var cover_image = post[i-1].cover_image;
//                 var title = post[i-1].title;
//                 var main_content = post[i-1].all_status.main_content.substr(0,100);
//                 var created_date = post[i-1].all_status.created_date;
//                 var username = post[i-1].all_status.username;
//                 var profile_image = post[i-1].all_status.img.profile_image;
//                 var bookmark_status = post[i-1].all_status.bookmark_status;

//                 $("#card_"+i+" .fb1_img").attr("id", pk);
//                 $("#card_"+i+" .fb1_txt_1").attr("id", pk);
//                 $("#card_"+i+" .fb1_txt_2").attr("id", pk);
//                 $("#card_"+i+" .profile_img").attr("id", "author_"+ author_id);
//                 $("#card_"+i+" .profile_mark > div").attr("id", "bookmark_"+pk);

//                 // $("#card_"+i+" .fb1_img > img").attr("src",json[i-1].post.cover_img);
//                 $("#card_"+i+" .fb1_img").css("background","url("+cover_image+")");        // 커버사진
//                 $("#card_"+i+" .fb1_txt_1").text(title);                                 // 제목
//                 $("#card_"+i+" .fb1_txt_2").text(main_content);            // 내용
//                 $("#card_"+i+" .profile_date").text(created_date);                       // 작성일

//                 $("#card_"+i+" .profile_name").text(username);                    // 작가이름
//                 $("#card_"+i+" .profile_readtime").text(readTime+" min read");                          // read time
//                 $("#card_"+i+" .profile_img").css("background-image","url("+profile_image+")");                          // read time

//                 //$("#card_"+i+" .profile_img").attr("id", "author_" + json[i-1].post.author.author_id);  // 프로필사진에 id 추가

//                 bookmark_status ? $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark") : $("#card_"+i+" .profile_mark > div").attr("class", "icon-bookmark-empty");
//             }
//         },
//         error: function(error) {
//             console.log(error);
//         }
//     });
//     return data;
// }