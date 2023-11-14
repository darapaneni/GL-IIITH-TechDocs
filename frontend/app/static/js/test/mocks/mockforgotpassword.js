
import { isEqualObjects, baseApiUrl } from "../helpers.js";
export { mockhandlers };
var forgotPasswordApiUrl = baseApiUrl + "forgot-password";
var successfulForgotPasswordRequest = {
  email_id: 'admin@techdocs.com'
}
//200 
var successfulForgotPasswordResponse = {
  message: "Sent a reset pwd link to email ID"
}
//401
var successfulForgotPasswordFailure = {
  message: "User account not found"
}

var mockforgotPasswordSuccess = {
  url: forgotPasswordApiUrl,
  data: function (data) {
    return isEqualObjects(data, successfulForgotPasswordRequest);
  },
  status: 200,
  responseText: successfulForgotPasswordResponse
};

var mockforgotPasswordFailure = {
  url: forgotPasswordApiUrl,
  data: function (data) {
    return !(isEqualObjects(data, successfulForgotPasswordRequest));
  },
  status: 401,
  responseText: successfulForgotPasswordFailure
};

var mockhandlers =
  [mockforgotPasswordSuccess,
    mockforgotPasswordFailure

  ];

