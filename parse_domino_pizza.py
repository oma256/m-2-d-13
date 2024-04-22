import requests
from bs4 import BeautifulSoup


def get_pizza_list(pizza_id=None):
    url = 'https://dominopizza.ru/'
    response = requests.get(url=url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    div_rim = soup.find('div', {'id': pizza_id})
    div_cls_cols = div_rim.find_all('div', {'class': 'col'})
    pizza_list = []

    for div_cls_col in div_cls_cols:
        div_cls_picture = div_cls_col.a.div.find('div', {'class': 'product-picture'})
        
        pizza_detail = div_cls_col.a.div.find(
            'div', {'class': 'product-card-content'}
        )

        pizza_id = pizza_detail.find(
            'div', {'class': 'product-name'}
        ).get('id')

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
            'id': pizza_id,
            'name': pizza_name,
            'description': pizza_description,
            'price': pizza_price,
            'picture': div_cls_picture.picture.img.get('src')
        })

    return pizza_list
