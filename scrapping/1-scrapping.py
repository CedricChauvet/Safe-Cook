"""
ce code recuypere des information sur le cout le temps de preparation et la difficulté.
ainsi que le titre et la note de la recette. il n'est pas complet et pas entierement fonctionnelle
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

def get_recipe_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    # Récupération du titre
    titre = soup.find('h1').text

    # La classe recipeV2-container contient les informations de la recette
    ma_classe = soup.find( class_= 'recipeV2-container')

    ma_classe_primary = ma_classe.find("div", class_="recipe-primary") # temps de cuisson, difficulté, coût
    mon_score = soup.find("span", class_="recipe-header__rating-text").text  # note
    
    ma_difficulte= ma_classe_primary.find_all('i')
    for item in ma_difficulte:
        # Vérifier si l'item contient une icône
        icon = item.find('i', class_='icon')
        print("icon",icon)
        

    return MarmitonRecipe(
        title=titre,
        rating=mon_score,
        review_count=True,
        prep_time=mon_temps,
        difficulty=True,
        cost=True,
        servings=True,
        ingredients=True,
        steps=True,
        tips=True,
        tags=True,
        url=url
    )
        



# Test
url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
titre = get_recipe_details(url)
print(titre)