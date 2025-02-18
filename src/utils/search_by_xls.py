import chardet
import csv
from classes import Article, Provider

def detect_and_read_csv(filename):
    # Определяем кодировку
    with open(filename, 'rb') as rawdata:
        result = chardet.detect(rawdata.read())
        charenc = result['encoding']
    with open(filename, 'r', encoding=charenc, newline='') as file:
        reader = csv.reader(file)
        return list(reader)


def best_price(providers: list[Provider]):
    min_price = 10**60
    resp = 'Не найдено лучшего предложения'
    for elem in providers:
        if type(elem.end_price) == int or type(elem.end_price) == float:
            if elem.end_price < min_price:
                min_price = elem.end_price
                resp = (elem.label, elem.country)
    return (min_price, resp)

res_zakupka = {}

rows = detect_and_read_csv('./test_cases/test1.csv')
for row in rows[2:]:
    full_stroka = ''
    for elem in row:
        full_stroka += ''.join(elem)
    partial = full_stroka.split(";")
    providers = []
    try:
        for i in range(5):
            new_pr = Provider(partial[33+16*i], partial[34+16*i], partial[35+16*i], partial[36+16*i], partial[37+16*i], partial[38+16*i])
            new_pr.convert_price_from_currency()
            providers.append(new_pr)
        article = Article(partial[11], partial[8])
        # print(article.name, article.OEM_number)
        res = best_price(providers)
        if  res[0] < 10**59:
            if res[1][0] in res_zakupka:
                res_zakupka[res[1][0]].append(article.OEM_number)
            else:
                res_zakupka[res[1][0]] = [article.OEM_number]
    except IndexError:
        continue
for key, val in res_zakupka.items():
    print(key, val)
