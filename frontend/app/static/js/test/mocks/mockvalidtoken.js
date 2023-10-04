
import { isEqualObjects, baseApiUrl } from "../helpers.js";
export { mockhandlers };
var validateTokenApiUrl = baseApiUrl + "validate-token";
var successfulIsValidTokenRequest = {
  token: '123456'
}
//200 
var successfulIsValidTokenResponse = {
  message: "Valid Token"
}
//401
var FailureIsValidTokenResponse = {
  message: "Not a valid link for resetting password"
}

var mockValidTokenSuccess = {
  url: validateTokenApiUrl,
  data: function (data) {
    return isEqualObjects(data, successfulIsValidTokenRequest);
  },
  status: 200,
  responseText: successfulIsValidTokenResponse
};

var mockValidTokenFailure = {
  url: validateTokenApiUrl,
  data: function (data) {
    return !(isEqualObjects(data, successfulIsValidTokenRequest));
  },
  status: 401,
  responseText: FailureIsValidTokenResponse
};

var mockhandlers =
  [mockValidTokenSuccess,
    mockValidTokenFailure

  ];

