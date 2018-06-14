function buyBtnClick(price) {
    //결제요청을 위한 Api, 실제 사용 코드
    var name = '';
    var username = '';
    var email = '';
    var addr = '';
    var phone = '';

    switch(price){
        case 2000: name = 'Tester';break;
        case 5000: name = 'Starter';break;
        case 10000: name = 'Regular';
    }
    $.ajax({
        url: "/api/member/shopUserData/",
        async: true,
        type: 'POST',
        dataType: 'json',
        success: function(json) {

            username = json.detail.username;
            email = json.detail.email;
            addr = json.detail.addr;
            phone = json.detail.phone;

            BootPay.request({
                price: price+price*0.1,               //실제 결제되는 가격
                application_id: '5ab88457b6d49c1aaa550da7',
                name: name,                 //결제창에서 보여질 이름
                pg: 'danal',
                show_agree_window: 0,       // 부트페이 정보 동의 창 보이기 여부
                items: [
                    {
                        item_name: name,            //상품명
                        qty: 1,                     //수량
                        unique: '1',                //해당 상품을 구분짓는 primary key
                        price: price+price*0.1,     //상품 단가
                        cat1: '',                   // 대표 상품의 카테고리 상, 50글자 이내
                        cat2: '',                   // 대표 상품의 카테고리 중, 50글자 이내
                        cat3: '',                   // 대표상품의 카테고리 하, 50글자 이내
                    }
                ],
                user_info: {
                    username: username,
                    email: email,
                    addr: addr,
                    phone: phone
                },
                method: '', //결제수단, 입력하지 않으면 결제수단 선택부터 화면이 시작합니다.
                order_id: '고유order_id_1234', //관리하시는 고유 주문번호를 입력해주세요
                params: {callback1: '그대로 콜백받을 변수 1', callback2: '그대로 콜백받을 변수 2', customvar1234: '변수명도 마음대로'},
            }).error(function (data) {
                //결제 진행시 에러가 발생하면 수행됩니다.
                console.log(data);
            }).cancel(function (data) {
                //결제가 취소되면 수행됩니다.
                console.log(data)
            // }).confirm(function (data) {
            //     //결제가 실행되기 전에 수행되며, 주로 재고를 확인하는 로직이 들어갑니다.
            //     //주의 - 카드 수기결제일 경우 이 부분이 실행되지 않습니다.
            //         $.ajax({
            //             url: "/api/member/payCheck/",
            //             async: true,
            //             type: 'POST',
            //             dataType: 'json',
            //             data: {
            //                 receipt_id: data.receipt_id
            //             },
            //             success: function(json) {
            //                 console.log(json[0])
            //                 BootPay.transactionConfirm(data); // 조건이 맞으면 승인 처리를 한다.
            //                 BootPay.removeWindow(); // 조건이 맞지 않으면 결제 창을 닫고 결제를 승인하지 않는다.
            //             },
            //             error: function(err){
            //             }
            //         });
            }).done(function (data) {
                //결제가 정상적으로 완료되면 수행됩니다
                //비즈니스 로직을 수행하기 전에 결제 유효성 검증을 하시길 추천합니다.
                $.ajax({
                    url: "/api/member/payCheck/",
                    async: true,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        receipt_id: data.receipt_id,
                        price: price,
                    },
                    success: function(json) {
                        window.location.href = "/";
                    },
                    error: function(err){
                    }
                });
            });
        },
        error: function(error) {
            console.log(error)
            var msg = error.responseJSON.content.message
            var title = error.responseJSON.content.title
            error_modal(title, msg, false);
        }
    });
}