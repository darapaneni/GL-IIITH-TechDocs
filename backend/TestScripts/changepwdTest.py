import requests
headers = {"authToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6Im1vdWxpa3NAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZSwibG9naW5UeXBlIjoiZW1haWwifQ.HTV8rV2O7wwPRX_MymdvBjNwHLQ-YwUgq-DELGxwu1M'}
req = requests.post("http://127.0.0.1:5000/api/changePassword", json={ 'currentPassword':'1234567', 'newPassword':'7654321' },headers=headers)
print(req.json())
