import requests
from bs4 import BeautifulSoup


def get_rim_pizza():
    url = 'https://dominopizza.ru/'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_rim = soup.find('div', {'id': 'rimskaya'})
    div_cls_cols = div_rim.find_all('div', {'class': 'col'})
    pizza_list = []

    for div_cls_col in div_cls_cols:
        pizza_detail = div_cls_col.a.div.find(
            'div', {'class': 'product-card-content'}
        )

        pizza_name = pizza_detail.find(
            'div', {'class': 'product-name'}
        ).get_text()

        pizza_description = pizza_detail.find(
            'p', {'class': 'product-description'}
        ).get_text()

        pizza_price = pizza_detail.find(
            'div', {'class': 'price'}
        ).get_text()

        pizza_list.append({
            'name': pizza_name,
            'description': pizza_description,
            'price': pizza_price,
        })

    return pizza_list
