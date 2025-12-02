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

# Recherche Nom et URL de chaque categories
for a in categories_href[1:]:

    pages_urls = []

    #Récupération du nom de la catégorie
    category_name = a.get_text(strip=True)
    print(f'le nom de la catégorie traitée est {category_name}')
    
    #Récupération de l'URL de la 1ère page de la catégorie
    category_url = ('https://books.toscrape.com/' + a['href'])
    print(f"L'URL de cette catégorie est {category_url}")
   
    
    #Récupération du contenu de la 1ère page de la catégorie
    category_content = requests.get(category_url)
    category_response = category_content.content
    category_soup = BeautifulSoup(category_response, 'html.parser')

    #Trouver nombre de page de la catégorie
    pages = category_soup.find('li', class_='current')
    if pages:
        pages = pages.get_text(strip=True)
        page_max = int(pages[-1])
        print(f'Présence de {page_max} pages')
        current_page = int(pages[5])
                              
        if current_page < page_max:
            for page in range(page_max):
                base_url = category_url.replace('index.html','')
                page_next = page + 1
                page_next_url = (str(base_url) + "page-" + str(page_next) + ".html")
                print(f'Conversion des URLs dans un format exploitable : {page_next_url}')
                pages_urls.append(page_next_url)
                
    else:
        pages_urls.append(category_url)

    
    print(f"liste pages_ulrs de la catégorie traitée {pages_urls}")   

    #Ajout des données extraites au dictionnaire 
    dico_categories_names_url[category_name] = pages_urls
    print("Mise à jour du dictionnaire regroupant Nom de catégorie + URLs")
 
print(f'dictionnaire Noms + URLs pages {dico_categories_names_url}')

categories_data = {}

#Création d'un dossier par catégorie
for category_name in dico_categories_names_url:
    print(f"Création d'un dossier reprenant le nom de la categorie : {category_name}")
    os.makedirs(rf'C:\Users\jon_c\Documents\OpenClassroom\0 - Exercices\Projet 2\Book to scrape\Données\{category_name}', exist_ok=True)

    #Création d'un dictionnaire "temporaire" par catégorie
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
    

    for url in dico_categories_names_url[category_name]:        
        print(f"Recherche des URLs des livres de la catégorie {category_name} sur la page")
        items_content = requests.get(url)
        items_content_response = items_content.content
        items_soup = BeautifulSoup(items_content_response, 'html.parser')
        
        #Identification des balises h3
        items_h3 = items_soup.find_all('h3')

        #Récupération des urls des pages des livres de la catégorie
        for h3 in items_h3:
            item_url = h3.find('a')
            item_url = item_url['href']
            item_url_cleaned = item_url.replace('../../../','')
            item_url_def = 'https://books.toscrape.com/catalogue/'+ item_url_cleaned
            items_details['product_page_url'].append(item_url_def)
            print(f"Ajout de l'URL du livre au dictionnaire provisoire items_details : {item_url_def}")

    #Récupération des données par URL d'un livre
    for product_page_url in items_details['product_page_url']:
        
        book_content = requests.get(product_page_url)
        book_response = book_content.content
        book_soup = BeautifulSoup(book_response, 'html.parser')

        #Récupération du titre d'un livre
        h1 = book_soup.find_all('h1')
        title = h1[0].get_text(strip=True)
        items_details['title'].append(title)
        print(f'Le titre du livre est "{title}" ; Ajout au dictionnaire provisoire items_details')

        # Récupération du code UPC
        td = book_soup.find_all('td')
        book_upc = td[0].get_text(strip=True)
        items_details['universal_ product_code (upc)'].append(book_upc)
        print(f'Le code UPC du livre "{title}" est {book_upc} ; Ajout au dictionnaire provisoire items_details')

        #Récupération du prix 
        price_including_tax = td[3].get_text(strip=True)
        items_details['price_including_tax'].append(price_including_tax)
        print(f'Le prix TTC du livre "{title}" est {price_including_tax} ; Ajout au dictionnaire provisoire items_details')

        #Récupération du prix hors taxe
        price_excluding_tax = td[2].get_text(strip=True)
        items_details['price_excluding_tax'].append(price_excluding_tax)
        print(f'Le prix HT du livre "{title}" est {price_excluding_tax} ; Ajout au dictionnaire provisoire items_details')

        # Récupération quantité en stock
        number_available = td[5].get_text(strip=True)
        number_available_clean = number_available[10]
        items_details['number_available'].append(number_available_clean)
        print(f'Le nombre du livre "{title}" dicponible {number_available_clean} ; Ajout au dictionnaire provisoire items_details')

        #Récupération description produit
        p = book_soup.find_all('p')
        product_description = p[3].get_text(strip=True)
        items_details['product_description'].append(product_description)
        print(f'Récupération de la description du livre "{title}" ; Ajout au dictionnaire provisoire items_details')

        #Récupération categorie
        category = td[1].get_text(strip=True)
        items_details['category'].append(category)
        print(f'Récupération de la catégorie du livre "{title}" ; Ajout au dictionnaire provisoire items_details')

        #Récupération note
        review_rating = book_soup.find('p', class_='star-rating')
        rating_class = review_rating.get('class', [])
        items_details['review_rating'].append(rating_class[1])
     
        #Récupération URL image
        img = book_soup.find_all('img')
        url_suffixe = img[0].get('src')
        suffixe_transforme = url_suffixe.replace('../..','')
        image_url = 'https://books.toscrape.com'+ suffixe_transforme
        items_details['image_url'].append(image_url)
        nom_image = f'{title}.jpg'
        nom_image_clean = nom_image.replace(':', '-').replace('#','').replace('*',' ').replace('?','').replace('!','').replace(';','').replace('/','').replace('|','').replace('\\','').replace('"','')
        chemin_fichier_image = os.path.join(rf'C:/Users/jon_c/Documents/OpenClassroom/0 - Exercices/Projet 2/Book to scrape/Données/{category_name}/{nom_image_clean}')
        urllib.request.urlretrieve(image_url, chemin_fichier_image)
        print(f"Ajout de l'image du livre {title} dans le dossier de la catégorie {category_name}")


    categories_data[category_name] = items_details
    print("Ajout des données extraites au dictionnaire répertoriant les détails des livres par catégorie")

    nom_fichier_csv = '0_données_categorie_' + category_name + '.csv'
    chemin_fichier = chemin_fichier_image = os.path.join(rf'C:/Users/jon_c/Documents/OpenClassroom/0 - Exercices/Projet 2/Book to scrape/Données/{category_name}/{nom_fichier_csv}')
    print("Création du chemin d'accès pour l'enregistrement des données dans répertoire local")

    with open(chemin_fichier, 'w',newline="",encoding='utf-8-sig') as csv_fiche_livre_donnes_extraites_par_categories:
        print(f"Création d'un fichier CSV compilant l'ensemble des renseignements extraits pour les livres de la catégorie {category_name}")
        fieldnames = list(items_details.keys())
        writer = csv.DictWriter(csv_fiche_livre_donnes_extraites_par_categories, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(items_details['title'])):
            ligne = {key: items_details[key][i] for key in fieldnames}
            writer.writerow(ligne)