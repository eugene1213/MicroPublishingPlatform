
function signup_api(){

    var lastName = $("#lastName").val().trim();
    var firstName = $("#firstName").val().trim();
    var email = $("#email").val().trim();
    var password1 = $("#password1").val().trim();
    var password2 = $("#password2").val().trim();

    console.log(lastName);
    console.log(firstName);
    console.log(email);
    console.log(password1);
    console.log(password2);

    $.ajax({
        url: "http://127.0.0.1:8000/api/member/signup/",
        async: false,
        type: 'POST',
        dataType: 'json',
        data: {
            last_name: lastName,
            first_name: firstName,
            username : email,
            password1 : password1,
            password2 : password2
        },
        success: function(json) {
            console.log("통신성공");
            check_email();
        },
        error: function(error) {
            console.log(error);
        }
    });
}