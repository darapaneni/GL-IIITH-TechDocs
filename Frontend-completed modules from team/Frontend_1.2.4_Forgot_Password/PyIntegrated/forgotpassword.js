
$(document).ready(function () {
    validateFormsAndAddHandlers();
   
});




function forgotpassword() {
    removeAlert('#forgot-password-errorMessage');
    try {
        $.ajax({
            data: {
                
                email_id: $('#email-input').val()
                   
                } ,
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

var forgotPasswordFormRules =
{
    'email-login': {
        required: true,
        email:true
    }
};

var  forgotPasswordFormMessages =

{
    'email-login': {
        required: "Enter Valid email address"
    }

};


function validateFormsAndAddHandlers() {

    $("#forgot-password").validate({
        rules: forgotPasswordFormRules,
        errorClass: "inputValidationError",
        errorPlacement: function (error, element) {
            element.next("label").after(error);
        },
        submitHandler: function (form) {
            forgotpassword();
        },
        messages: forgotPasswordFormMessages
    });

    

    $("form").each(function () {
        $(this).validate();
    });

}