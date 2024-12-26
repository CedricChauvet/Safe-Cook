"""
cette partie du code est fonctionnelle
on recupere les informations de la page marmiton et on les affiche
titre et note.
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MarmitonRecipe:
    title: str
    rating: Optional[float]
    review_count: int
    prep_time: str
    difficulty: str
    cost: str
    servings: int
    ingredients: List[str]
    steps: List[str]
    tips: List[str]
    tags: List[str]
    url: str

def get_recipe_details(url: str) -> Optional[MarmitonRecipe]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraction du titre
    title = soup.find('h1').text.strip()
    
    # Extraction de la note
    try:
        # Chercher tous les divs contenant des notes (format: "4.6/5")
        rating_text = None

        # un exemple de recupération de la note
        rating_div = soup.find('div', class_='recipe-header__rating')
        # print("rd ",rating_div)
        rating_text = rating_div.find('span', class_='recipe-header__rating-text').text.strip()
        print("rd ",rating_text)

        for div in soup.find_all('div'):
            # ensemble des données de la page
            classes = div.get('class', [])
            print("classes",classes)

            text = div.text.strip()
            if '/5' in text and len(text) < 10:  # Évite les longs textes contenant "/5"
                rating_text = text
                break
        
        rating = float(rating_text.replace('/5', '')) if rating_text else None
        review_count = 0  # À implémenter si nécessaire
    
    except Exception as e:
        print(f"Erreur lors de l'extraction de la note: {e}")
        rating = None
        review_count = 0
    
    # Pour le test, on remplit les autres champs avec des valeurs par défaut
    return MarmitonRecipe(
        title=title,
        rating=rating,
        review_count=review_count,
        prep_time="",
        difficulty="",
        cost="",
        servings=0,
        ingredients=[],
        steps=[],
        tips=[],
        tags=[],
        url=url
    )

# Test
url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
recipe = get_recipe_details(url)
print(f"Titre: {recipe.title}")
print(f"Note: {recipe.rating}/5")