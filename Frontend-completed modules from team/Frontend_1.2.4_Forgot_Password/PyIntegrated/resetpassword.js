
$(document).ready(function () {
    $('#reset-password').hide();
    validateToken();
    validateFormsAndAddHandlers();

});

function hideLoadingButton() {
    $('#loadingbutton').hide();
}
function showPasswordForm() {
    $('#reset-password').show();
}
function validateToken() {
    try {
        $.ajax({
            data: {
                token: getToken()
            },
            type: 'POST',
            url: getApiUrl('validate-token'),
            success: function (data) {
                hideLoadingButton();
                showPasswordForm();
            },
            error: function (data) {
                // in case of error we need to read response from data.responseJSON
                hideLoadingButton();
                showAlert('#valid-token-errorMessage', 'alert-danger', "Reset Password!!", getResponseMessage(data));
            }
        });
    }
    catch (e) {
        console.log(e)
    }
}
function getToken() {
    var token = "";
    searchParams = new URLSearchParams(window.location.search)
    if (searchParams.has('token'))
        token = searchParams.get('token');
    return token;
}


function forgotpassword() {
    removeAlert('#forgot-password-errorMessage');
    try {
        $.ajax({
            data: {

                email_id: $('#email-input').val()

            },
            type: 'POST',
            url: getApiUrl('forgot-password'),
            success: function (data) {
                //In case of success the data contains the JSON


                showAlert('#forgot-password-errorMessage', 'alert-success', "Forgot Password!!", "Reset email has been sent to your ID");

            },
            error: function (data) {
                // in case of error we need to read response from data.responseJSON
                showAlert('#forgot-password-errorMessage', 'alert-danger', "Forgot Password!!", getResponseMessage(data));
            }
        });
    }
    catch (e) {
        console.log(e)
    }
}

function changePassword() {
    removeAlert('#password-errorMessage');
    try {
        $.ajax({
            data: {
                token: getToken(),
                new_password: $('#new-password').val()

            },
            type: 'POST',
            url: getApiUrl('reset-password'),
            success: function (data) {
                //In case of success the data contains the JSON

                
                    showAlert('#password-errorMessage', 'alert-success', "Reset Password!!", "Successfully changed");
                
            },
            error: function (data) {
                // in case of error we need to read response from data.responseJSON
                showAlert('#password-errorMessage', 'alert-danger', "Reset Password!!", getResponseMessage(data));
            }
        });
    }
    catch (e) {
        console.log(e)
    }
}

var passwordFormRules =
{

    'new-password': {
        required: true,
        strong_password: true,
        minlength: 6
    },
    'confirm-password': {
        required: true,
        equalTo: "#new-password"
    }
};

var passwordFormMessages =
{
    'new-password': {
        required: "Cannot be blank",
        minlength: "Need at least 6 characters"
    },
    'confirm-password': {
        required: "Confirm your new password",
        equalTo: "Should be same as above"
    },

};


function validateFormsAndAddHandlers() {

    $("#reset-password").validate({
        rules: passwordFormRules,
        errorClass: "inputValidationError",
        errorPlacement: function (error, element) {
            element.next("label").after(error);
        },
        submitHandler: function (form) {
            changePassword();
        },
        messages: passwordFormMessages

    });



    $("form").each(function () {
        $(this).validate();
    });

}