from pycbrf import ExchangeRates


def salary_processing(res_full, res, sal, rate):
    # rate = ExchangeRates()  # загрузка текущих курсов валют

    if res_full['salary']:
        code = res_full['salary']['currency']
        if rate[code] is None:
            code = 'RUR'
        k = 1 if code == 'RUR' else float(rate[code].value)
        sal['from'].append(k * res_full['salary']['from']
                           if res['salary']['from'] else
                           k * res_full['salary']['to'])
        sal['to'].append(k * res_full['salary']['to']
                         if res['salary']['to'] else
                         k * res_full['salary']['from'])
    return sal
