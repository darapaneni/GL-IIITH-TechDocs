import requests
headers = {'x-access-tokens':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6InRlc3RAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZX0.7d4LVnr43Od8tK7tcCdMMRoieXYD8xycLJBxxQxSDOU'}
req = requests.get('http://127.0.0.1:5000/filemanagerhealth', headers=headers)
print(req.json())
