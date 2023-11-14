import requests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



s = Serializer('secret', 100)
user_id='sai.dappu@gmail.com'
token=s.dumps({'Id': user_id}).decode('utf-8')

req = requests.post("http://127.0.0.1:5000//api/reset-password", json={'token':token,'new_password':'Test1234'})
print(req.json())
