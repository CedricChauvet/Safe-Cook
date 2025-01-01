"""
on entre dans la partie  base de données, mongoDB

petit topo des commandes mongoDB    

sudo service mongod start
mongosh

# Dans mongosh ou Python avec pymongo :

    # Lister toutes les recettes
    db.recipes.find()

    # Trouver une recette par nom
    db.recipes.find({"name": "Tarte aux pommes"})

    # Compter les recettes
    db.recipes.countDocuments()

    # Recherche avec projection (seulement certains champs)
    db.recipes.find({}, {"name": 1, "prep_time": 1})

    # Tri par temps de préparation
    db.recipes.find().sort({"prep_time": 1})

    # Recherche avec filtres
    db.recipes.find({"prep_time": {"$lt": 30}})  # Moins de 30 minutes
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
get_recipe_page = __import__('3-scrapping').get_recipe_page
print_recipe = __import__('3-scrapping').print_recipe


from pymongo import MongoClient



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


def to_json(recipe: MarmitonRecipe):
    return {
        "title": recipe.title,
        "rating": recipe.rating,
        "review_count": recipe.review_count,
        "prep_time": recipe.prep_time,
        "difficulty": recipe.difficulty,
        "cost": recipe.cost,
        "servings": recipe.servings,
        "ingredients": recipe.ingredients,
        "steps": recipe.steps,
        "tips": recipe.tips,
        "tags": recipe.tags,
        "url": recipe.url
    }


url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
url1 = "https://www.marmiton.org/recettes/recette_quiche-poireaux-chevre-lardons_22275.aspx"
url2 = "https://www.marmiton.org/recettes/recette_poulet-au-curry_22274.aspx"
url3 = "https://www.marmiton.org/recettes/recette_tarte-aux-pommes_22273.aspx"
url4 = "https://www.marmiton.org/recettes/recette_blanquette-de-dinde-aux-poireaux_24308.aspx"
url5 = "https://www.marmiton.org/recettes/recette_crepes-au-sarrasin-farcies-a-l-oeuf-fromage-et-jambon_71106.aspx"
url6 = "https://www.marmiton.org/recettes/recette_salade-cesar_32442.aspx"
url7 = "https://www.marmiton.org/recettes/recette_pommes-de-terres-sautees_36392.aspx"
url8 = "https://www.marmiton.org/recettes/recette_tarte-aux-pommes-a-l-alsacienne_11457.aspx"
url9 = "https://www.marmiton.org/recettes/recette_haricots-verts-a-la-carbonara_308397.aspx" 

# recipe = get_recipe_page(url1)

# print(print_recipe(recipe))
# recipe_json = to_json(recipe)  

# # Connexion à MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# db = client['0safe-cook']  # Nom de la base de données
# recipes = db['recipes_noel']  # Nom de la collection
# # Création d'un index unique sur le champ 'email'
# recipes.create_index([('title', ASCENDING)], unique=True)

# # db.recipes_noel.drop() /* Supprimer la collection */

# try:
#     result = recipes.insert_one(recipe_json)
#     print(f"Recette stockée avec l'ID: {result.inserted_id}")
# except DuplicateKeyError:
#     print(f"Erreur : Une recette avec le titre {recipe_json['title']} existe déjà.")



def into_db(urls):
    # Connexion à MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['0safe-cook']  # Nom de la base de données
    recipes_mix = db['recipes_mix1']  # Nom de la collection
    # Création d'un index unique sur le champ 'email'
    recipes_mix.create_index([('title', ASCENDING)], unique=True)

    for url in urls:
        print(url)
        recipe = get_recipe_page(url)
        recipe_json = to_json(recipe)
        print(recipe_json)
        try:
            result = recipes_mix.insert_one(recipe_json)
            print(f"Recette stockée avec l'ID: {result.inserted_id}")
        except DuplicateKeyError:
            print(f"Erreur : Une recette avec le titre {recipe_json['title']} existe déjà.") 
            pass


liste_recettes = [url, url1, url2, url3, url4, url5, url6, url7, url8, url9]
into_db(liste_recettes)