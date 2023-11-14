import requests
headers = {"authToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6Im1vdWxpa3NAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZSwibG9naW5UeXBlIjoiZW1haWwifQ._HohFYV5rS0fD8wRT1N42OYPI10hyXqtu70yPg0-_Fw'}
req = requests.get("http://127.0.0.1:5000/api/get_permissions", json={ 'DocId':'1' },headers=headers)
print(req.json())
req = requests.post("http://127.0.0.1:5000/api/set_permissions", json={ 'share_email':'mouliks@test.com','DocId':'1', 'permission_type':'edit' },headers=headers)
print(req.json())
req = requests.get("http://127.0.0.1:5000/api/get_permissions", json={ 'DocId':'1' },headers=headers)
print(req.json())
