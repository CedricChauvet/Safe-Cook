

"""
cette partie du code recupere toutes les informations sur une recette de marmiton
herite des fichiers 0,1 et 2 de scrapping.py
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



def get_recipe_page(url: str) -> Optional[MarmitonRecipe]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:




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
