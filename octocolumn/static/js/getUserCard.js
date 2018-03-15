function getUserCard(){

    var count = 0;
    
    
    if($(".flip").length != 0){

        count = $(".flip").length;
    }
    console.log(count);
    $.ajax({
        url: "/api/member/getUserCard/" + count,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {
            
            for( json in jsons) {

                var cover_img = jsons[json].cover_img;
                var profile_img = jsons[json].profile_img;
                var nickname = jsons[json].nickname;
                var followers = jsons[json].follower;
                var intro = jsons[json].intro;

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
                                    <div class="btn-follow"> \
                                        Unfollow \
                                    </div> \
                                    <div class="card_profile_name"> \
                                        '+ nickname +' \
                                    </div> \
                                    <div class="card_profile_title"> \
                                    </div> \
                                    <div class="socialbar"> \
                                        <a><img src="/static/images/icons/balloon/fb-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/isn-combined-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/t-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/bl-combined-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/inf-combined-shape-copy-2@3x.png" class="more-info"></a> \
                                    </div> \
                                </div> \
                                <div class="arrow_box_2"> \
                                    <div class="card_profile_info"> \
                                        '+ intro +' \
                                    </div> \
                                    <div class="socialbar"> \
                                        <a><img src="/static/images/icons/balloon/fb-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/isn-combined-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/t-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/bl-combined-shape-copy-2@3x.png"></a> \
                                        <a><img src="/static/images/icons/balloon/inf-combined-shape-copy-2@3x.png" class="more-info2"></a> \
                                    </div> \
                                </div> \
                            </div>';
                $(".profile-relationship").append(str);
                $(".profile-relationship").append(str);
                $(".profile-relationship").append(str);
                $(".profile-relationship").append(str);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });

    $(".more-info").click(function(e){

        $(e.target).parent().parent().parent().hide();
        $(e.target).parent().parent().parent().parent().children(".arrow_box_2").show();
    });

    $(".more-info2").click(function(e){

        $(e.target).parent().parent().parent().hide();
        $(e.target).parent().parent().parent().parent().children(".arrow_box_1").show();
    });
}