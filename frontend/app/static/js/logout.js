/* This logoutButtonClicked function checks for the userToken in local Storage
   and user in Session Storage. 
   if user in Session Storage it clears Session and 
   if JWT is i local storage it removes it sends JWT to backend for validation
   if it is valid redirects to home page after logout
   if it is invalid or not in local storage, it issues a "bad request" alert and 
   redirects to home page*/


async function clearSession() {

    await fetch(getFrontEndUrl('clearSession'), {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {console.log(data)})
    .then(error => {console.log(error)})
        
    return
}



async function logoutButtonClicked()
{
    
    userToken = localStorage.getItem('userToken');
    sessionUser = sessionStorage.getItem('user');
    
    clearSession()
    
    if (userToken !== null){
        localStorage.removeItem('userToken');
         localStorage.removeItem('email');
        await fetch(getApiUrl('signout'), {
            method: 'post',
            headers:{
                'Content-Type':'application/json',
                'authToken': userToken,
            }
        })
        .then(response => { if(response.status == 400 || response.status == 401) {
                                window.alert('bad request');
                            }})
        .then(data => {console.log(data)})
        .catch(error => {console.log(error)})
    }

    else{
        window.alert('bad request');
    }
    window.location.replace('/');
}