

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
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialisation des variables
        difficulty = ""
        cost = ""
        
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

        print(f"Difficulté trouvée: {difficulty}")
        print(f"Coût trouvé: {cost}")
        
        return MarmitonRecipe(
            title="",  # À compléter avec le reste du code
            rating=None,
            review_count=0,
            prep_time="",
            difficulty=difficulty,
            cost=cost,
            servings=0,
            ingredients=[],
            steps=[],
            tips=[],
            tags=[],
            url=url
        )
        
    except Exception as e:
        print(f"Erreur lors de l'extraction de la recette: {e}")
        return None
    


def print_recipe(recipe: MarmitonRecipe):
    if not recipe:
        print("Impossible de récupérer la recette")
        return
        
    print(f"Titre: {recipe.title}")
    print(f"Note: {recipe.rating}/5 ({recipe.review_count} avis)")
    print(f"Temps de préparation: {recipe.prep_time}")
    print(f"Difficulté: {recipe.difficulty}")
    print(f"Coût: {recipe.cost}")
    print(f"Nombre de portions: {recipe.servings}")
    
    print("\nIngrédients:")
    for ingredient in recipe.ingredients:
        print(f"- {ingredient}")
    
    print("\nÉtapes:")
    for i, step in enumerate(recipe.steps, 1):
        print(f"{i}. {step}")
    
    if recipe.tips:
        print("\nAstuces:")
        for tip in recipe.tips:
            print(f"- {tip}")
    
    if recipe.tags:
        print("\nTags:")
        print(", ".join(recipe.tags))


url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
recipe = get_recipe_details(url)
print_recipe(recipe)
