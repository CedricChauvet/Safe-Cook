"""
docker build -t docker_safecook .
docker run -it -p 5000:5000 -v ${PWD}/mount:/mount --name sc_v2 docker_safecook
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

app = Flask(__name__)



def search_in_db(aliments):
    if len(aliments) == 0:
        raise ValueError("La photo n'a rien détecté")

    # aliments = aliments.replace("carrot","carotte")
    aliments = ["carotte" if x == "carrot" else x for x in aliments]
    aliments = ["brocoli" if x == "broccoli" else x for x in aliments]
    aliments = ["pomme" if x == "apple" else x for x in aliments]
    aliments = ["orange" if x == "orange" else x for x in aliments]


    aliments= set(aliments)
    uri = "mongodb+srv://9184:f9XGDwYrIBnUnNkw@cluster0.ufblf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    client = MongoClient(uri)
    db = client['0safe-cook']
    recipes_collection = db['demo-day'] # attention a choisir la bonne base de données
    try:
        # Requête qui fonctionne correctement
        requete = {
            "$and": [
                {"ingredients": {"$regex": aliment, "$options": "i"}} 
                for aliment in aliments
            ]
        }

        resultats = recipes_collection.find(requete)

        # for recipe in resultats:
        #     print(recipe["title"])

        # Convertir les résultats en liste de dictionnaires JSON
        recipes_json = []
        for recipe in resultats:
            # Convertir ObjectId en string pour permettre la sérialisation JSON
            recipe['_id'] = str(recipe['_id'])
            recipes_json.append(recipe)
        
        # print("nombre de recettes trouvées", len(recipes_json),"\n", recipes_json[0])
        return recipes_json if recipes_json else []

    except Exception:
        # Retourne un JSON vide en cas d'erreur
        print(f"Une erreur est survenue dans la recherche des recettes : {e}")
        return []


    


# Charger le modèle au démarrage
try:
    model = YOLO("yolo11x.pt")
 
    print("Modèle YOLO chargé avec succès")
except Exception as e:
    print("Erreur fatale lors du chargement du modèle :")
    print(traceback.format_exc())
    model = None


@app.route('/detect', methods=['POST'])
def detect_objects():
    """
    Endpoint pour la détection de classes d'objets
    """
    if model is None:
        return jsonify({
            'error': 'Modèle YOLO non chargé',
            'details': 'Échec du chargement initial du modèle'
        }), 500

    if 'image' not in request.json:
        return jsonify({'error': 'Pas d\'image fournie'}), 400

    try:
        # Décoder l'image base64
        image_b64 = request.json['image']

        # Enlever le préfixe data:image si présent
        if image_b64.startswith('data:image'):
            # Extraire uniquement la partie base64 après la virgule
            image_b64 = image_b64.split(',')[1]

        print("Image reçue, décodage en cours...")
        # Décoder
        image_bytes = base64.b64decode(image_b64)
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Vérification et resize
        if image is None:
            raise ValueError("Échec du décodage de l'image")


        # premiere version du resize   
        # image = cv2.resize(image, (640, 640))
        image = resize_for_yolo(image, target_size=640)
        # Vérification de l'image
        if image is None:
            return jsonify({
                'error': 'Impossible de décoder l\'image',
                'details': 'La conversion en image a échoué'
            }), 500

        # Définir le chemin vers le répertoire monté
        # c'est le chemin du conteneur

        # # Générer un nom de fichier unique avec UUID
        # unique_id = str(uuid.uuid4())
        # filename = f"{unique_id}.jpg"
        # filepath = os.path.join(UPLOAD_DIR, filename)
        # # Sauvegarder l'image originale sous format uuid
        # with open(filepath, 'wb') as f:
        #     f.write(image_bytes)

        # Conversion en tensor
        image_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        image_tensor = image_tensor.unsqueeze(0)

        # Détecter les objets, bien choisir le seuil de confiance
        results = model(image_tensor, conf=0.5)

        # Traitement des détections
        detections = []
        classes = []
        boxes = []
        confidences = []
        labels = []
        aliments = ()

        allowed = ["apple", "broccoli", "orange", "carrot"] # evite de prendre les autres objets de yol


        for box in results[0].boxes:
            
            class_name = model.names[int(box.cls)]
            if class_name in allowed:
                confidence = float(box.conf.item())
                bbox = box.xyxy[0]  # Format: x1, y1, x2, y2
                
                classes.append(class_name)
                detections.append((class_name, confidence))
                boxes.append(bbox)
                confidences.append(confidence)
                labels.append(class_name)

        print("les labels", labels)
        to_json = search_in_db(labels)
        print("nombre de recettes", len(to_json))

        class_counts = dict(Counter(classes))

        # Générer un nom de fichier unique

        # Générer un nom de fichier unique
        unique_id = uuid.uuid4()


        image_with_boxes = draw_detections(
            image, 
            torch.stack(boxes), 
            labels, 
            confidences
        )

        UPLOAD_DIR = '/mount'

        filename = f"{unique_id}_with_boxes.jpg"
        filepath = os.path.join(UPLOAD_DIR, filename)
        cv2.imwrite(str(filepath), image_with_boxes)


        # partie renvoyée au client
        # classes : liste des classes détectées
        # class_counts : nombre d'instances par classe
        # filename : nom du fichier sauvegardé
        # json contient les recettes filtrées apres photo
        return jsonify({
            'classes': classes,
            'class_counts': class_counts,
            'filename': filename,
            'to_json': to_json
        })

    except Exception as e:
        # Imprimer l'erreur complète côté serveur
        print("Erreur lors de la détection :")
        print(traceback.format_exc())

        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500



def resize_for_yolo(image, target_size=640):
    """
    Redimensionne une image pour YOLO en préservant le ratio d'aspect.
    Ajoute du padding noir si nécessaire pour obtenir une image carrée.
    
    Args:
        image: Image source (format numpy array)
        target_size: Taille cible (par défaut 640)
    
    Returns:
        Image redimensionnée avec padding si nécessaire
    """
    height, width = image.shape[:2]
    
    # Calcul du ratio pour le redimensionnement
    ratio = float(target_size) / max(height, width)
    if ratio >= 1:
        ratio = 1
        
    # Nouvelles dimensions en préservant le ratio
    new_height = int(height * ratio)
    new_width = int(width * ratio)
    
    # Redimensionnement de l'image
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    # Création d'une image noire de la taille cible
    square_img = np.zeros((target_size, target_size, 3), dtype=np.uint8)
    
    # Calcul des offsets pour centrer l'image
    y_offset = (target_size - new_height) // 2
    x_offset = (target_size - new_width) // 2
    
    # Copie de l'image redimensionnée sur le fond noir
    square_img[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized
    
    return square_img

def draw_detections(
    image,
    boxes,
    labels,
    confidences
) -> np.ndarray:
    """
    Dessine les boîtes de détection et les étiquettes sur l'image.
    
    Args:
        image: Image numpy
        boxes: Tenseur des boîtes de détection (x1, y1, x2, y2)
        labels: Liste des noms de classes
        confidences: Liste des scores de confiance
    
    Returns:
        Image avec les détections dessinées
    """
    img_with_boxes = image.copy()
    
    for box, label, conf in zip(boxes, labels, confidences):
        # Coordonnées de la boîte
        x1, y1, x2, y2 = map(int, box.tolist())
        
        # Couleur aléatoire pour chaque classe
        color = tuple(np.random.randint(0, 255, 3).tolist())
        
        # Dessiner la boîte
        cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), color, 2)
        
        # Préparer le texte
        text = f"{label} {conf:.2f}"
        
        # Obtenir les dimensions du texte
        (text_width, text_height), _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
        )
        
        # Dessiner le fond du texte
        cv2.rectangle(
            img_with_boxes,
            (x1, y1 - text_height - 10),
            (x1 + text_width + 10, y1),
            color,
            -1
        )
        
        # Ajouter le texte
        cv2.putText(
            img_with_boxes,
            text,
            (x1 + 5, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
    
    return img_with_boxes


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

