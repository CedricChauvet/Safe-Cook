

"""
cette partie du code recupere toutes les informations sur une recette
de marmiton herite des fichiers 0,1 et 2 de scrapping.py
il est fonctionnel
"""
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional

extract_ingredients = __import__('0-scrapping').extract_ingredients
extract_recipe_steps = __import__('1-scrapping').extract_recipe_steps
get_recipe_details = __import__('2-scrapping').get_recipe_details


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

    # url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
    # url1 = "https://www.marmiton.org/recettes/recette_quiche-poireaux-chevre-lardons_22275.aspx"
    # url2 = "https://www.marmiton.org/recettes/recette_risotto-aux-poireaux_19753.aspx"
    # url3 = "https://www.marmiton.org/recettes/recette_gratin-de-pates-lardons-et-champignons_37409.aspx"
    # url4 = "https://www.marmiton.org/recettes/recette_tajine-de-courgettes-patates-douces-et-raisins-secs_14597.aspx"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    ing_out = extract_ingredients(soup)
    steps = extract_recipe_steps(soup)
    title, note, prep_time, difficulty, cost, servings, = get_recipe_details(soup)

    return MarmitonRecipe(
        title=title,  # À compléter avec le reste du code
        rating=note,
        review_count=-1,
        prep_time=prep_time,
        difficulty=difficulty,
        cost=cost,
        servings=servings,
        ingredients=ing_out,
        steps=steps,
        tips=[],
        tags=[],
        url=url
    )


def print_recipe(recipe: MarmitonRecipe):
    if not recipe:
        print("Impossible de récupérer la recette")
        return
        url = "https://www.marmiton.org/recettes/"\
              "recette_pates-a-la-carbonara_80453.aspx"

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

    """
    partie inutile pour le moment
    # if recipe.tips:
    #     print("\nAstuces:")
    #     for tip in recipe.tips:
    #         print(f"- {tip}")
    # if recipe.tags:
    #     print("\nTags:")
    #     print(", ".join(recipe.tags))
    """

# url = "https://www.marmiton.org/recettes/"\
#       "recette_pates-a-la-carbonara_80453.aspx"
# recipe = get_recipe_page(url)
# print_recipe(recipe)
# print(to_json(recipe))
