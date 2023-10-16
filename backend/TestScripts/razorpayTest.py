import requests
req = requests.post("http://127.0.0.1:5000/api/razorSubmit", json={ 'amt':'1', 'orderDesc':'test', 'fname':'S', 'lname':'Moulik', 'userId':'81577282-11fe-4db5-b52a-e833e64352f5' })
##print(req.json())
##req = requests.post("http://127.0.0.1:5000/api/razorStatus")
