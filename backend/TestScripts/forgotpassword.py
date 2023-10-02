import requests
req = requests.post("http://127.0.0.1:5000/api/forgot-password")
print(req.json())
