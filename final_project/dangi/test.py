import requests

url = 'http://127.0.0.1:8000/user/auth/'

response = requests.post(url, data={'username':'playdata', 'password': 'qwer0502'})
print(response.text)

# myToken = response.json() #text가 아니라 json으로 받아와야함
#
# token = myToken['token']
# header = {'Authorization' : 'Token ' + token} #'Token ' < 스페이스바 하나를 넣어줘야함
# response = requests.get('http://127.0.0.1:8000/user/user_list/', headers=header) #header가 아닌 headers임
# print(response.text)