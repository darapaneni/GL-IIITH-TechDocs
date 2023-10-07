import requests
import sys


req = requests.post('http://127.0.0.1:5000/api/signin', json={'loginType':'email','email':'Test1@Test','password':'Test123', 'rememberMe':1})
print(req.json())
