function saveUserAuthToken(userToken)
{
	try {
		localStorage.setItem('userAuthToken',userToken);
		return true;
	    }
	catch
		{
			return false;
		}
}

function getUserAuthToken()
{
	var authToken="";
	try {
		authToken = localStorage.getItem('userAuthToken');
		
	    }
	catch
		{
			authToken = "Not Supported";
		}
	return authToken;
}
function deleteUserAuthToken()
{
	try {
		localStorage.removeItem('userAuthToken');
		return true;
	    }
	catch
		{
			return false;
		}
}