import requests
import sys


req = requests.post('http://127.0.0.1:5000/api/signin', json={'loginType':'email','email':'test@test.com','password':'1234567', 'rememberMe':1})
print(req.json())

##Below response - "User not Registered"
req = requests.post("http://127.0.0.1:5000/api/signin", json={'loginType':'gmail', 'email':'test@test.com', 'password':'1234567', 'rememberMe':1})
print(req.json())

##Below response - "Email field cannot be empty"
req = requests.post("http://127.0.0.1:5000/api/signin", json={'loginType':'email', 'email':'', 'password':'1234567', 'rememberMe':1})
print(req.json())

##Below repsonse - "Password field cannot be empty"
req = requests.post("http://127.0.0.1:5000/api/signin", json={'loginType':'email', 'email':'test@test.com', 'password':'', 'rememberMe':1})
print(req.json())

## Below response - "User not Registered"
req = requests.post("http://127.0.0.1:5000/api/signin",json={'loginType':'email','email':'idonotexists','password':'1234567','rememberMe':1})
print(req.json())
