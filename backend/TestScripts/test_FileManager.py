import requests
import sys

headers = {"authToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6InRlc3RAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZX0.7d4LVnr43Od8tK7tcCdMMRoieXYD8xycLJBxxQxSDOU'}

#------------------------------
# Test /file/creat - for upload
# -----------------------------

req = requests.post('http://127.0.0.1:5000/api/filecreate',
            json={"DocId":"0", "DocName":"test.tex","IsUpload":False,"DocText":"r\andom\data","RefDocId":"0"},
            headers=headers)

print(req.text)


# req = requests.post('http://127.0.0.1:5000/api/filerename',
#             #json={"DocId":"1", "DocName":"retest.tex","IsUpload":False},
#             json={"DocId":"1", "DocName":"retest.tex","IsUpload":False},
#             headers=headers)

# print(req.text)

#------------------
# Test /file/create
#------------------
#res = requests.post('http://127.0.0.1:5000/file/create', json={"UserId":"u345", "DocName":""})
#print(res.json())
# output will be 
# {'data': '{"DocId": 4, "DocName": "untitled_20221011212801.tex", "UserId": "u123", "body": ""}', 'message': 'success'}

#------------------
# Test /file/modify - update the file or save the file
#------------------
#res = requests.post('http://127.0.0.1:5000/file/modify', 
# json={"UserId":"u345", "DocId":"3", "DocName":"document3.tex", 
# "Doctext":"justice league", "Operation":"update"})
#print(res.json())

#------------------
# Test /file/modify - rename the file 
#------------------
#res = requests.post('http://127.0.0.1:5000/file/modify', 
#                    json={"UserId":"u234", "DocId":"2", "DocName":"document2.tex", 
#                          "Doctext":"avengers assemble!", "Operation":"rename"})
#print(res.json())







