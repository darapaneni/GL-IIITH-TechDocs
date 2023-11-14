
# {authToken:"xxxxxxxxxxxxx",
# userData:{
#             firstName:"ghjgjg",
#             lastName:"jhjghjg"
#           },
# address : {
#             streetAddress: "xxxx",
#              state:"yyyy",
#              country:"zzzz"
#             },
#              occupation: "ooooo",
#              purposeOfUse:"pppp"
#             }                      
# }

##For updateProfile
import requests
import json
json_obj={ 
        'userData':{
            'firstName':'Soumava',
            'lastName':'Mk',
                    
            'address':{
                'streetAddress':'N S C Bose Road',
                'state': 'WB',
                'country': 'IND',
                    },
            'occupation':'IT',
            'purposeOfUse':'Test'
    
        }
    }
headers = {"authToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6Im1vdWxpa3NAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZSwibG9naW5UeXBlIjoiZW1haWwifQ.HTV8rV2O7wwPRX_MymdvBjNwHLQ-YwUgq-DELGxwu1M'}
req = requests.post('http://127.0.0.1:5000/api/updateProfile', json=json_obj, headers=headers)
print(req.json())

##For GetProfile
req = requests.post('http://127.0.0.1:5000/api/getProfile', headers=headers)
print(json.dumps(req.json(), indent=3))

#####METHOD NOT ALLOWED#######
##req =requests.get("http://127.0.0.1:5000/api/getProfile", headers=headers)
##print(req.json())
