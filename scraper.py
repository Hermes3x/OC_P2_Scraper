import requests
from bs4 import BeautifulSoup
import csv
import urllib.request
import os

site_url = "https://books.toscrape.com/index.html"
site_content = requests.get(site_url)
site_response = site_content.content
site_soup = BeautifulSoup(site_response, 'html.parser')

category_marker = site_soup.find('div', class_='side_categories')
categories_href = category_marker.find_all('a')

dico_categories_names_url = {}

categories_names = []


# Recherche Nom et URL de chaque categories
for a in categories_href[1:]:
    category_name = a.get_text(strip=True)
    #print(category_name)
    category_url = ('https://books.toscrape.com/' + a['href'])
    categories_names.append(category_name)

    pages_urls = []
    
    category_content = requests.get(category_url)
    category_response = category_content.content
    category_soup = BeautifulSoup(category_response, 'html.parser')

    #Trouver nombre de page
    pages = category_soup.find('li', class_='current')
    if pages:
        pages = pages.get_text(strip=True)
        page_max = int(pages[-1])
        current_page = int(pages[5])
              
        if current_page < page_max:
            for page in range(page_max):
                base_url = category_url.replace('index.html','')
                page_next = page + 1
                page_next_url = (str(base_url) + "page-" + str(page_next) + ".html")
                pages_urls.append(page_next_url)
    else:
        pages_urls.append(category_url)

    #print(pages_urls)
    dico_categories_names_url[category_name] = pages_urls


categories_data = {}


for category_name in categories_names:
    os.makedirs(rf'C:\Users\jon_c\Documents\OpenClassroom\0 - Exercices\Projet 2\Book to scrape\{category_name}', exist_ok=True)
    for url in dico_categories_names_url[category_name]:        
        items_details = {
            'product_page_url': [],
            'universal_ product_code (upc)':[],
            'title' : [],
            'price_including_tax' : [],
            'price_excluding_tax' : [],
            'number_available' : [],
            'product_description' : [],
            'category':[],
            'review_rating':[],
            'image_url':[]
            }
        
        items_content = requests.get(url)
        items_content_response = items_content.content
        items_soup = BeautifulSoup(items_content_response, 'html.parser')
       
        items_h3 = items_soup.find_all('h3')

        #Récupération des urls
        for h3 in items_h3:
            item_url = h3.find('a')
            item_url = item_url['href']
            item_url_cleaned = item_url.replace('../../../','')
            item_url_def = 'https://books.toscrape.com/catalogue/'+ item_url_cleaned
            items_details['product_page_url'].append(item_url_def)


        for product_page_url in items_details['product_page_url']:
            #Récupération des données par URL d'un livre
            book_content = requests.get(product_page_url)
            book_response = book_content.content
            book_soup = BeautifulSoup(book_response, 'html.parser')

            # Récupération du code UPC
            td = book_soup.find_all('td')
            book_upc = td[0].get_text()
            items_details['universal_ product_code (upc)'].append(book_upc)

            #Récupération du titre d'un livre
            h1 = book_soup.find_all('h1')
            title = h1[0].get_text()
            items_details['title'].append(title)

            #Récupération du prix 
            price_including_tax = td[3].get_text()
            items_details['price_including_tax'].append(price_including_tax)

            #Récupération du prix hors taxe
            price_excluding_tax = td[2].get_text()
            items_details['price_excluding_tax'].append(price_excluding_tax)

            # Récupération quantité en stock
            number_available = td[5].get_text()
            items_details['number_available'].append(number_available)

            #Récupération description produit
            p = book_soup.find_all('p')
            product_description = p[3].get_text()
            items_details['product_description'].append(product_description)

            #Récupération categorie
            category = td[1].get_text()
            items_details['category'].append(category)

            #Récupération note
            review_rating = td[6].get_text()
            items_details['review_rating'].append(review_rating)

            #Récupération URL image
            img = book_soup.find_all('img')
            url_suffixe = img[0].get('src')
            suffixe_transforme = url_suffixe.replace('../..','')
            image_url = 'https://books.toscrape.com'+ suffixe_transforme
            items_details['image_url'].append(image_url)
            nom_image = f'{title}.jpg'
            nom_image_clean = nom_image.replace(':', '-').replace('#','').replace('*',' ').replace('?','').replace('!','').replace(';','').replace('/','').replace('|','').replace('\\','').replace('"','')
            chemin_fichier_image = os.path.join(rf'C:/Users/jon_c/Documents/OpenClassroom/0 - Exercices/Projet 2/Book to scrape/{category_name}/{nom_image_clean}')
            urllib.request.urlretrieve(image_url, chemin_fichier_image)


        categories_data[category_name] = items_details

        nom_fichier_csv = 'données_categorie_' + category_name + '.csv'
        chemin_fichier = chemin_fichier_image = os.path.join(rf'C:/Users/jon_c/Documents/OpenClassroom/0 - Exercices/Projet 2/Book to scrape/{category_name}/{nom_fichier_csv}')

        with open(chemin_fichier, 'w',newline="",encoding='utf-8') as csv_fiche_livre_donnes_extraites_par_categories:
            fieldnames = list(items_details.keys())
            writer = csv.DictWriter(csv_fiche_livre_donnes_extraites_par_categories, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(items_details['title'])):
                ligne = {key: items_details[key][i] for key in fieldnames}
                writer.writerow(ligne)