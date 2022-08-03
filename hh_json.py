from pprint import pprint
from pickle import dump, load
from os.path import exists
import re
from collections import Counter
from json import dump as jdump
from requests import get
from pycbrf import ExchangeRates
from functions_hh import salary_processing

#  ввод интерeсующей вакансии
vacancy = input('Введите интересующую вакансию: ')
limit_pages = int(input('Введите интерecующее число страниц: '))
limit_skills = int(input('Введите интерecующее число навыков: '))
url = 'https://api.hh.ru/vacancies'
rate = ExchangeRates()  # загрузка текущих курсов валют
# загрузка файла с цифровыми кодами
if exists('area.pkl'):
    with open('area.pkl', mode='rb') as f:
        area = load(f)
else:
    area = {}
answer = get(url=url, params={'text': vacancy}).json()
pprint(answer)
count_pages = answer['pages']
result = {'keywords': vacancy,
          'count': 0}
sal = {'from': [], 'to': []}
skills_all = []
# сначала выявляем сколько будет получено страниц
# и готовим нужные переменные. А затем проходим по каждой из полученных страниц.
for page in range(count_pages):
    if page > limit_pages - 1:
        break
    else:
        print(f"Обрабатывается страница {page}")
    p = {'text': vacancy,
         'page': page}
    count_on_page = len(answer['items'])
    result['count'] += count_on_page
    for res in answer['items']:
        # pprint(res)
        skills_set = set()  # TODO переменная точно только к одной вакансии относится?
        city_vac = res['area']['name']
        # добавление города из ответа на запроса, если его нет в файле.
        if city_vac not in area:
            area[city_vac] = res['area']['id']
        ar = res['area']
        res_full = get(res['url']).json()
        # pprint(res_full)

        #  обработка описания вакансии. Вытаскивание английских слов из описания вакансии
        #  предполагается, что это навыки для IT
        pp = res_full['description']
        # print(pp)
        pp_re = re.findall(r'\s[A-Za-z-?]+', pp)
        # print(pp_re)
        its = set(x.strip(' -').lower() for x in pp_re)
        # print(its)

        # формирование списка навыков из официальных и вытащенных из описания
        for sk in res_full['key_skills']:
            skills_all.append(sk['name'].lower())
            skills_set.add(sk['name'].lower())
        # skills |= sk1
        for it in its:
            if not any(it in x for x in skills_set):
                skills_all.append(it)
        # окончание формирования списка навыков

        # обработка заплаты
        sal = salary_processing(res_full, res, sal, rate)

# print(skillis)
sk2 = Counter(skills_all)
# pprint(sk2)
skills_out = [{'name': name, 'count': count, 'percent': round((count / result['count']) * 100, 2)}
              for name, count in sk2.most_common(limit_skills)]
up = sum(sal['from']) / len(sal['from'])
down = sum(sal['to']) / len(sal['to'])
result.update({'salary_down': round(up, 2),
               'salary_up': round(down, 2),
               'requirements': skills_out})

pprint(result)
# сохранение файла с результами работы
with open('result.json', mode='w') as f:
    jdump([result], f)
with open('area.pkl', mode='wb') as f:
    dump(area, f)
