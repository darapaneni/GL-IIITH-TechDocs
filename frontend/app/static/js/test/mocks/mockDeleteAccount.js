
import { isEqualObjects,baseApiUrl } from "../helpers.js";
export {mockhandlers};
var deleteAccountAPIUrl = baseApiUrl + "deleteAccount";


var user1DeleteRequest = {
    authToken:'123456',
    currentPassword:"abcdefg"    
}
var user2DeleteRequest = {
  authToken:'789123',
  currentPassword:"abcdefg"    
}


var DeleteFailure = {
    status:false,
    message:"MOCK : Invalid Password"
}

var DeleteSuccess = {
  status:true,
  message:"MOCK : Account Deleted"
}

function checkValidDeleteRequest(data)
{
  return isEqualObjects( data, user1DeleteRequest ) || isEqualObjects( data, user2DeleteRequest );
}
var deleteAccountUser={
    url: deleteAccountAPIUrl,
    data: function( data ) {
        return checkValidDeleteRequest(data);
      },
    status:200,
    responseText:DeleteSuccess
  };



  var deleteAccountUserFailure={
    url: deleteAccountAPIUrl,
    data: function( data ) {
        return !checkValidDeleteRequest(data);
      },
    status:401,
    responseText:DeleteFailure
  };

  
  
  var mockhandlers=[
    deleteAccountUser,
    deleteAccountUserFailure
    
            ];
  
