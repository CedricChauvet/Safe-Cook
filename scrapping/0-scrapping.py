"""
Ce code est fonctionnel,il recupere les ingredients d'une page marmiton
il afficher les quantité les unités et les noms des ingredients
pour telle recette
"""
import requests
from bs4 import BeautifulSoup


# Fonction pour extraire les ingrédients
def extract_ingredients(soup):

    ing_out = []
    # Récupérer les ingrédients avec find_all
    mes_ingredients = soup.find_all("div", class_="card-ingredient")
    # boucle for pour parcourir les ingredients
    for ingrdt in mes_ingredients:
        name_ingredient = ingrdt.find("span", class_="ingredient-name").text
        nmb_ingredient = ingrdt.find("span",
                                     class_="card-ingredient-quantity").text
        unite = ingrdt.find("span", class_="card-ingredient-unit")

        # Nettoyer et combiner tout en une ligne
        quantite = (nmb_ingredient + (unite.text if unite else ""))\
            .replace(" ", "").replace('\n', '').replace('\t', '')\
            .strip()
        nom = name_ingredient.replace('\n', '').replace('\t', '').strip()

        # Afficher la ligne complète
        ing_out.append(f"{quantite} {nom}")
    return ing_out


# # Usage
# html_content = "https://www.marmiton.org/recettes/"\
#                "recette_pates-a-la-carbonara_80453.aspx"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#     'AppleWebKit/537.36'
# }

# response = requests.get(html_content, headers=headers)
# response.raise_for_status()
# soup = BeautifulSoup(response.text, 'html.parser')

# ing = extract_ingredients(soup)
# print(ing)
