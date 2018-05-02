function getUserCard(followDirection){
    //followDirection => 'Following' or 'Follower'

    var count = 0;
    
    
    if($(".flip").length != 0){

        count = $(".flip").length;
    }
    $.ajax({
        beforeSend: function(){
            if(count==$('#'+followDirection).text()*1) return $(window).unbind('scroll');            
        },
        url: "/api/member/getUser" + followDirection + "Card/" + count,
        async: true,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {
            console.log(jsons);
            
            for(json in jsons) {

                var cover_img = jsons[json].cover_img;
                var profile_img = jsons[json].profile_img;
                var nickname = jsons[json].nickname;
                var followers = jsons[json].follower;
                var intro = jsons[json].intro;
                var pk = jsons[json].pk;

                if(followDirection == 'Follower') {
                    
                    var follow_status = jsons[json].follow_status;
                    var status = 'Follow';
                    
                    if(follow_status) status += 'ing';
                }else var status = 'Following';

                var str =  '<div class="flip"> \
                                <div class="arrow_box_1"> \
                                    <div class="card_background_img" style="background-image:url('+ cover_img +')"> \
                                        <img class="card_profile_img" src="'+ profile_img +'"> \
                                    </div> \
                                    <div class="wrap-followers"> \
                                        <div class="followers"> \
                                            Followers \
                                        </div> \
                                        <div class="num_of_followers"> \
                                            '+ followers +' \
                                        </div> \
                                    </div> \
                                    <div class="btn-follow" id="'+pk+'"> \
                                        '+ status + ' \
                                    </div> \
                                    <div class="card_profile_name"> \
                                        '+ nickname +' \
                                    </div> \
                                    <div class="card_profile_title"> \
                                    </div> \
                                    <div class="socialbar">\
                                        <a><i class="iconbtn-facebook"></i></a>\
                                        <a><i class="iconbtn-twitter-bird"></i></a>\
                                        <a><i class="iconbtn-instagram-filled"></i></a>\
                                        <a><i class="iconbtn-globe"></i></a>\
                                        <a><i class="iconbtn-info-circled-alt more-info"></i></a>\
                                    </div>\
                                </div> \
                                <div class="arrow_box_2"> \
                                    <div class="card_profile_info"> \
                                        '+ intro +' \
                                    </div> \
                                    <div class="socialbar">\
                                        <a><i class="iconbtn-facebook"></i></a>\
                                        <a><i class="iconbtn-twitter-bird"></i></a>\
                                        <a><i class="iconbtn-instagram-filled"></i></a>\
                                        <a><i class="iconbtn-globe"></i></a>\
                                        <a><i class="iconbtn-info-circled-alt more-info2"></i></a>\
                                    </div>\
                                </div> \
                            </div>';
                $(".profile-relationship").append(str);
                $(window).scroll(function() { 
                    if ($(window).scrollTop() == $(document).height() - $(window).height()) {
                        if($('#'+followDirection).text()*1 != count) getUserCard(followDirection);
                    } 
                });
            }
            if(followDirection=='Follower') {
                $('.tab:contains(Follower)').addClass('zoom');
                $('.tab:contains(Following)').removeClass('zoom');
            }else{
                $('.tab:contains(Following)').addClass('zoom');
                $('.tab:contains(Follower)').removeClass('zoom');
            }
        },
        error: function(error) {
            console.log(error);
        }
    });

    $(".profile-relationship").delegate('.more-info', 'click', function(e){

        $(e.target).closest('.arrow_box_1').hide();
        $(e.target).closest('.arrow_box_1').siblings(".arrow_box_2").show();
    });

    $(".profile-relationship").delegate('.more-info2', 'click', function(e){

        $(e.target).closest('.arrow_box_2').hide();
        $(e.target).closest('.arrow_box_2').siblings(".arrow_box_1").show();
    });
}