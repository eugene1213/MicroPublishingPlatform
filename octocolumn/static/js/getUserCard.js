function getUserCard(){

    var count = 0;
    
    if($(".flip").length != 0){

        count = $(".flip").length;
    }
    $.ajax({
        url: "/api/member/getUserCard/" + count,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(jsons) {
            
            console.log(jsons);
            for( json in jsons) {

                var cover_img = json.cover_img;
                var profile_img = json.profile_img;
                var nickname = json.nickname;
                var followers = json.followers;
                var intro = json.intro;

                var str =  '<div class="flip"> \n\
                                <div class="arrow_box_1"> \n\
                                    <div class="card_background_img" style="background-image:url('+ cover_img +')"> \n\
                                        <img class="card_profile_img" src="'+ profile_img +'"> \n\
                                    </div> \n\
                                    <div class="wrap-followers"> \n\
                                        <div class="followers"> \n\
                                            Followers \n\
                                        </div> \n\
                                        <div class="num_of_followers"> \n\
                                            '+ followers +'K \n\
                                        </div> \n\
                                    </div> \n\
                                    <div class="btn-follow"> \n\
                                        Follow \n\
                                    </div> \n\
                                    <div class="card_profile_name"> \n\
                                        '+ nickname +' \n\
                                    </div> \n\
                                    <div class="card_profile_title"> \n\
                                        <!--정치전문가--> \n\
                                    </div> \n\
                                    <div class="socialbar"> \n\
                                        <a><img src="{% static \'images/icons/balloon/fb-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/isn-combined-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/t-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/bl-combined-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/inf-combined-shape-copy-2@3x.png\' %}" class="more-info"></a> \n\
                                    </div> \n\
                                </div> \n\
                                <div class="arrow_box_2"> \n\
                                    <div class="card_profile_info"> \n\
                                        '+ intro +' \n\
                                    </div> \n\
                                    <div class="socialbar"> \n\
                                        <a><img src="{% static \'images/icons/balloon/fb-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/isn-combined-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/t-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/bl-combined-shape-copy-2@3x.png\' %}"></a> \n\
                                        <a><img src="{% static \'images/icons/balloon/inf-combined-shape-copy-2@3x.png\' %}" class="more-info2"></a> \n\
                                    </div> \n\
                                </div> \n\
                            </div>'
                $(".profile-relationship").append(str);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });

    $(".more-info").click(function(){
        
        $( ".arrow_box_1" ).hide();
        $( ".arrow_box_2" ).show();
    });

    $(".more-info2").click(function(){

        $( ".arrow_box_2" ).hide();
        $( ".arrow_box_1" ).show();
    });
}