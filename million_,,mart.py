import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests

names= []
prices = []

for pages in range(1,8,1):
    url = f'https://millionmartgroup.com/page/{pages}/?5&post_type=product&product_cat=0'

    with requests.get(url) as resp:
            resp.raise_for_status()
            content = resp.content

    soup = BeautifulSoup(content,'html.parser')

    div = soup.find('div',class_='site-content shop-content-area col-lg-9 col-12 col-md-9 description-area-before content-with-products wd-builder-off')

    for i in div.find_all('div',class_='product-element-bottom product-information'):
            name =str.upper(i.find('h3',class_='wd-entities-title').text.strip())
            names.append(name)
    
    for i in div.find_all('div',class_='product-element-bottom product-information'):
        element = i.find('div',class_='wrapp-product-price')
        price=element.text.strip() if element else 0
        prices.append(price)

df = pd.DataFrame({
      'name':names,
      'price':prices
})
df['price'] = df['price'].str.replace('Ks', '')
df.to_csv('million_mart.csv',index=False)
