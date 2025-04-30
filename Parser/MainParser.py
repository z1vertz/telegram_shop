import requests
from bs4 import BeautifulSoup as b
import re


def url_request(url):
    """Получает инит библиотеки"""
    quet = requests.get(url)
    soup = b(quet.text, "html.parser")
    return soup

#     1424 - кол-во с примером с ауди
#3 + pages * 2 * 10 * 7 = 199363
def parser(url):
    """Получает количество страниц"""
    soup = url_request(url)
    pages = int([''.join(x.text.split(" ")) for x in (soup.find_all('a', class_='page-link'))][6])

    print(pages)

    """Цикл который подключается к странице 10 предложений и получает ссылку"""
    for iterations in range(0, int(pages)):
        url = f"{url.split('?')[0]}?page={iterations}"  # обновление переменной url
        print(url)
        soup = url_request(url)
        links = [href.get('href') for href in soup.find_all('a', class_='address')]
        list_result = []
        """Цикл который итерациями подключается к каждой полученой ссылке товара"""
        for sites in links:
            nowsite = url_request(str(sites))

            """Каждую итерацию получается информация последовательно с каждого сайта"""
            for i in nowsite.find_all('div', class_='technical-info ticket-checked'):
                if "модель" in i.text.split(', ')[1:]:

                    """Виделение текста с полученой информации парсера"""
                    model_match = re.search(r'Марка, модель, рік (.+?)(Двигун|в)', i.text[1:])
                    liters_match = re.search(r'Двигун (.+?) л', i.text[1:])
                    fuel_match = re.search(r'(Бензин|Дизель|Електро|Гібрид)', i.text[1:])
                    color_match = re.search(r'Колір (.+?)(В|Остання|Перша)', i.text[1:])
                    operation_match = re.search(r'операція (.+?) ', i.text[1:])

                    info_list = [model_match.group(1).strip() if model_match else None,
                            [prices.text for prices in nowsite.find_all('strong')][0],
                            liters_match.group(1) if liters_match else None,
                            'Бензин' if fuel_match.group(1) == 'Бензин' else 'Дизель' if fuel_match.group(1) == 'Дизель' else 'Електро' if fuel_match.group(1) == 'Електро' else 'Гібрид' if fuel_match.group(1) == 'Гібрид' else None,
                            color_match.group(1).strip() if color_match else None,
                            operation_match.group(1).strip() if operation_match else None,
                            sites]
                    print(info_list)
                    list_result.append(info_list)

if __name__ == "__main__":
    """Проверка на основной файл(пока что без потребности), работает любая ссылка со страницы предложений вот пример"""
    #https://auto.ria.com/uk/legkovie/audi/?page=5
    parser(input("<Input the link:> "))
    print("ON, ALL ARE GOOD")

