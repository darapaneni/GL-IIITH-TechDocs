
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
            'firstName':'new',
            'lastName':'new89789789',
                    
            'address':{
                'streetAddress':'newStreeatt',
                'state': 'newSte',
                'country': 'newCountry',
                    },
            'occupation':'newoccupation',
            'purposeOfUse':'NewUsage'
    
        }
    }
headers = {"authToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJFbWFpbCI6InRlc3RAdGVzdC5jb20iLCJpc0FkbWluIjpmYWxzZX0.7d4LVnr43Od8tK7tcCdMMRoieXYD8xycLJBxxQxSDOU'}
req = requests.post('http://127.0.0.1:5000/api/updateProfile', json=json_obj, headers=headers)
print(req.json())

##For GetProfile
req = requests.post('http://127.0.0.1:5000/api/getProfile', headers=headers)
print(json.dumps(req.json(), indent=3))

#####METHOD NOT ALLOWED#######
req =requests.get("http://127.0.0.1:5000/api/getProfile", headers=headers)
print(req.json())