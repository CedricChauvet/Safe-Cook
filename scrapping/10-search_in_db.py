from pymongo import MongoClient
from typing import List, Dict, Any

def search_in_db(aliments: List[str]) -> List[Dict[Any, Any]]:
    """
    Retourne un json avec les recettes groupées par ordre décroissant de match.
    """



    if not aliments:
        raise ValueError("La photo n'a rien détecté")

    # Conversion en set pour éliminer les doublons
    aliments = set(aliments)
    
    uri = "mongodb+srv://9184:f9XGDwYrIBnUnNkw@cluster0.ufblf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = MongoClient(uri)
        db = client['0safe-cook']
        recipes_collection = db['demo-day']

        # Requête pour trouver toutes les recettes avec au moins un ingrédient
        requete = {
            "$or": [
                {"ingredients": {"$regex": f"\\b{aliment}\\b", "$options": "i"}}
                for aliment in aliments
            ]
        }

        resultats = recipes_collection.find(requete)
        
        # Liste pour stocker toutes les recettes avec leur nombre de matches
        recipes_with_matches = []
        
        for recipe in resultats:
            # Compter le nombre d'ingrédients qui matchent
            matches = sum(
                1 for aliment in aliments 
                if any(aliment.lower() in ingr.lower() for ingr in recipe.get('ingredients', []))
            )
            
            if matches > 0:  # Ne garder que les recettes avec au moins une correspondance
                # Convertir ObjectId en string
                recipe['_id'] = str(recipe['_id'])
                
                # Ajouter le nombre de matches aux informations de la recette
                recipe['nombre_matches'] = matches
                recipes_with_matches.append(recipe)

        # Trier les recettes par nombre de matches décroissant
        recipes_with_matches.sort(key=lambda x: x['nombre_matches'], reverse=True)

        return recipes_with_matches

    except Exception as e:
        print(f"Une erreur est survenue dans la recherche des recettes : {e}")
        return []

    finally:
        if 'client' in locals():
            client.close()

            
if __name__ == '__main__':
    aliments = ["pomme", "orange"]
    to_json = search_in_db(aliments)
    print(len(to_json))
    print(to_json[2])