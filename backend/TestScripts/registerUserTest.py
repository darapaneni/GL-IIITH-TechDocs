import requests
import sys


req = requests.post('http://127.0.0.1:5000/api/register', json={'loginType':'email','email':'test@test.com','password':'1234567','FirstName':'Test','LastName':'Test', 'rememberMe':1})
print(req.json())

