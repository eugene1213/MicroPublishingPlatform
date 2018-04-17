function invite(email) {
    
    $.ajax({
        url: "/api/member/invite/",
        async: true,
        type: 'POST',
        dataType: 'json',
        data: {email:email},
        success: function(json) {
            
        },
        error: function(error) {
            console.log(error);         
        }
    });
}