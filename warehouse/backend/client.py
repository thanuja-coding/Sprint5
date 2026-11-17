import requests
URL = "http://127.0.0.1:8000"
user_credentials = {"username": "abcdefgh","password": "12345"}


response = requests.post(url = URL+"/register",json=user_credentials)
print(response.status_code)
print(response.json())

response = requests.post(url=URL+"/login",json=user_credentials)
response_json = response.json()
access_token=response_json["access_token"]
refresh_token=response_json["refresh_token"]

header={"token":access_token}
response = requests.get(url=URL+"/packages",headers=header)
print(response.json())

header={"token":access_token}
response=requests.get(url=URL+"/packages/2",headers=header)
print(response.json())

header={"token":access_token}
update={"destination":"Mumbai"}
response=requests.patch(url=URL+"/packages/1",headers=header,json=update)
print(response.json())



