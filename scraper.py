import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
livre = requests.get(url)
reponse = livre.content
soup = BeautifulSoup(reponse, 'html.parser')

produit = {}

h1 = soup.find_all('h1')
titre = h1[0].get_text()

td = soup.find_all('td')
upc = td[0].get_text()
prix_taxe_ex = td[2].get_text()
prix_taxe_inc = td[3].get_text()
en_stock = td[5].get_text()
categorie = td[1].get_text()
review = td[6].get_text()

p = soup.find_all('p')
description = p[3].get_text()

img = soup.find_all('img')
url_suffixe = img[0].get('src')
suffixe_transforme = url_suffixe.replace('../..','')
url_image = 'https://books.toscrape.com/'+ suffixe_transforme

produit = {
    'product_page_url' : url,
    'universal_ product_code (upc)' : upc,
    'title' : titre,
    'price_including_tax' : prix_taxe_inc,
    'price_excluding_tax' : prix_taxe_ex,
    'number_available' : en_stock,
    'product_description' : description,
    'category' : categorie ,
    'review_rating' : review,
    'image_url' : url_image
    }

print(produit)
