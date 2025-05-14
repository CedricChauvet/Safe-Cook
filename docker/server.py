"""
This is the server file, it does pretty much everything in the application, 
it uses the MongoDB database, receives the images and returns the json. It also saves the annotated images in the mount folder

to run the docker run these instructions:

docker build -t docker_safecook .
docker run -it -p 5000:5000 -v ${PWD}/mount:/mount --name sc_v2 docker_safecook

This is an request "or" algorithm 

"""

import torch
import cv2
import os
import numpy as np
import uuid
import base64
from flask import Flask, request, jsonify
import traceback
from ultralytics import YOLO
from collections import Counter
from pymongo import MongoClient
import json
import re

app = Flask(__name__)


def search_in_db(aliments):
    """
    Retourne un json avec les recettes groupées par ordre décroissant de match.
    """
    if not aliments:
        raise ValueError("La photo n'a rien détecté")

    # Dictionnaire de traduction EN -> FR
    translations = {
        "carrot": "carotte",
        "broccoli": "brocoli",
        "banana": "banane",
        "apple": "pomme",
        "orange": "orange"
        # Ajouter d'autres traductions au besoin
    }

    # Appliquer les traductions
    translated_aliments = [translations.get(aliment, aliment) for aliment in aliments]
    
    # Utiliser un set pour éliminer les doublons
    aliments_set = set(translated_aliments)
    
    # Dictionnaire pour gérer les pluriels (singulier -> regex pattern)
    plurals = {
        "carotte": r"carotte[s]?",
        "brocoli": r"brocoli[s]?",
        "banane": r"banane[s]?",
        "pomme": r"pomme[s]?",
        "orange": r"orange[s]?",
        "pomme de terre": r"pomme[s]? de terre[s]?"
        # Ajouter d'autres pluriels selon besoin
    }
    
    # Dictionnaire des termes exacts à rechercher (avec gestion des pluriels)
    exact_terms = {
        "pomme de terre": r"pomme[s]? de terre[s]?"
        # Ajouter d'autres termes exacts si nécessaire
    }
    
    # Dictionnaire des exclusions
    exclusions = {
        "pomme": ["pomme de terre"]
        # Ajouter d'autres exclusions si nécessaire
    }
    
    # Récupérer les identifiants MongoDB
    mongodb_uri = os.environ.get("MONGODB_URI", 
                                "mongodb+srv://9184:f9XGDwYrIBnUnNkw@cluster0.ufblf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    try:
        client = MongoClient(mongodb_uri)
        db = client['0safe-cook']
        recipes_collection = db['v2']

        # Construire une requête qui gère les cas particuliers et les pluriels
        query_conditions = []
        
        for aliment in aliments_set:
            # Obtenir le pattern regex qui gère le pluriel
            pattern = plurals.get(aliment, f"{re.escape(aliment)}[s]?")
            
            # Vérifier s'il s'agit d'un terme exact à rechercher
            if aliment in exact_terms:
                # Rechercher exactement ce terme (avec gestion du pluriel)
                exact_pattern = exact_terms[aliment]
                query_conditions.append(
                    {"ingredients": {"$regex": f"\\b{exact_pattern}\\b", "$options": "i"}}
                )
            else:
                # Condition d'inclusion standard pour cet aliment (avec pluriel)
                inclusion = {"ingredients": {"$regex": f"\\b{pattern}\\b", "$options": "i"}}
                
                # Ajouter des conditions d'exclusion si nécessaire
                if aliment in exclusions:
                    for excluded in exclusions[aliment]:
                        # Obtenir le pattern d'exclusion avec gestion du pluriel
                        excl_pattern = plurals.get(excluded, f"{re.escape(excluded)}[s]?")
                        
                        # Créer une requête qui inclut l'aliment mais exclut l'expression spécifique
                        condition = {
                            "$and": [
                                inclusion,
                                {"ingredients": {"$not": {"$regex": f"\\b{excl_pattern}\\b", "$options": "i"}}}
                            ]
                        }
                        query_conditions.append(condition)
                else:
                    # Si pas d'exclusion, juste inclure l'aliment
                    query_conditions.append(inclusion)
        
        # Construire la requête finale avec un $or entre toutes les conditions
        requete = {"$or": query_conditions}

        resultats = recipes_collection.find(requete)
        
        # Liste pour stocker toutes les recettes avec leur nombre de matches
        recipes_with_matches = []
        
        for recipe in resultats:
            # Compter le nombre d'ingrédients qui matchent précisément
            matches = 0
            matching_ingredients = []
            
            for ingr in recipe.get('ingredients', []):
                for aliment in aliments_set:
                    # Obtenir le pattern avec gestion du pluriel
                    pattern = plurals.get(aliment, f"{re.escape(aliment)}[s]?")
                    
                    # Gestion spéciale pour les termes exacts
                    if aliment in exact_terms:
                        exact_pattern = exact_terms[aliment]
                        if re.search(f"\\b{exact_pattern}\\b", ingr, re.IGNORECASE):
                            matches += 1
                            matching_ingredients.append(ingr)
                            break
                    else:
                        # Vérifier si l'ingrédient contient l'aliment mais pas ses exclusions
                        if re.search(f"\\b{pattern}\\b", ingr, re.IGNORECASE):
                            # Vérifier les exclusions
                            should_exclude = False
                            if aliment in exclusions:
                                for excluded in exclusions[aliment]:
                                    # Pattern d'exclusion avec pluriel
                                    excl_pattern = plurals.get(excluded, f"{re.escape(excluded)}[s]?")
                                    if re.search(f"\\b{excl_pattern}\\b", ingr, re.IGNORECASE):
                                        should_exclude = True
                                        break
                            
                            if not should_exclude:
                                matches += 1
                                matching_ingredients.append(ingr)
                                break
            
            if matches > 0:  # Ne garder que les recettes avec au moins une correspondance
                # Convertir ObjectId en string
                recipe['_id'] = str(recipe['_id'])
                
                # Ajouter le nombre de matches et les ingrédients correspondants
                recipe['nombre_matches'] = matches
                recipe['matching_ingredients'] = matching_ingredients
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


# Charger le modèle au démarrage
try:
    model = YOLO("3mentors.pt")
    # model = YOLO("yolo11L-seg60.pt") ne detecte rien
    print("Modèle YOLO chargé avec succès")
except Exception as e:
    print("Erreur fatale lors du chargement du modèle :")
    print(traceback.format_exc())
    model = None

@app.route('/detect', methods=['POST'])
def detect_objects():
    """
    Endpoint pour la détection d'objets dans une image JPG
    Version simplifiée (v6)
    """
    print("Une requête est arrivée")
    if model is None:
        return jsonify({
            'error': 'Modèle YOLO non chargé'
        }), 500

    try:
        # Vérifier si une image est présente dans la requête
        if 'photo' not in request.files:
            return jsonify({"error": "Aucune image trouvée dans la requête"}), 400
            
        # Récupérer le fichier image
        image_file = request.files['photo']
        print(f"Image reçue: {image_file.filename}")
        
        # Récupérer les allergies si présentes
        allergies = []
        if 'allergies' in request.form:
            allergies = json.loads(request.form['allergies'])
            print(f"Allergies reçues: {allergies}")
        
        # Sauvegarder temporairement l'image pour la traiter avec YOLO
        UPLOAD_DIR = '/mount'
        unique_id = str(uuid.uuid4())
        temp_path = os.path.join(UPLOAD_DIR, f"{unique_id}_original.jpg")
        
        # Enregistrer l'image reçue
        image_file.save(temp_path)
        print(f"Image sauvegardée à: {temp_path}")
        
        # Charger l'image pour obtenir ses dimensions
        image = cv2.imread(temp_path)
        height, width = image.shape[:2]
        print(f"Dimensions de l'image: {width}x{height}")
        
        # Paramètres de détection
        conf_threshold = 0.25
        iou_threshold = 0.45
        
        # Exécuter la détection directement sur le fichier comme dans le premier code
        print("Exécution de la détection...")
        result = model(temp_path, conf=conf_threshold, iou=iou_threshold)[0]
        
        # Extraire les détections
        boxes = result.boxes
        num_detections = len(boxes)
        print(f"Nombre de détections: {num_detections}")
        
        # Traiter les résultats
        classes = []
        confidences = []
        labels = []
        
        # Parcourir les détections
        for box in boxes:
            cls = int(box.cls)
            class_name = result.names[cls]
            confidence = float(box.conf.item())
            
            classes.append(class_name)
            confidences.append(confidence)
            labels.append(class_name)
        
        # Comptage des classes
        class_counts = {}
        for cls in classes:
            if cls in class_counts:
                class_counts[cls] += 1
            else:
                class_counts[cls] = 1
        
        print(f"Classes détectées: {class_counts}")
        
        # Sauvegarder l'image avec les annotations
        result_filename = f"{unique_id}_with_boxes.jpg"
        result_path = os.path.join(UPLOAD_DIR, result_filename)
        result.save(filename=result_path)
        print(f"Image annotée sauvegardée à: {result_path}")
        
        # Chercher des recettes si des aliments sont détectés
        to_json = []
        if labels:
            to_json = search_in_db(labels)
            print(f"Nombre de recettes trouvées: {len(to_json)}")
        
        # Préparer la réponse
        return jsonify({
            'classes': classes,
            'class_counts': class_counts,
            'filename': result_filename,
            'original_filename': f"{unique_id}_original.jpg",
            'image_dimensions': {
                'width': width,
                'height': height
            },
            'detections': {
                'count': num_detections,
                'confidence_avg': sum(confidences) / len(confidences) if confidences else 0
            },
            'to_json': to_json
        })

    except Exception as e:
        print("Erreur lors de la détection:")
        print(traceback.format_exc())
        
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("Démarrage du serveur Flask... v3.0")
    app.run(host='0.0.0.0', port=5000)

