
$(document).ready(function() {

    console.log("ready")

    validatePassFormsAndAddHandlers();

    $('#register-form').on('submit', function(event) {
        console.log("register");
        event.preventDefault();
        if ($('#register-form').valid()) {
            if ($('#password-input').val() != $('#password_confirm-input').val()) {
              showAlert('#register-errorMessage', 'alert-danger', "Error:","Password and confirm password should match!!");
              $('#register').prop('disabled', false);
              return;
           }
           $('#register').prop('disabled', true);
           registerButtonClicked(); 
        } else {
            return;
        }
     });
});


function registerButtonClicked() {
    registerFormData = {
        "loginType" : "email",
        "FirstName" : $('#firstname-input').val(),
        "LastName" : $('#lastname-input').val(),
        "email" : $('#email-input').val(),
        "password" : $('#password_input').val()
    };
    console.log(JSON.stringify(registerFormData))
    callLoginApi(registerFormData);
}

function callLoginApi(registerFormData) {
    removeAlert('#register-errorMessage');
    try {
    $.ajax({
           data : JSON.stringify(registerFormData),
           contentType:"application/json; charset=utf-8",
           type : 'POST',
           dataType: "json",
           url : getApiUrl('register'),
           success: function(data) {
            //In case of success the data contains the JSON
            
            console.log("Registered successfully!!")
            showAlert('#register-infoMessage', 'alert-success', "", "Your are registered successfully!!");
            $('#register').prop('disabled', false);

          },
          error:function(data) {
            // in case of error we need to read response from data.responseJSON
            showAlert('#register-errorMessage', 'alert-danger', "Register!!", getResponseMessage(data));
            $('#register').prop('disabled', false);
          }
        });
    } catch(e) {
        console.log(e)
    }
}

var googleLoginButtonOptions=
{ 
  theme: 'filled_blue', 
  size: 'large',
  width:380
};

function handleGoogleAuthResponse(token) {
    var response = parseJwt(token.credential);
    console.log(response); 
    registerFormData = {
        loginType : "google",
        email : response.email,
        password: "authenticated",
        rememberMe : 0
            };
    callLoginApi(registerFormData);
    
  }

  window.onload = function () {
    google.accounts.id.initialize({
      client_id: getClientId(),
      callback: handleGoogleAuthResponse,
      prompt_parent_id:"googleLogin"
    });
   
    google.accounts.id.renderButton($('#googleLogin')[0],googleLoginButtonOptions);
    
  };



var passwordFormRules =
{
    'password_input': {
        required: true,
        strong_password: true,
        minlength: 6
    },
    'password_confirm': {
        required: true,
        equalTo: "#password_input"
    }
};

var passwordFormMessages =
{
    'password-input': {
        required: "Cannot be blank",
        minlength: "Need at least 6 characters"
    },
    'password_confirm-input': {
        required: "Confirm your password",
        equalTo: "Should be same as above"
    },

};

function validatePassFormsAndAddHandlers() {

    $("#register-form").validate({
        rules: passwordFormRules,
        errorClass: "inputValidationError",
        errorPlacement: function (error, element) {
            element.next("label").after(error);
        },
        submitHandler: function (form) {
           
        },
        messages: passwordFormMessages
    });

}
