$(document).ready(function () {
    
    $.validator.addMethod("strong_password", function (value, element) {
        let password = value;
        if (!(/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!^*()@#$%&])(.{6,20}$)/.test(password))) {
            return false;
        }
        return true;
    }, function (value, element) {
        let password = $(element).val();
        if (!(/^(.{6,20}$)/.test(password))) {
            return 'Must be between 6 to 20 characters long.';
        }
        else if (!(/^(?=.*[A-Z])/.test(password))) {
            return 'Must contain at least one uppercase.';
        }
        else if (!(/^(?=.*[a-z])/.test(password))) {
            return 'Must contain at least one lowercase.';
        }
        else if (!(/^(?=.*[0-9])/.test(password))) {
            return 'Must contain at least one digit.';
        }
        else if (!(/^(?=.*[!^*()@#$%&])/.test(password))) {
            return "Must contain special characters from !^*()@#$%&.";
        }
        return false;
    });
});