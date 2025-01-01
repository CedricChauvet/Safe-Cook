"""
Structure de la page d'une recette Marmiton:
- Titre
- Note et nombre d'avis
- Temps de préparation
- Difficulté
- Coût
- Portions
et c'est tout pour l'instant
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional


def get_portions(soup):
    div_element = soup.find('div', class_='mrtn-recette_ingredients-counter')
    servings_number = div_element['data-servingsnb']
    servings_unit = div_element['data-servingsunit']
    return f"{servings_number} {servings_unit}"


def get_title(soup):
    # Extraction du titre
    title = soup.find('h1').text.strip()
    return title    


def get_rating(soup):
    rating = None
    rating_div = soup.find('div', class_='recipe-header__rating')
    if rating_div:
        rating_text = rating_div.find('span', class_='recipe-header__rating-text')
        if rating_text:
            rating = float(rating_text.text.strip().replace('/5', ''))
    return rating


def get_recipe_primary(soup):
    # Extraction du temps de préparation
    time_total = soup.find(class_="time__total")
    if time_total:
        # Récupérer le texte du span (label)
        time_label = time_total.find('span')
        # Récupérer le texte du div (valeur)
        time_value = time_total.find('div').text.strip()
        prep_time = time_value

    # Récupérer le conteneur recipe-primary
    recipe_primary = soup.find('div', class_='recipe-primary')
    if recipe_primary:
        # Chercher tous les items à l'intérieur de recipe-primary
        recipe_items = recipe_primary.find_all('div', class_='recipe-primary__item')
        
        # Parcourir les items pour trouver la difficulté et le coût
        for item in recipe_items:
            # Vérifier si l'item contient une icône
            icon = item.find('i', class_='icon')
            if icon:
                # Récupérer le span correspondant
                span_text = item.find('span').text if item.find('span') else ""
                
                # Identifier le type d'information selon l'icône
                if 'icon-difficulty' in icon['class']:
                    difficulty = span_text
                elif 'icon-price' in icon['class']:
                    cost = span_text
    return  prep_time, difficulty, cost


    
def get_recipe_details(soup):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:

        
        title = get_title(soup)
        note = get_rating(soup) 
        prep_time, difficulty, cost = get_recipe_primary(soup)
        servings = get_portions(soup)
        return title, note, prep_time, difficulty, cost, servings,

    except Exception as e:
        print(f"Erreur lors de l'extraction de la recette: {e}")
        return None



# # Usage
# html_content = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"


# # Usage
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# }

# response = requests.get(html_content, headers=headers)
# response.raise_for_status()
# soup = BeautifulSoup(response.text, 'html.parser')



# recipe = get_recipe_details(soup)

# print(recipe)


