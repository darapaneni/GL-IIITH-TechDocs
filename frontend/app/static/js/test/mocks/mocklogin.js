
import { isEqualObjects,baseApiUrl } from "../helpers.js";
export {mockhandlers};
var loginApiUrl = baseApiUrl + "signin";
var successfulAuthToken = "ewogICJhbGciOiAiSFMyNTYiLAogICJ0eXAiOiAiSldUIgp9.ewogICJFbWFpbCI6ICJhZG1pbkB0ZWNoZG9jcy5jb20iLAogICJsb2dpblR5cGUiOiAiZW1haWwiLAogICJpc0FkbWluIjogMQp9"
var successfulLoginRequest = { 
    loginType:"email",
    email:'admin@techdocs.com', 
    password : 'admin123',
    rememberMe : 1
}

var successfulLoginRequestGoogle = { 
  loginType:"google",
  email:'sarith.madhu@gmail.com', 
  password : 'authenticated',
  rememberMe : 0
}

var loginResponseSuccess = {
    
    userAuthToken: successfulAuthToken,
    isAdmin:true
    
}
var loginResponseFailure = {

    message:"MOCK : Invalid userid or password"
}
var mockLoginSuccess={
    url: loginApiUrl,
    data: function( data ) {
        return isEqualObjects( data, successfulLoginRequest ) || isEqualObjects( data, successfulLoginRequestGoogle );
      },
    status:200,
    responseText:loginResponseSuccess
  };

  var mockLoginFailure={
    url: loginApiUrl,
    data: function( data ) {
        return !(isEqualObjects( data, successfulLoginRequest ) || isEqualObjects( data, successfulLoginRequestGoogle ));
      },
    status:401,
    responseText:loginResponseFailure
  };
  
  var mockhandlers=
    [mockLoginSuccess,
     mockLoginFailure
    ];
  
