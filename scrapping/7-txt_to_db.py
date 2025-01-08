"""
prendre en charge un ou plusieurs txt contenant des urls de recettes Marmiton
et les ajouter à la base de données MongoDB

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
import os
import glob
from dataclasses import dataclass
from typing import List
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
get_recipe_page = __import__('3-scrapping').get_recipe_page
print_recipe = __import__('3-scrapping').print_recipe


@dataclass
class MarmitonRecipe:
    title: str
    rating: float
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
def into_db(urls):
    # Connexion à MongoDB
   
    uri = "mongodb+srv://9184:f9XGDwYrIBnUnNkw@cluster0.ufblf.mongodb.net/"
    # Créer une instance de client
    client = MongoClient(uri)


    db = client['0safe-cook']  # Nom de la base de données
    recipes_mix = db['recipes_many_txt']  # Nom de la collection

    # Création d'un index unique sur le champ 'title'
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


def main():


    # Spécifiez le chemin du répertoire
    path = '/mnt/c/Users/chauv/Desktop/holberton-demoday/Safe-Cook/scrapping/bdd_txt/'

    # Utilisez glob pour trouver tous les fichiers .txt
    fichiers_txt = glob.glob(os.path.join(path, '*.txt'))
    liste_recettes = [] 
    for file in fichiers_txt:
        
        # Liste des recettes
        for fichier in fichiers_txt:
            
            with open(fichier, 'r', encoding='utf-8') as f:
                liste_txt = f.readlines()
                for url in liste_txt:
                    if url[0:4] == 'http':
                        url = url.replace("\n", "")
                        # print(url)
                        liste_recettes.append(url)
                    # recipe_json = to_json(recipe)
                    # print(recipe_json)
                    # try:
                    #     result = recipes_mix.insert_one(recipe_json)
                    #     print(f"Recette stockée avec l'ID: {result.inserted_id}")

                    # except DuplicateKeyError:
                    #     print(f"Erreur : Une recette avec le titre {recipe_json['title']} existe déjà.")
                    #     pass  
            # Appel de la fonction into_db
            # into_db(liste_recettes)
            # print(liste_recettes)
    # liste_recettes = [url, url1, url2, url3, url4, url5, url6, url7, url8, url9]

    # # Appel de la fonction into_db
    print(liste_recettes) 
    into_db(liste_recettes)


if __name__ == "__main__":
    main()
