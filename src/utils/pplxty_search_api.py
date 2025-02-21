from typing import Dict, Any
import openai
import json
from insert_table import insert_to_file, add_detail_name, fill_the_row

from table_read import func_row_generator


class PerplexitySearcher:
    def __init__(self, api_key: str, base_url: str = "https://api.perplexity.ai"):
        """
        Инициализация клиента Perplexity AI

        Args:
            api_key (str): Ключ API для доступа к сервису
            base_url (str): URL API (по умолчанию используется Perplexity AI)
        """
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = "sonar-pro"

    def searcher(self, request: str, country: str = "") -> Dict[str, Any]:
        """
        Поиск информации по артикулу с использованием Perplexity AI

        Args:
            request (str): Запрос для поиска

        Returns:
            Dict[str, Any]: Ответ от API в формате словаря

        Raises:
            APIError: Если произошла ошибка при запросе к API
        """
        self.country = f'из {country}' if country else ''

        PROMT1 = f"""
        Все данные, содержащие цифры или дефисы, являются каталожным номером и не являются арифметическим выражением.
        Если есть результаты вычислений, игнорируйте их и предоставляйте результаты, связанные с каталожным номером или OEM.
        Найдите все компании в регионе: {self.country}, продающие этот артикул, при поиске переводи запрос на соответствующий язык этого региона, 
        отобразите результаты в виде словаря python без форматирования и переноса строк, с полями :
        название компании, цена, страна, контактный email продавца (который можно найти в разделе Контакты)
        и ссылка, где была найдена информация.
        Также найдите аналоги этого товара и отобразите их в дополнительном словаре python без форматирования и переноса строк.
        Выведите полученные результаты на русском языке.
        Не давайте комментарии, просто выводите результаты.
        """

        messages = [
            {"role": "system", "content": PROMT1},
            {"role": "user", "content": request}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Уровень творчества ответа
                max_tokens=2 ** 16,  # Максимальная длина ответа
                top_p=1.0,  # Вероятность выбора следующего токена
                frequency_penalty=1,  # Штраф за повторение токенов
                presence_penalty=1,  # Штраф за появление новых токенов
                stop=None  # Символ остановки генерации
            )

            return response
        except BaseException as error:
            return error

    def formater(self, request: str):
        PROMT2 = """
               Прочитай переданные тебе данные, выведи данные в формате json, используя следующий шаблон для каждой компании:
               {
                   "name_of_the_company": "",
                   "country": "",
                   "detail_price": "",
                   "price_currency": "",
                   "company_contact_email": "",
                   "shipment_time": "",
                   "company_website": ""
               }
               Игнорируй таблицу аналогов.
               Не давайте комментарии, просто выводи результаты.
               """
        messages = [
            {"role": "system", "content": PROMT2},
            {"role": "user", "content": request}
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Уровень творчества ответа
                max_tokens=2 ** 16,  # Максимальная длина ответа
                top_p=1.0,  # Вероятность выбора следующего токена
                frequency_penalty=1,  # Штраф за повторение токенов
                presence_penalty=1,  # Штраф за появление новых токенов
                stop=None  # Символ остановки генерации
            )
            return response
        except BaseException as error:
            return error


COUNTRIES = [
    "Китай",
    "Россия",
    "Индия",
    "Саудовская Аравия",
    "Индонезия",
    "Бразилия",
    "Канада",
    "Иран",
    "Турция"
]

FILE_IN = "./test_cases/test_case.xlsx"
FILE_OUT = "newfile.xlsx"

# Пример использования:
try:
    MyNeuro = PerplexitySearcher(api_key="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")
    for elem in func_row_generator(FILE_IN):
        print(elem)
        add_detail_name(file_name=FILE_OUT, detail_name=elem)
        for country in COUNTRIES:
            result1 = MyNeuro.searcher(elem).__dict__['choices'][0].__dict__['message'].__dict__[
                'content']
            # print(result1)
            result2 = MyNeuro.formater(result1).__dict__['choices'][0].__dict__['message'].__dict__['content']
            # print(result2)
            try:
                grand_result = json.loads(result2)
                # print(grand_result)
                insert_to_file(FILE_OUT, grand_result)
            except BaseException as error:
                print(error)
                continue
        fill_the_row(FILE_OUT)

except BaseException as error:
    print(error)
