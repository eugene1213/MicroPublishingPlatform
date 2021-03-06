/* url에 파라미터로 리퀘스트한 뒤 데이터를 받아온다. */
function loadTemp() {

    var url         = window.location.href;
    var splitString = url.split("/");
    var temp_id     = splitString[splitString.length-1];
    var data        = {};
    
    $.ajax({
        url: "/api/column/tempView/" + temp_id,
        async: false,
        type: 'GET',
        dataType: 'json',
        success: function(json) {

            data = json;
        },
        error: function(error) {
            console.log(error);
        }
    });
    $.ajax({
        url: "/api/member/userInfo/",
        async: false,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            var nickname = json.user.nickname;
            var profile_image = json.profileImg.profile_image;

            $("#profileImage").css("background-image","url(" + profile_image + ")");
            $(".profile-sub-wrap > .username").text(nickname);

            // $(".profile-img > img").load(function(e){
            //     loadCropImage(".profile-img > img");
            // });
        },
        error: function(error) {
            console.log(error);
        }
    });
    
    if(data != '' && (temp_id == '' || temp_id == '#top')){

        dateTime = data.created_date;
        yyyymmdd = dateTime.split("T")[0].replace(/-/g,".");
        HHMM     = dateTime.split("T")[1].substr(0,5);

        $(".modal-ask-text > span").text(yyyymmdd + " " + HHMM);
        $(".modal-extend-wrap").show();

    }else viewTemp(data);
    
    return data;
}
/* 불러온 데이터를  */
function viewTemp(loadTempReturnData) {                            // 파라미터는 loadTemp의 리턴값

    if(loadTempReturnData != ''){

        $(".title").append(loadTempReturnData.title);
        $(".editable").append(loadTempReturnData.main_content);

        localStorage.setItem("temp_id", loadTempReturnData.id);    // 넘겨 받은 tmp_id를 로컬 저장소에 저장
                                                                
                                                                   /*                                                */
        $(".editable").focus();                                    /* 값이 있을때 페이지 로딩 후 placeholder를 제거하기 위함.  */
        $(".title").focus();                                       /*                                                */
        $(".editable").focus();
    }
}