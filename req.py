import requests

res = requests.get('https://127.0.0.0:8000/cats/cats').json()
print(res)