"""
afin de voir si la base de données est bien remplie, on va afficher les recettes
recipes_mix1 est la collection de la base de données 0safe-cook de 10 recettes
"""
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['0safe-cook']  # Nom de la base de données
recipes = db['recipes_mix1']  # Nom de la collection

# Correction ici : pas besoin de .find() sur recipe_list
for recipe in recipes.find():
    print(recipe["title"])
