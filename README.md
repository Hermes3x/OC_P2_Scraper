# Books to Scrape — extracteur de données

Script Python qui extrait les données de tous les livres du site de démonstration
[books.toscrape.com](https://books.toscrape.com/index.html), catégorie par catégorie.

Pour chaque catégorie, il produit :

- un fichier **CSV** qui regroupe les informations de chaque livre : URL, code UPC, titre, prix
  TTC et HT, stock disponible, description, catégorie, note sur 5 et URL de l'image ;
- les **images de couverture** des livres, au format JPG.

Les fichiers sont enregistrés dans un dossier `Données/`, créé à côté du script, avec un
sous-dossier par catégorie.

## Prérequis

- Python 3.10 ou plus récent (le script utilise `match`)

## Installation

1. Créer un environnement virtuel dans le dossier du projet :

   ```bash
   python -m venv env
   ```

2. L'activer :

   - Windows : `env\Scripts\activate`
   - macOS / Linux : `source env/bin/activate`

3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

```bash
python scraper.py
```

Le script affiche sa progression dans le terminal (catégorie, puis chaque livre extrait).

## Structure

- `scraper.py` : script principal (extraction, transformation, chargement)
- `requirements.txt` : dépendances
