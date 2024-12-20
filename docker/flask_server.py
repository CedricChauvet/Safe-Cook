import torch
import cv2

import numpy as np
import uuid
import base64
from flask import Flask, request, jsonify
import traceback
import sys
import subprocess
from ultralytics import YOLO
from collections import Counter

app = Flask(__name__)

# Chemin de sauvegarde des images
SAVE_PATH = '/data/images_server'


def load_yolo_model():
    """
    Tenter de charger le modèle YOLO avec des diagnostics détaillés
    """
    try:
    #     print("Début du chargement du modèle YOLO")
    #     print(f"Python version: {sys.version}")
    #     print(f"PyTorch version: {torch.__version__}")
    #     print(f"Torch hub path: {torch.hub.get_dir()}")

    #     # Vérifier si CUDA est disponible
    #     print(f"CUDA disponible: {torch.cuda.is_available()}")
        
        # Tenter de charger le modèle
        model = YOLO("yolo11x.pt")    
        print("Modèle YOLO chargé avec succès")
        return model
    except Exception as e:
        print("Erreur lors du chargement du modèle :")
        print(traceback.format_exc())
        return None

# Charger le modèle au démarrage
try:
    model = load_yolo_model()
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
        image_bytes = base64.b64decode(image_b64)
        
        # Conversion explicite en numpy
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        
        # Vérification de l'image
        if image is None:
            return jsonify({
                'error': 'Impossible de décoder l\'image',
                'details': 'La conversion en image a échoué'
            }), 500
        


                # Générer un nom de fichier unique
        filename = "mon_test_img.jpg"
        # filename = f"{uuid.uuid4()}.jpg"
        filepath =  f"./mon_test_img.jpg"
        
        # Sauvegarder l'image originale
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Conversion en tensor
        image_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        image_tensor = image_tensor.unsqueeze(0)
        
        # Détecter les objets
        results = model(image_tensor, conf=0.25)
        
        
        classes = []
        for box in results[0].boxes:
            class_name = model.names[int(box.cls)]
            confidence = box.conf.item()
            print(f"Classe : {class_name}, Confiance : {confidence}")
            classes.append(class_name)
        class_counts = dict(Counter(classes))
    
        return jsonify({
            'classes': classes,
            'class_counts': class_counts,
            'filename': filename
        })


    except Exception as e:
        # Imprimer l'erreur complète côté serveur
        print("Erreur lors de la détection :")
        print(traceback.format_exc())
        
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000)