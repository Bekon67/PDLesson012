from pprint import pprint

from requests import get, post, delete


url1 = 'http://127.0.0.1:8000/cats/cats/3'
url_root = 'http://127.0.0.1:8000/cats/cats'

# r = post(url1, data={'name': 'Murzik', 'breed': 'siams', 'age': 35})
# print(r.json())

r = delete(url1)
print(r.text)

r = get(url_root)
pprint(r.json())

