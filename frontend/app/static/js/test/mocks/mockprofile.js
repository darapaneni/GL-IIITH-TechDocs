
import { isEqualObjects,baseApiUrl } from "../helpers.js";
export {mockhandlers};
var getProfileAPIUrl = baseApiUrl + "getProfile";
var updateProfileAPIUrl = baseApiUrl + "updateProfile";
var changePasswordAPIUrl = baseApiUrl + "changePassword";
var userProfiles=
{
  'ewogICJhbGciOiAiSFMyNTYiLAogICJ0eXAiOiAiSldUIgp9.ewogICJFbWFpbCI6ICJhZG1pbkB0ZWNoZG9jcy5jb20iLAogICJsb2dpblR5cGUiOiAiZW1haWwiLAogICJpc0FkbWluIjogMQp9':{
    firstName:'Sarith',
    lastName:'Madhu',
    address : {
      streetAddress: "Hyderabad, Tarnaka",
      state:"Telangana",
      country:"IN"},
    occupation: "Researcher",
    purposeOfUse:""
  },
  '789123':
  {
    firstName: 'Tech',
    lastName:'Docs',
    address : {
      streetAddress: "trivandrum",
      state:"Kerala",
      country:"IN"},
    occupation: "Student",
    purposeOfUse:"Student"
  }
};
function writeProfiles(profiles)
{
  localStorage.setItem('userProfiles',JSON.stringify(profiles));
}
if(!(localStorage.getItem('userProfiles')))
{
  writeProfiles(userProfiles);
}
function getProfiles()
{
  return JSON.parse(localStorage.getItem('userProfiles'));
}

function getProfileData(authtoken)
{
  var userData=getProfiles();
  return userData[authtoken];
}
var user1GetRequest = {
    authToken:'ewogICJhbGciOiAiSFMyNTYiLAogICJ0eXAiOiAiSldUIgp9.ewogICJFbWFpbCI6ICJhZG1pbkB0ZWNoZG9jcy5jb20iLAogICJsb2dpblR5cGUiOiAiZW1haWwiLAogICJpc0FkbWluIjogMQp9'    
}
var user2GetRequest = {
  authToken:'789123'    
}


var profileDataFailure = {
    message:"MOCK : Unable to fetch Data"
}

var updateProfileDataFailure = {
  message:"MOCK : Unable to update Data"
}
var changePasswordDataFailure = {
  message:"MOCK : Unable to update Password"
}
function checkValidProfileRequest(data)
{
  return isEqualObjects( data, user1GetRequest ) || isEqualObjects( data, user2GetRequest );
}
var getProfileUser={
    url: getProfileAPIUrl,
    data: function( data ) {
        return checkValidProfileRequest(data);
      },
    status:200,
    response:function(settings)
    {
      var response = {
        userData:getProfileData(settings.data.authToken),
        usageStats:{
          signUpDate:"12/06/2022",
          lastActiveDate:"12/10/2022" 
}        
      };
      this.responseText=response;
    }
  };



  var profileDataFailure={
    url: getProfileAPIUrl,
    data: function( data ) {
        return !checkValidProfileRequest(data);
      },
    status:401,
    responseText:profileDataFailure
  };

  function checkValidUpdateRequest(data)
  {
    if(data.authToken!='ewogICJhbGciOiAiSFMyNTYiLAogICJ0eXAiOiAiSldUIgp9.ewogICJFbWFpbCI6ICJhZG1pbkB0ZWNoZG9jcy5jb20iLAogICJsb2dpblR5cGUiOiAiZW1haWwiLAogICJpc0FkbWluIjogMQp9'&&data.authToken!='789123')
      return false;
    if(data.userData.firstName.length>10) return false;
    updateProfileData(data);
    return true;
  }
  function checkValidChangePasswordRequest(data)
  {
    if(data.authToken!='ewogICJhbGciOiAiSFMyNTYiLAogICJ0eXAiOiAiSldUIgp9.ewogICJFbWFpbCI6ICJhZG1pbkB0ZWNoZG9jcy5jb20iLAogICJsb2dpblR5cGUiOiAiZW1haWwiLAogICJpc0FkbWluIjogMQp9'&&data.authToken!='789123')
      return false;
    if(data.currentPassword.length>10) return false;
    return true;
  }
  function updateProfileData(data)
  {
    var token = data.authToken;
    var userData=getProfiles();
    userData[token]=data.userData;
   
    writeProfiles(userData);

  }
  var updateProfileUser={
    url: updateProfileAPIUrl,
    data: function( data ) {
        return checkValidUpdateRequest(JSON.parse(data));
      },
    status:200,
    response:function(settings)
    {
      
      var response = {
        message:"Profile updated"
      };
      this.responseText=response;
    }
  };

  var updateProfileUserFailure={
    url: updateProfileAPIUrl,
    data: function( data ) {
        return !checkValidUpdateRequest(data);
      },
    status:[402,404,500],
    responseText:updateProfileDataFailure
  };
  var changePassword={
    url: changePasswordAPIUrl,
    data: function( data ) {
        return checkValidChangePasswordRequest(data);
      },
    status:200,
    response:function(settings)
    {
      var response = {
        status:true,
        message:"OK"
    
      };
      this.responseText=response;
    }
  };

  var changePasswordFailure={
    url: changePasswordAPIUrl,
    data: function( data ) {
        return !checkValidChangePasswordRequest(data);
      },
    status:[402,404,500],
    responseText:changePasswordDataFailure
  };
  
  var mockhandlers=[
    getProfileUser,
    profileDataFailure,
    updateProfileUser,
    updateProfileUserFailure,
    changePassword,
    changePasswordFailure
    
            ];
  
