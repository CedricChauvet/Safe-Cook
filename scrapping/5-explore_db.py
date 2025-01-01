from pymongo import MongoClient

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['0safe-cook']  # Nom de la base de données
recipes = db['recipes_noel']  # Nom de la collection

# Correction ici : pas besoin de .find() sur recipe_list
for recipe in recipes.find():
    print(recipe["title"])
