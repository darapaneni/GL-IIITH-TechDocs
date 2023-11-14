
import { isEqualObjects, baseApiUrl } from "../helpers.js";
export { mockhandlers };
var resetPasswordApiUrl = baseApiUrl + "reset-password";
var successfulResetPasswordRequest = {
  token: '123456',
  new_password:'Strong#123'
}
//200 
var successfulResetPasswordResponse = {
  message: "Successfully Reset"
}
//401
var FailureResetPasswordResponse = {
  message: "Could not Change Password"
}

var mockResetPasswordSuccess = {
  url: resetPasswordApiUrl,
  data: function (data) {
    return isEqualObjects(data, successfulResetPasswordRequest);
  },
  status: 200,
  responseText: successfulResetPasswordResponse
};

var mockResetPasswordFailure = {
  url: resetPasswordApiUrl,
  data: function (data) {
    return !(isEqualObjects(data, successfulResetPasswordRequest));
  },
  status: 401,
  responseText: FailureResetPasswordResponse
};

var mockhandlers =
  [mockResetPasswordSuccess,
    mockResetPasswordFailure

  ];

