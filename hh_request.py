from pprint import pprint

from requests import get


url = 'https://api.hh.ru/vacancies'
params = {'text': 'python'}
res = get(url, params=params).json()
print(res['found'])
pprint(res['items'])


