import requests
req = requests.post("http://127.0.0.1:5000/api/forgot-password", json={ 'email_id':'mouliks@test.com' })
print(req.json())
