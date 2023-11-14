import requests
import sys

headers = {"authToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6Im1vdWxpa3NAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZSwibG9naW5UeXBlIjoiZW1haWwifQ.HTV8rV2O7wwPRX_MymdvBjNwHLQ-YwUgq-DELGxwu1M'}
paramsload = {"filename":'test_latex.tex'}

req =requests.get('http://127.0.0.1:5000/api/convertLatexToPdf', headers=headers, params=paramsload)
print(req.text)
