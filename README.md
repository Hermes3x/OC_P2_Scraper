Voici une version synthétique et claire à utiliser pour ton README :
# README
Ce script extrait les données des livres proposés par https://books.toscrape.com/index.html
Les données textuelles sont ensuite chargées dans des fichiers .csv 
Les fichiers .csv sont organisés par catégorie
Les fichiers (.csv , .jpg) sont enregistrés dans le répertoire suivant "C:\Users\jon_c\Documents\OpenClassroom\0 - Exercices\Projet 2\Book to scrape\Données"

## Prérequis
- Python 3.8+ installé

## Installation rapide

1. **Créer un environnement virtuel**  
   Sous le dossier du projet :  
   ```
   python -m venv env
   ```
   Active-le :  
   - Windows : `env\Scripts\activate`  
   - macOS/Linux : `source env/bin/activate`

2. **Installer les dépendances**  
   ```
   pip install -r requirements.txt
   ```

## Utilisation

Lancer le script principal depuis le terminal :
```
python scraper.py
```

## Structure
- `scraper.py` : script principal
- `requirements.txt` : dépendances