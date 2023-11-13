import requests

url = "http://127.0.0.1:8080/grammar_edits"
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}
data = {
    "sentence": "Incorrectly spelled sentance wih grammar mistakes.",
}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.json())

url = "http://127.0.0.1:8080/grammar_correction"
headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}
data = {
    "sentence": "Incorrectly spelled sentance wih grammar mistakes.",
}

response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.json())
